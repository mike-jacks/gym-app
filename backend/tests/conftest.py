from uuid import UUID
from typing import Annotated
import json
import pytest
from pydantic import ValidationError
from httpx import Response
from jose import JWTError, jwt
from fastapi.testclient import TestClient
from fastapi.security import SecurityScopes
from fastapi import HTTPException, Depends, status
from db import Session, SQLModel, create_engine, get_db
from sqlmodel.pool import StaticPool
from sqlmodel import select, insert
from models.relationship_merge import Exercise, User, WorkoutCategory, MovementCategory, MajorMuscle, SpecificMuscle, Equipment, BandColor, Role
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event
from utilities.authorization import get_current_user, oauth2_scheme, SECRET_KEY, ALGORITHM, TokenData
from main import app

def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def build_database(engine):
    with open("exercise_json/new_exercise_json.json", 'r') as file:
        exercise_data = json.load(file)   
    with Session(bind=engine) as session:
        for exercise in exercise_data:
            if not session.exec(select(WorkoutCategory).where(WorkoutCategory.name == exercise["workoutCategory"].title())).first():
                session.exec(insert(WorkoutCategory).values(name=exercise["workoutCategory"].title()))
            if not session.exec(select(MovementCategory).where(MovementCategory.name == exercise["movementCategory"].title())).first():
                session.exec(insert(MovementCategory).values(name=exercise["movementCategory"].title()))
            if not session.exec(select(MajorMuscle).where(MajorMuscle.name == exercise["majorMuscle"].title())).first():
                session.exec(insert(MajorMuscle).values(name=exercise["majorMuscle"].title()))
            for specific_muscle in exercise["specificMuscles"]:
                if not session.exec(select(SpecificMuscle).where(SpecificMuscle.name == specific_muscle.title())).first():
                    session.exec(insert(SpecificMuscle).values(name=specific_muscle.title()))
            if not session.exec(select(Equipment).where(Equipment.name == exercise["equipment"].title())).first():
                session.exec(insert(Equipment).values(name=exercise["equipment"].title()))
        roles = {"User", "Admin"}
        for role in roles:
            if not session.exec(select(Role).where(Role.name == role)).first():
                session.add(Role(name=role)) 
        band_colors = ["yellow", "red", "green", "black", "purple", "blue", "orange", "gray"]
        for color in band_colors:
            if not session.exec(select(BandColor).where(BandColor.name == color.title())).first():
                session.exec(insert(BandColor).values(name=color.title()))
        session.commit()
        return session
    

@pytest.fixture
def session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    event.listen(engine, "connect", set_sqlite_pragma)
    SQLModel.metadata.create_all(engine)
    return build_database(engine) 

@pytest.fixture
def client(session: Session):
    def get_db_override():
        return session
    
    def override_get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
        if security_scopes.scopes:
            authenticate_value = f"Bearer scope={security_scopes.scopes}"
        else:
            authenticate_value = "Bearer"
        credentials_exception = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_uuid: UUID = UUID(payload.get("sub"))
            if user_uuid is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(user_uuid=user_uuid, scopes=token_scopes)
        except (JWTError, ValidationError):
            raise credentials_exception
        user = session.exec(select(User).where(User.uuid == token_data.user_uuid)).first()
        if user is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user
    
    app.dependency_overrides[get_db] = get_db_override
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    admin_data = {
        "username": "admin",
        "hashed_password": "admin",
        "first_name": "Admin",
        "last_name": "Admin",
        "birthday": "2020-05-03",
        "body_weight": 200,
        "height": 80,
        "gender": "male"
    }

    user_data = {
        "username": "user",
        "hashed_password": "user",
        "first_name": "User",
        "last_name": "User",
        "birthday": "2024-01-01",
        "body_weight": 100,
        "height": 70,
        "gender": "male"
    }
    client.post("/users/register", json=admin_data)
    client.post("/users/register", json=user_data).json()
    user: User = session.exec(select(User).where(User.username == "admin")).first()
    user.roles = [session.exec(select(Role).where(Role.name == "Admin")).first()]


    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def client_full_db(client_login: TestClient, session: Session):
    client: TestClient = client_login("admin", "admin")
    user_data = [
        {
            "username": "programmerOne",
            "hashed_password": "programmer1",
            "first_name": "Wade",
            "last_name": "Watts",
            "birthday": "2020-05-03",
            "body_weight": 150,
            "height": 77,
            "gender": "male"
        },
        {
            "username": "ZeroCool",
            "hashed_password": "hackers",
            "first_name": "Dade",
            "last_name": "Murphy",
            "birthday": "2020-05-03",
            "body_weight": 160,
            "height": 70,
            "gender": "male"
        },
        {
            "username": "MI",
            "hashed_password": "MI5",
            "first_name": "Ethan",
            "last_name": "Hunt",
            "birthday": "1985-05-03",
            "body_weight": 165,
            "height": 50,
            "gender": "male"
        }
    ]
    for user in user_data:
        client.post("/users/register", json=user)
    
    exercise_data = [
        {
            "name": "Barbell Chest Press",
            "description": "Barbell Chest Press Description",
            "workout_category": "Upper",
            "movement_category": "Press",
            "equipment": "Barbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ]
        },
        {
            "name": "Dumbbell Chest Press",
            "description": "Dumbbell Chest Press Description",
            "workout_category": "Upper",
            "movement_category": "Press",
            "equipment": "Dumbbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ]
        },
        {
            "name": "Dumbbell Chest Fly",
            "description": "Dumbbell Chest Fly Description",
            "workout_category": "Upper",
            "movement_category": "Fly",
            "equipment": "Dumbbell",
            "major_muscle": "Chest", 
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ]
        },
    ]
    
    for exercise in exercise_data:
        client.post("/users/me/exercises", json=exercise)
    
    
    
    yield client

@pytest.fixture
def client_login(client: TestClient):
    def login(username: str, password: str):
        response: Response = client.post("/users/login", data={"username": username, "password": password})
        client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
        return client
    yield login