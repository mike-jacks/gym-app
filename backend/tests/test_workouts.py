from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from httpx import Response
from db import Session
from sqlmodel import select
from models.relationship_merge import Workout, User



def test_get_empty_workouts(client_login: TestClient):
    client: TestClient = client_login("user", "user")
    response: Response = client.get(f"/users/me/workouts")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict['data'] == []
    assert response_dict['detail'] == "0 workouts fetched successfully."

def test_get_workouts(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_data = {
        "name": "Back Day",
        "description": "Back Day Description"
        }
    response = client_full_db.post(f"/users/me/workouts", json=workout_data)
    user_uuid = client_full_db.get("/users/me").json()['data']['uuid']
    user = session.exec(select(User).where(User.uuid == UUID(user_uuid))).first()
    workout_uuid = session.exec(select(Workout).where(Workout.name == "Back Day").where(Workout.user_id == user.id)).first().uuid
    response: Response = client_full_db.get(f"/users/me/workouts")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict['data'] == [
        {
            "name": "Back Day",
            "description": "Back Day Description",
            "uuid": str(workout_uuid),
            "workout_exercises": []
        }
    ]

def test_get_workout(client_full_db: TestClient):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_data = {
        "name": "Chest Day",
        "description": "Chest Day Description"
    }
    client_full_db.post(f"/users/me/workouts", json=workout_data)
    workout_uuid = client_full_db.get(f"/users/me/workouts").json()["data"][0]["uuid"]
    response: Response = client_full_db.get(f"/users/me/workouts/{workout_uuid}")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict['data'] == {
        "name": "Chest Day",
        "description": "Chest Day Description",
        "uuid": workout_uuid,
        "workout_exercises": []
    }
    assert response_dict['detail'] == "Workout fetched successfully."

def test_post_workout(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_data = {
        "name": "Leg Day",
        "description": "Leg Day Description"
        }
    response: Response = client_full_db.post(f"/users/me/workouts", json=workout_data)
    response_dict = response.json()
    assert response.status_code == 201
    assert response_dict['data'] == {
        "name": "Leg Day",
        "description": "Leg Day Description",
        "uuid": response_dict['data']['uuid'],
        "workout_exercises": []
    }
    assert response_dict['detail'] == "Workout added successfully."
    assert session.exec(select(Workout).where(Workout.uuid == UUID(response_dict['data']['uuid']))).first().model_dump() == {
        "id": session.exec(select(Workout).where(Workout.uuid == UUID(response_dict['data']['uuid']))).first().id,
        "uuid": UUID(response_dict['data']['uuid']),
        "name": "Leg Day",
        "description": "Leg Day Description",
        "user_id": 2
    }

def test_put_workout(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_data = {
        "name": "Back Day",
        "description": "Back Day Description"
        
    }
    workout_uuid = client_full_db.post(f"/users/me/workouts", json=workout_data).json()["data"]["uuid"]
    workout_data = {
        "name": "Leg Day",
        "description": "Leg Day Description"
        }
    response: Response = client_full_db.put(f"/users/me/workouts/{workout_uuid}", json=workout_data)
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict['data'] == {
        "name": "Leg Day",
        "description": "Leg Day Description",
        "uuid": workout_uuid,
        "workout_exercises": []
    }
    assert response_dict['detail'] == "Workout updated successfully."
    assert session.exec(select(Workout).where(Workout.uuid == UUID(workout_uuid))).first().model_dump() == {
        "id": session.exec(select(Workout).where(Workout.uuid == UUID(workout_uuid))).first().id,
        "uuid": UUID(workout_uuid),
        "name": "Leg Day",
        "description": "Leg Day Description",
        "user_id": 2
    }

def test_patch_workout(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_data = {
        "name": "Leg Day",
        "description": "Leg Day Description"
    }
    workout_uuid = client_full_db.post(f"/users/me/workouts", json=workout_data).json()["data"]["uuid"]
    response: Response = client_full_db.patch(f"/users/me/workouts/{workout_uuid}", json={"name": "Arm Day"})
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict['data'] == {
        "name": "Arm Day",
        "description": "Leg Day Description",
        "uuid": workout_uuid,
        "workout_exercises": []
    }
    assert response_dict['detail'] == "Workout updated successfully."
    assert session.exec(select(Workout).where(Workout.uuid == UUID(workout_uuid))).first().model_dump() == {
        "id": session.exec(select(Workout).where(Workout.uuid == UUID(workout_uuid))).first().id,
        "uuid": UUID(workout_uuid),
        "name": "Arm Day",
        "description": "Leg Day Description",
        "user_id": 2
    }

def test_delete_workout(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_data = {
        "name": "Leg Day",
        "description": "Leg Day Description"
        }
    workout_uuid = client_full_db.post(f"/users/me/workouts", json=workout_data).json()["data"]["uuid"]
    response: Response = client_full_db.delete(f"/users/me/workouts/{workout_uuid}")
    assert response.status_code == 204
    assert not session.exec(select(Workout).where(Workout.uuid == UUID(workout_uuid))).first()