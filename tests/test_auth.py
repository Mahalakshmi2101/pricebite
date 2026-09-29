import pytest
from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    """
    Test 1: User registration succeeds with 201 Created and does NOT leak password_hash.
    """
    response = client.post(
        "/auth/register",
        json={
            "name": "Karthik Raja",
            "email": "karthik@example.com",
            "password": "SecurePassword123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Karthik Raja"
    assert data["email"] == "karthik@example.com"
    assert data["role"] == "customer"
    assert "id" in data
    assert "created_at" in data
    # Critical security assertion: password_hash must never be exposed
    assert "password_hash" not in data
    assert "password" not in data


def test_register_duplicate_email(client: TestClient):
    """
    Test 2: Duplicate email registration returns 409 Conflict.
    """
    payload = {
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "password": "Password456!"
    }
    # First registration: succeeds
    res1 = client.post("/auth/register", json=payload)
    assert res1.status_code == 201

    # Second registration with identical email: rejected with 409 Conflict
    res2 = client.post("/auth/register", json=payload)
    assert res2.status_code == 409
    assert res2.json()["detail"] == "Email already registered"


def test_login_and_get_me_with_token(client: TestClient):
    """
    Test 3: Login generates valid JWT, and protected /auth/me returns authenticated user.
    """
    # 1. Register
    reg_payload = {
        "name": "Anand Kumar",
        "email": "anand@example.com",
        "password": "SuperSecretPass789!"
    }
    reg_res = client.post("/auth/register", json=reg_payload)
    assert reg_res.status_code == 201

    # 2. Login
    login_payload = {
        "email": "anand@example.com",
        "password": "SuperSecretPass789!"
    }
    login_res = client.post("/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    token = token_data["access_token"]

    # 3. Access protected /auth/me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["name"] == "Anand Kumar"
    assert me_data["email"] == "anand@example.com"
    assert me_data["role"] == "customer"
    assert "password_hash" not in me_data


def test_login_invalid_credentials_timing_and_enumeration(client: TestClient):
    """
    Test 4: Non-existent email and wrong password return identical 401 response.
    """
    # Register a user
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "valid@example.com", "password": "CorrectPassword1!"}
    )

    # Wrong password for existing email
    res_wrong_pw = client.post(
        "/auth/login",
        json={"email": "valid@example.com", "password": "WrongPassword!"}
    )
    assert res_wrong_pw.status_code == 401
    assert res_wrong_pw.json()["detail"] == "Invalid email or password"
    assert res_wrong_pw.headers.get("www-authenticate") == "Bearer"

    # Non-existent email
    res_no_user = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "AnyPassword!"}
    )
    assert res_no_user.status_code == 401
    # Must match EXACTLY to prevent user enumeration
    assert res_no_user.json()["detail"] == res_wrong_pw.json()["detail"]
    assert res_no_user.headers.get("www-authenticate") == "Bearer"
