from fastapi.testclient import TestClient
from httpx import Response
from db import Session
from sqlmodel import select
from models.relationship_merge import User

def test_get_one_user(client_login: TestClient, session: Session):
    client: TestClient = client_login("admin", "admin")
    response: Response = client.get("/users/users")
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 200
    assert response_dict == {
        'data': [
            {
                "uuid": str(session.exec(select(User).where(User.username == "user")).first().uuid),
                "username": "user",
                "first_name": "User",
                "last_name": "User",
                "birthday": "2024-01-01",
                "body_weight": 100.0,
                "height": 70,
                "roles": [
                    "User"
                ],
                "gender":"male"
                }
            ],
        'detail': '1 user fetched successfully.',
        }

def test_get_users(client_full_db: TestClient, session: Session):
    response: Response = client_full_db.post("/users/login", data={"username": "admin", "password": "admin"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response: Response = client_full_db.get("/users/users")
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 200
    assert response_dict['detail'] == "4 users fetched successfully."
    assert len(response_dict['data']) == 4
    assert response_dict == {
        'data': [
            {
                "uuid": str(session.exec(select(User).where(User.username == "user")).first().uuid),
                "username": "user",
                "first_name": "User",
                "last_name": "User",
                "birthday": "2024-01-01",
                "body_weight": 100.0,
                "height": 70,
                "roles": [
                    "User"
                ],
                "gender":"male"
                },
            {
                "username": "programmerOne",
                "first_name": "Wade",
                "last_name": "Watts",
                "birthday": "2020-05-03",
                "body_weight": 150.0,
                "height": 77,
                "gender": "male",
                "uuid": f"{session.exec(select(User).where(User.username == "programmerOne")).first().uuid}",
                "roles": [
                    "User"
                ]
                },
            {
                "username": "ZeroCool",
                "first_name": "Dade",
                "last_name": "Murphy",
                "birthday": "2020-05-03",
                "body_weight": 160.0,
                "height": 70,
                "gender": "male",
                "uuid": f"{session.exec(select(User).where(User.username == "ZeroCool")).first().uuid}",
                "roles": [
                    "User"
                ]
                },
            {
                "username": "MI",
                "first_name": "Ethan",
                "last_name": "Hunt",
                "birthday": "1985-05-03",
                "body_weight": 165.0,
                "height": 50,
                "gender": "male",
                "uuid": f"{session.exec(select(User).where(User.username == "MI")).first().uuid}",
                "roles": [
                    "User"
                ]
                }
            ],
        'detail': '4 users fetched successfully.'
    }

def test_post_user(client_login: TestClient, session: Session):
    client: TestClient = client_login("admin", "admin")
    user = session.exec(select(User).where(User.username == 'admin')).first()
    response = client.delete(f"/users/{user.uuid}")
    assert response.status_code == 204

    data = {
        "username": "programmerOne",
        "hashed_password": "programmer1",
        "first_name": "Wade",
        "last_name": "Watts",
        "birthday": "2020-05-03",
        "body_weight": 150,
        "height": 77,
        "gender": "male"
    }
    response: Response = client.post("/users/register", json=data)
    response_dict: dict[str, object] = response.json()
    assert len(session.exec(select(User)).all()) == 2
    assert response.status_code == 201
    assert response_dict == {
        'data':{
                "username": "programmerOne",
                "first_name": "Wade",
                "last_name": "Watts",
                "birthday": "2020-05-03",
                "body_weight": 150.0,
                "height": 77,
                "gender": "male",
                "uuid": f"{session.exec(select(User).where(User.username == 'programmerOne')).first().uuid}",
                "roles": [
                    "User"
                ]
                },
        'detail': 'New User has been added.'
        }

def test_put_user(client_full_db: TestClient, session: Session):
    data = {
        "username": "programmerOne",
        "hashed_password": "programmer1",
        "first_name": "Wade",
        "last_name": "Watts",
        "birthday": "2020-05-03",
        "body_weight": 100,
        "height": 70,
        "gender": "female"
    }
    user = session.exec(select(User).where(User.username == 'programmerOne')).first()
    user_uuid = user.uuid
    response: Response = client_full_db.post("/users/login", data={"username": user.username, "password": "programmer1"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response: Response = client_full_db.put(f"/users/me", json=data)
    response_dict: dict[str, object] = response.json()
    session.refresh(user)
    assert response.status_code == 200
    assert response_dict == {
        'data':{
                "username": "programmerOne",
                "first_name": "Wade",
                "last_name": "Watts",
                "birthday": "2020-05-03",
                "body_weight": 100.0,
                "height": 70,
                "gender": "female",
                "uuid": f"{session.exec(select(User).where(User.username == 'programmerOne')).first().uuid}",
                "roles": [
                    "User"
                ]
                },
        'detail': 'User updated.'
    }
    assert user.username == "programmerOne"
    assert user.first_name == "Wade"
    assert user.last_name == "Watts"
    assert user.birthday.isoformat() == "2020-05-03"
    assert user.body_weight == 100.0
    assert user.height == 70
    assert user.gender == "female"
    assert user.uuid == user_uuid

def test_patch_user(client_full_db: TestClient, session: Session):
    data = {
        "body_weight": 200,
        "height": 80
    }
    user = session.exec(select(User).where(User.username == 'programmerOne')).first()
    response = client_full_db.post("/users/login", data={"username": user.username, "password": "programmer1"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response: Response = client_full_db.patch(f"/users/me", json=data)
    response_dict: dict[str, object] = response.json()
    session.refresh(user)
    assert response.status_code == 200
    assert response_dict == {
        'data':{
                "username": "programmerOne",
                "first_name": "Wade",
                "last_name": "Watts",
                "birthday": "2020-05-03",
                "body_weight": 200.0,
                "height": 80,
                "gender":"male",
                "uuid": str(user.uuid),
                "roles": [
                    "User"
                ]
                },
        'detail': 'User updated.'
    }

def test_delete_user(client_full_db: TestClient, session: Session):
    admin = session.exec(select(User).where(User.username == 'admin')).first()
    user = session.exec(select(User).where(User.username == 'programmerOne')).first()
    response = client_full_db.post("/users/login", data={"username": admin.username, "password": "admin"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    user_uuid = user.uuid
    response: Response = client_full_db.delete(f"/users/{user_uuid}")
    assert response.status_code == 204
    assert len(session.exec(select(User)).all()) == 4
    assert not session.exec(select(User).where(User.username == 'programmerOne')).first()
    assert session.exec(select(User).where(User.username == 'ZeroCool')).first()
    assert session.exec(select(User).where(User.username == 'MI')).first()
    assert session.exec(select(User).where(User.username == 'admin')).first()