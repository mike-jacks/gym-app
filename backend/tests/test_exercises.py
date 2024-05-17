import pytest
from uuid import UUID
from fastapi.testclient import TestClient
from httpx import Response
from db import Session
from sqlmodel import select
from models.relationship_merge import Exercise

def test_get_empty_exercises(client_login: TestClient):
    client = client_login("admin", "admin")
    response: Response = client.get("users/me/exercises")
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 200
    assert len(response_dict['data']) == 0
    assert response_dict['data'] == []

def test_get_exercises(client_full_db: TestClient, session: Session):
    response: Response = client_full_db.get("users/me/exercises")
    response_dict: dict[str, object] = response.json()
    for data in response_dict['data']:
        data['specific_muscles'].sort()
    response_dict['data'].sort(key=lambda x: x['name'])
    assert response.status_code == 200
    assert len(response_dict['data']) == 3
    assert response_dict == {
        'data': [
            {
            "uuid": str(session.exec(select(Exercise).where(Exercise.uuid == UUID(response_dict['data'][0]['uuid']))).first().uuid),
            "name": "Barbell Chest Press",
            "description": "Barbell Chest Press Description",
            "workout_category": "Upper",
            "movement_category": "Press",
            "equipment": "Barbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ],
            "image_url": None
        },
        {
            "uuid": str(session.exec(select(Exercise).where(Exercise.uuid == UUID(response_dict['data'][1]['uuid']))).first().uuid),
            "name": "Dumbbell Chest Fly",
            "description": "Dumbbell Chest Fly Description",
            "workout_category": "Upper",
            "movement_category": "Fly",
            "equipment": "Dumbbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ],
            "image_url": None
        },
        {
            "uuid": str(session.exec(select(Exercise).where(Exercise.uuid == UUID(response_dict['data'][2]['uuid']))).first().uuid),
            "name": "Dumbbell Chest Press",
            "description": "Dumbbell Chest Press Description",
            "workout_category": "Upper",
            "movement_category": "Press",
            "equipment": "Dumbbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ],
            "image_url": None
        },
        ],
        'detail': 'Exercises fetched successfully.'
    }

def test_post_exercise(client_login: TestClient, session: Session):
    client = client_login("user", "user")
    data = {
        "name": "Chest Press",
        "description": "Chest Press Description",
        "workout_category": "Upper",
        "movement_category": "Press",
        "equipment": "Dumbbell",
        "major_muscle": "Chest",
        "specific_muscles": [
            "Middle Chest", "Triceps"
        ],
        "image_url": None
    }
    response: Response = client.post("/users/me/exercises", json=data)
    response_dict = response.json()
    response_dict["data"]["specific_muscles"].sort()
    if 'detail' in response_dict:
        if 'msg' in response_dict['detail']:
            print(f"ERROR: {response_dict['detail']['msg']}")
    exercises = session.exec(select(Exercise).where(Exercise.name == response_dict["data"]["name"])).all()
    exercise_uuid = exercises[0].uuid
    assert response.status_code == 201
    expected_response = {
        "data": {
            "name": "Chest Press",
            "description": "Chest Press Description",
            "workout_category": "Upper",
            "movement_category": "Press",
            "equipment": "Dumbbell",
            "uuid": str(exercise_uuid),
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest",
                "Triceps"
            ],
            "image_url": None
            },
        "detail": "Exercise added successfully."
        }
    expected_response["data"]["specific_muscles"].sort()
    assert response_dict == expected_response

 
def test_update_exercise(client_full_db: TestClient, session: Session):
    response: Response = client_full_db.get("/users/me/exercises")
    response_dict: dict[str, object] = response.json()
    exercise_uuid = str(response_dict["data"][0]["uuid"])
    new_data = {
            "name": "Dumbbell Chest Fly",
            "description": "Dumbbell Chest Fly Description",
            "workout_category": "Upper",
            "movement_category": "Fly",
            "equipment": "Dumbbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ],
            "image_url": None
            } 
    response = client_full_db.put(f"/users/me/exercises/{exercise_uuid}", json=new_data)
    response_dict = response.json()
    exercise_uuid = session.exec(select(Exercise).where(Exercise.uuid == UUID(response_dict["data"]["uuid"]))).first().uuid
    expected_response = {
        "data": {
            "uuid": str(exercise_uuid),
            "name": "Dumbbell Chest Fly",
            "description": "Dumbbell Chest Fly Description",
            "workout_category": "Upper",
            "movement_category": "Fly",
            "equipment": "Dumbbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ],
            "image_url": None
            },
        "detail": "Exercise updated successfully."
        }
    response_dict["data"]["specific_muscles"].sort()
    expected_response["data"]["specific_muscles"].sort()
    assert response_dict == expected_response

def test_patch_exercise(client_full_db: TestClient, session: Session):
    response: Response = client_full_db.get("/users/me/exercises")
    response_dict: dict[str, object] = response.json()
    exercise_uuid = str(session.exec(select(Exercise).where(Exercise.uuid == UUID(response_dict['data'][2]['uuid']))).first().uuid)
    new_data = {
            "name": "Dumbbell Incline Chest Fly",
            "description": "Dumbbell Incline Chest Fly Description",
            "major_muscle": "Chest"
            } 
    response = client_full_db.patch(f"/users/me/exercises/{exercise_uuid}", json=new_data)
    response_dict = response.json()
    for key, value in response_dict['data'].items():
        if isinstance(value, list):
            response_dict['data'][key].sort()
    expected_response = {
        "data": {
            "uuid": exercise_uuid,
            "name": "Dumbbell Incline Chest Fly",
            "description": "Dumbbell Incline Chest Fly Description",
            "workout_category": "Upper",
            "movement_category": "Press",
            "equipment": "Dumbbell",
            "major_muscle": "Chest",
            "specific_muscles": [
                "Middle Chest", "Triceps"
            ],
            "image_url": None
            },
        "detail": "Exercise patched successfully."
        }
    assert response.status_code == 200
    assert response_dict == expected_response 

def test_delete_exercise(client_full_db: TestClient, session: Session):
    response: Response = client_full_db.get("/users/me/exercises")
    response_dict: dict[str, object] = response.json()
    exercise_uuid: str = str(session.exec(select(Exercise).where(Exercise.uuid == UUID(response_dict['data'][1]['uuid']))).first().uuid)  
    response: Response = client_full_db.delete(f"/users/me/exercises/{exercise_uuid}")
    assert response.status_code == 204
