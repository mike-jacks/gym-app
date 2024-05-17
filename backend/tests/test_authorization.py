import pytest
from uuid import UUID
from fastapi.testclient import TestClient
from httpx import Response
from db import Session
from sqlmodel import select

def test_register(client: TestClient):
    response: Response = client.post("/users/register", json={
        "username": "test",
        "password": "test",
        "first_name": "Test",
        "last_name": "Test",
        "birthday": "2024-01-01",
        "body_weight": 100,
        "height": 70,
        "gender": "male",
        "hashed_password": "test"
    })
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 201
    assert response_dict['data']["username"] == "test"
    assert response_dict['data']["first_name"] == "Test"
    assert response_dict['data']["last_name"] == "Test"
    assert response_dict['data']["birthday"] == "2024-01-01"
    assert response_dict['data']["body_weight"] == 100.0
    assert response_dict['data']["height"] == 70.0
    assert response_dict['data']['roles'] == ["User"]


def test_login(client: TestClient):
    response: Response = client.post("/users/login", data={"username": "user", "password": "user"})
    response_dict: dict[str, object] = response.json()
    assert response.status_code == 200
    assert "access_token" in response_dict
    assert "token_type" in response_dict
    assert response_dict["token_type"] == "bearer"