from __future__ import annotations

from typing import Dict, List

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from src.main import app, fake_users_db


@pytest.fixture(autouse=True)
def clear_fake_db() -> None:
    """
    Limpia la "DB" en memoria antes de cada test para evitar
    dependencia entre tests.
    """
    fake_users_db.clear()
    return None


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app=app)


def test_root_returns_hello_world(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
    return None


def test_create_user_returns_201_and_user_payload(client: TestClient) -> None:
    payload: Dict[str, str] = {"name": "Daniel", "email": "daniel@gmail.com"}
    response = client.post(url="/users", json=payload)
    assert response.status_code == 201
    data: Dict[str, object] = response.json()

    assert "id" in data
    assert data["name"] == "Daniel"
    assert data["email"] == "daniel@gmail.com"
    return None


def test_get_users_returns_empty_list_initially(client: TestClient) -> None:
    response: Response = client.get(url="/users")
    assert response.status_code == 200
    assert response.json() == []
    return None


def test_get_users_returns_list_after_create(client: TestClient) -> None:
    payload: Dict[str, str] = {"name": "Daniel", "email": "daniel@gmail.com"}
    create_res: Response = client.post(url="/users", json=payload)
    assert create_res.status_code == 201

    response = client.get("/users")
    assert response.status_code == 200

    users: List[Dict[str, object]] = response.json()
    assert len(users) == 1
    assert users[0].get("name") == "Daniel"
    assert users[0].get("email") == "daniel@gmail.com"
    return None


def test_get_user_by_id_returns_200(client: TestClient) -> None:
    payload: Dict[str, str] = {"name": "Daniel", "email": "daniel@gmail.com"}
    create_res: Response = client.post(url="/users", json=payload)
    user_id: str = create_res.json()["id"]

    response: Response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json().get("id") == user_id
    assert response.json().get("name") == "Daniel"
    assert response.json().get("email") == "daniel@gmail.com"
    return None


def test_get_user_by_id_returns_404_when_missing(client: TestClient) -> None:
    response: Response = client.get("/users/non-existent-id")
    assert response.status_code == 404
    assert response.json() == dict(detail="User not found")
    return None


def test_update_user_returns_200_and_updates_fields(client: TestClient) -> None:
    payload: Dict[str, str] = {"name": "Daniel", "email": "daniel@gmail.com"}
    create_res: Response = client.post(url="/users", json=payload)
    user_id: str = create_res.json()["id"]

    update_payload: Dict[str, str] = {"name": "Dani Updated", "email": "dani@new.com"}
    response: Response = client.put(url=f"/users/{user_id}", json=update_payload)

    assert response.status_code == 200
    data: Dict[str, object] = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Dani Updated"
    assert data["email"] == "dani@new.com"


def test_update_user_partial_updates_only_one_field(client: TestClient) -> None:
    payload: Dict[str, str] = {"name": "Daniel", "email": "daniel@gmail.com"}
    create_res: Response = client.post(url="/users", json=payload)
    user_id: str = create_res.json()["id"]

    update_payload: Dict[str, str] = {"name": "Benjamin"}
    response: Response = client.put(url=f"/users/{user_id}", json=update_payload)

    assert response.status_code == 200
    data: Dict[str, object] = response.json()

    assert data["name"] == "Benjamin"
    assert data["email"] == "daniel@gmail.com"
    return None


def test_update_user_returns_404_when_missing(client: TestClient) -> None:
    update_payload: Dict[str, str] = {"name": "Zeus"}
    response: Response = client.put(url="/users/non-existent-id", json=update_payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    return None


def test_delete_user_returns_204_and_user_is_gone(client: TestClient) -> None:
    payload: Dict[str, str] = {"name": "Daniel", "email": "daniel@gmail.com"}
    create_res: Response = client.post(url="/users", json=payload)
    user_id: str = create_res.json()["id"]

    delete_res: Response = client.delete(url=f"/users/{user_id}")
    assert delete_res.status_code == 204
    assert delete_res.content == b""

    # Confirmar Que Ya No Existe el Usuario
    get_res: Response = client.get(f"/users/{user_id}")
    assert get_res.status_code == 404
    assert get_res.json() == {"detail": "User not found"}
    return None


def test_delete_user_returns_404_when_missing(client: TestClient) -> None:
    response: Response = client.delete(url="/users/non-existent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    return None