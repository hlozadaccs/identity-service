import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_register_success(async_client: AsyncClient):
    payload = {"email": "test@example.com", "password": "Secret123!"}
    r = await async_client.post("/auth/register", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "test@example.com"
    assert "user_id" in data


@pytest.mark.anyio
async def test_register_duplicate_email(async_client: AsyncClient):
    payload = {"email": "dup@example.com", "password": "Secret123!"}
    r1 = await async_client.post("/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = await async_client.post("/auth/register", json=payload)
    assert r2.status_code == 400


@pytest.mark.anyio
async def test_login_success(async_client: AsyncClient):
    await async_client.post(
        "/auth/register",
        json={"email": "login@test.com", "password": "Secret123!"},
    )

    r = await async_client.post(
        "/auth/login",
        json={"email": "login@test.com", "password": "Secret123!"},
    )

    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_invalid_password(async_client: AsyncClient):
    await async_client.post(
        "/auth/register",
        json={"email": "bad@test.com", "password": "Secret123!"},
    )

    r = await async_client.post(
        "/auth/login",
        json={"email": "bad@test.com", "password": "wrong"},
    )

    assert r.status_code == 401