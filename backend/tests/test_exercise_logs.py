from uuid import UUID
from fastapi.testclient import TestClient
from httpx import Response
from db import Session
from sqlmodel import select
from models.relationship_merge import ExerciseLog, Exercise, User

def test_empty_get_exercise_logs(client_login: TestClient):
    client: TestClient = client_login("user", "user")
    response: Response = client.get(f"/users/me/exercise_logs")
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 200
    assert response_dict == {
        "data": [],
        "detail": "Exercise Logs fetched successfully."
        }

def test_post_exercise_log(client_full_db: TestClient):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    exercise_uuid: str = client_full_db.get("/users/me/exercises").json()["data"][0]["uuid"]
    exercise_log_data = {
        "datetime_completed": "2022-01-01T12:00:00",
        "exercise_uuid": exercise_uuid,
        "reps": 10,
        "weight": 145.0
        }
    response: Response = client_full_db.post(f"/users/me/exercise_logs", json=exercise_log_data)
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 201
    assert response_dict == {
        "data": {
            "datetime_completed": "2022-01-01T12:00:00",
            "exercise": {
                "description": "Barbell Chest Press Description",
                "equipment": "Barbell",
                "major_muscle": "Chest",
                "movement_category": "Press",
                "name": "Barbell Chest Press",
                "specific_muscles": [
                    "Middle Chest",
                    "Triceps"
                    ],
                "uuid": exercise_uuid,
                "workout_category": "Upper",
                "image_url": None
                },
            "reps": 10,
            "uuid": response_dict["data"]["uuid"],
            "weight": 145.0
            },
        "detail": "Exercise log created successfully."
        }

def test_put_exercise_log(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    exercise_uuid: str = client_full_db.get("/users/me/exercises").json()["data"][0]["uuid"]
    exercise_log_data: dict[str,object] = {
        "datetime_completed": "2022-01-01T12:00:00",
        "exercise_uuid": exercise_uuid,
        "reps": 10,
        "weight": 145.0
        }
    response: Response = client_full_db.post(f"/users/me/exercise_logs", json=exercise_log_data)
    response_dict: dict[str, object] = response.json() 
    response: Response = client_full_db.get(f"/users/me/exercise_logs")
    response_dict: dict[str, object] = response.json()
    exercise_log_uuid = response_dict["data"][0]["uuid"]
    exercise_uuid = client_full_db.get(f"/users/me/exercise_logs/{exercise_log_uuid}").json()["data"]["exercise"]["uuid"]
    exercise_log_data = {
        "datetime_completed": "2025-01-01T12:00:00",
        "exercise_uuid": exercise_uuid,
        "reps": 200,
        "weight": 125.0
        }
    response: Response = client_full_db.put(f"/users/me/exercise_logs/{exercise_log_uuid}", json=exercise_log_data)
    response_dict = response.json()
    exercise_log_uuid = UUID(exercise_log_uuid)
    exercise_log_uuid, exercise_id, user_id = map(str, session.exec(select(ExerciseLog.uuid, ExerciseLog.exercise_id, ExerciseLog.user_id).where(ExerciseLog.uuid == exercise_log_uuid)).first())
    assert response.status_code == 200
    assert response_dict == {
        "data": {
            "datetime_completed": "2025-01-01T12:00:00",
            "exercise": {
                "description": "Barbell Chest Press Description",
                "equipment": "Barbell",
                "major_muscle": "Chest",
                "movement_category": "Press",
                "name": "Barbell Chest Press",
                "specific_muscles": [
                    "Middle Chest",
                    "Triceps"
                    ],
                "uuid": exercise_uuid,
                "workout_category": "Upper",
                "image_url": None
                },
            "reps": 200,
            "uuid": exercise_log_uuid,
            "weight": 125.0
            },
        "detail": "Exercise log updated successfully."
        }

def test_patch_exercise_log(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    exercise_uuid = client_full_db.get("/users/me/exercises").json()["data"][0]["uuid"]
    exercise_log_data = {
        "datetime_completed": "2022-01-01T12:00:00",
        "exercise_uuid": exercise_uuid,
        "reps": 10,
        "weight": 145.0
        }
    response = client_full_db.post(f"/users/me/exercise_logs", json=exercise_log_data)
    response_dict = response.json()
    exercise_log_uuid = client_full_db.get(f"/users/me/exercise_logs").json()["data"][0]["uuid"]
    exercise_uuid = client_full_db.get(f"/users/me/exercise_logs/{exercise_log_uuid}").json()["data"]["exercise"]["uuid"]
    exercise_log_data = {
        "reps": 20,
        "weight": 125.0
        }
    response: Response = client_full_db.patch(f"/users/me/exercise_logs/{exercise_log_uuid}", json=exercise_log_data)
    response_dict = response.json()
    exercise_log_uuid = UUID(exercise_log_uuid)
    exercise_log_uuid, exercise_id, user_id = map(str, session.exec(select(ExerciseLog.uuid, ExerciseLog.exercise_id, ExerciseLog.user_id).where(ExerciseLog.uuid == exercise_log_uuid)).first())
    assert response.status_code == 200
    assert response_dict == {
        "data": {
            "datetime_completed": "2022-01-01T12:00:00",
            "exercise": {
                "description": "Barbell Chest Press Description",
                "equipment": "Barbell",
                "major_muscle": "Chest",
                "movement_category": "Press",
                "name": "Barbell Chest Press",
                "specific_muscles": [
                    "Middle Chest",
                    "Triceps"
                    ],
                "uuid": str(session.exec(select(Exercise).where(Exercise.id == exercise_id)).first().uuid),
                "workout_category": "Upper",
                "image_url": None 
                },
            "reps": 20,
            "uuid": exercise_log_uuid,
            "weight": 125.0
            },
        "detail": "Exercise log updated successfully."
        }

def test_delete_exercise(client_full_db: TestClient, session: Session):
    response = client_full_db.post("/users/login", data={"username": "user", "password": "user"})
    client_full_db.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    exercise_uuid = client_full_db.get("/users/me/exercises").json()["data"][0]["uuid"]
    exercise_log_data = {
        "datetime_completed": "2022-01-01T12:00:00",
        "exercise_uuid": exercise_uuid,
        "reps": 10,
        "weight": 145.0
        }
    response: Response = client_full_db.post(f"/users/me/exercise_logs", json=exercise_log_data)
    exercise_log_uuid = client_full_db.get(f"/users/me/exercise_logs").json()["data"][0]["uuid"]
    assert session.exec(select(ExerciseLog).where(ExerciseLog.uuid == UUID(exercise_log_uuid))).first() != None
    response = client_full_db.delete(f"/users/me/exercise_logs/{exercise_log_uuid}")
    assert response.status_code == 204
    assert session.exec(select(ExerciseLog).where(ExerciseLog.uuid == UUID(exercise_log_uuid))).first() == None
    response: Response = client_full_db.delete(f"/users/me/exercise_logs/{exercise_log_uuid}")
    response_dict = response.json()
    assert response.status_code == 404
    assert response_dict == {
        "detail": f"Exercise Log UUID: {exercise_log_uuid} not found."
        }