import pytest
from fastapi.testclient import TestClient
from httpx import Response
from db import Session
from sqlmodel import select
from models.relationship_merge import Exercise, User

@pytest.fixture
def client_full_db_with_workout_exercises(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username":"user", "password":"user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    workout_exercises_data = [
        {
            "planned_sets": 3,
            "planned_reps": 10,
            "planned_resistance_weight": 80,
            "exercise_uuid": str(session.exec(select(Exercise).where(Exercise.name == "Dumbbell Chest Press")).first().uuid)
        },
        {
            "planned_sets": 3,
            "planned_reps": 8,
            "planned_resistance_weight": 160,
            "exercise_uuid": str(session.exec(select(Exercise).where(Exercise.name == "Barbell Chest Press")).first().uuid)
        },
        {
            "planned_sets": 3,
            "planned_reps": 6,
            "planned_resistance_weight": 40,
            "exercise_uuid": str(session.exec(select(Exercise).where(Exercise.name == "Dumbbell Chest Fly")).first().uuid)
        }
        
    ] 
    for workout_exercise in workout_exercises_data:
        client_full_db.post(f"/users/me/workout-exercises", json=workout_exercise)
    yield client_full_db

def test_get_empty_workout_exercises(client_login: TestClient):
    client = client_login("user", "user")
    response: Response = client.get(f"/users/me/workout-exercises")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["data"] == []
    assert response_dict["detail"] == "0 workout exercises fetched successfully."

def test_get_workout_exercises(client_full_db_with_workout_exercises: TestClient):
    response = client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["data"] == [
        {
            'exercise': {
                'uuid': response_dict['data'][0]['exercise']['uuid'],
                'name': 'Dumbbell Chest Press',
                'description': 'Dumbbell Chest Press Description',
                'workout_category': 'Upper',
                'movement_category': 'Press',
                'equipment': 'Dumbbell',
                'major_muscle': 'Chest',
                'specific_muscles': ['Middle Chest', 'Triceps'],
                "image_url": None
            },
            'uuid': response_dict['data'][0]['uuid'],
            'planned_sets': 3,
            'planned_reps': 10,
            'planned_resistance_weight': 80.0,
            'exercise_order': None
        },
        {
            'exercise': {
                'uuid': response_dict['data'][1]['exercise']['uuid'],
                'name': 'Barbell Chest Press',
                'description': 'Barbell Chest Press Description',
                'workout_category': 'Upper',
                'movement_category': 'Press',
                'equipment': 'Barbell',
                'major_muscle': 'Chest',
                'specific_muscles': ['Middle Chest', 'Triceps'],
                "image_url": None
            },
            'uuid': response_dict['data'][1]['uuid'],
            'planned_sets': 3,
            'planned_reps': 8,
            'planned_resistance_weight': 160.0,
            'exercise_order': None
        },
        {
            'exercise': {
                'uuid': response_dict['data'][2]['exercise']['uuid'],
                'name': 'Dumbbell Chest Fly',
                'description': 'Dumbbell Chest Fly Description',
                'workout_category': 'Upper',
                'movement_category': 'Fly',
                'equipment': 'Dumbbell',
                'major_muscle': 'Chest',
                'specific_muscles': ['Middle Chest', 'Triceps'],
                "image_url": None
            },
            'uuid': response_dict['data'][2]['uuid'],
            'planned_sets': 3,
            'planned_reps': 6,
            'planned_resistance_weight': 40.0,
            'exercise_order': None
        },
    ]
    assert response_dict["detail"] == f"{len(response_dict['data'])} workout exercises fetched successfully."

def test_get_workout_exercise(client_full_db_with_workout_exercises: TestClient):
    response = client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises")
    response_dict = response.json()
    workout_exercise_uuid = response_dict["data"][0]["uuid"]
    response = client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises/{workout_exercise_uuid}")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["data"] =={
            'exercise': {
                'uuid': response_dict['data']['exercise']['uuid'],
                'name': 'Dumbbell Chest Press',
                'description': 'Dumbbell Chest Press Description',
                'workout_category': 'Upper',
                'movement_category': 'Press',
                'equipment': 'Dumbbell',
                'major_muscle': 'Chest',
                'specific_muscles': ['Middle Chest', 'Triceps'],
                "image_url": None
            },
            'uuid': response_dict['data']['uuid'],
            'planned_sets': 3,
            'planned_reps': 10,
            'planned_resistance_weight': 80.0,
            'exercise_order': None
            }

def test_post_workout_exercise(client_full_db_with_workout_exercises: TestClient, session: Session):
    workout_exercise_data = {
        "planned_sets": 3,
        "planned_reps": 8,
        "planned_resistance_weight": 30,
        "exercise_uuid": str(session.exec(select(Exercise).where(Exercise.name == "Dumbbell Chest Fly")).first().uuid)
    }
    response = client_full_db_with_workout_exercises.post(f"/users/me/workout-exercises", json=workout_exercise_data)
    response_dict = response.json()
    assert response.status_code == 201
    assert response_dict["data"] == {
        'exercise': {
            'uuid': response_dict['data']['exercise']['uuid'],
            'name': 'Dumbbell Chest Fly',
            'description': 'Dumbbell Chest Fly Description',
            'workout_category': 'Upper',
            'movement_category': 'Fly',
            'equipment': 'Dumbbell',
            'major_muscle': 'Chest',
            'specific_muscles': ['Middle Chest', 'Triceps'],
            "image_url": None
        },
        'uuid': response_dict['data']['uuid'],
        'planned_sets': 3,
        'planned_reps': 8,
        'planned_resistance_weight': 30.0,
        'exercise_order': None
    }
    assert response_dict["detail"] == "Workout Exercise added successfully." 
    assert len(client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises").json()["data"]) == 4

def test_put_workout_exercise(client_full_db_with_workout_exercises: TestClient, session: Session):
    response = client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises")
    response_dict = response.json()
    workout_exercise_uuid = response_dict["data"][0]["uuid"]
    updated_workout_exercise_data = {
        "planned_sets": 3,
        "planned_reps": 8,
        "planned_resistance_weight": 30,
        "exercise_uuid": str(session.exec(select(Exercise).where(Exercise.name == "Dumbbell Chest Fly")).first().uuid)
    }
    response = client_full_db_with_workout_exercises.put(f"/users/me/workout-exercises/{workout_exercise_uuid}", json=updated_workout_exercise_data)
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["data"] == {
        'exercise': {
            'uuid': response_dict['data']['exercise']['uuid'],
            'name': 'Dumbbell Chest Fly',
            'description': 'Dumbbell Chest Fly Description',
            'workout_category': 'Upper',
            'movement_category': 'Fly',
            'equipment': 'Dumbbell',
            'major_muscle': 'Chest',
            'specific_muscles': ['Middle Chest', 'Triceps'],
            "image_url": None
        },
        'uuid': response_dict['data']['uuid'],
        'planned_sets': 3,
        'planned_reps': 8,
        'planned_resistance_weight': 30.0,
        'exercise_order': None
    }
    assert response_dict["detail"] == "Workout Exercise updated successfully." 
    assert len(client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises").json()["data"]) == 3

def test_patch_workout_exercise(client_full_db_with_workout_exercises: TestClient, session: Session):
    response = client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises")
    response_dict = response.json()
    workout_exercise_uuid = response_dict["data"][0]["uuid"]
    updated_workout_exercise_data = {
        "planned_sets": 3,
        "planned_reps": 8
    }
    response = client_full_db_with_workout_exercises.patch(f"/users/me/workout-exercises/{workout_exercise_uuid}", json=updated_workout_exercise_data)
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["data"] == {
        'exercise': {
            'uuid': response_dict['data']['exercise']['uuid'],
            'name': 'Dumbbell Chest Press',
            'description': 'Dumbbell Chest Press Description',
            'workout_category': 'Upper',
            'movement_category': 'Press',
            'equipment': 'Dumbbell',
            'major_muscle': 'Chest',
            'specific_muscles': ['Middle Chest', 'Triceps'],
            "image_url": None
        },
        'uuid': response_dict['data']['uuid'],
        'planned_sets': 3,
        'planned_reps': 8,
        'planned_resistance_weight': 80.0,
        'exercise_order': None
    }
    assert response_dict["detail"] == "Workout Exercise updated successfully." 
    assert len(client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises").json()["data"]) == 3

def test_delete_workout_exercise(client_full_db_with_workout_exercises: TestClient):
    response = client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises")
    response_dict = response.json()
    workout_exercise_uuid = response_dict["data"][0]["uuid"]
    response = client_full_db_with_workout_exercises.delete(f"/users/me/workout-exercises/{workout_exercise_uuid}")
    assert response.status_code == 204
    assert len(client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises").json()["data"]) == 2
    assert client_full_db_with_workout_exercises.get(f"/users/me/workout-exercises/{workout_exercise_uuid}").status_code == 404