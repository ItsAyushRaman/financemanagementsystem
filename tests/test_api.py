from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def wipe_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "admin", "password": "password", "role": "Admin"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "admin"
    assert data["role"] == "Admin"
    assert "id" in data

def test_login_and_create_transaction():
    client.post(
        "/api/v1/auth/register",
        json={"username": "user", "password": "password", "role": "Admin"}
    )
    
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user", "password": "password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    tx_resp = client.post(
        "/api/v1/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={"amount": 100.5, "type": "income", "category": "Salary"}
    )
    assert tx_resp.status_code == 200, tx_resp.text
    tx_data = tx_resp.json()
    assert tx_data["amount"] == 100.5
    assert tx_data["type"] == "income"
    assert tx_data["category"] == "Salary"

def test_get_summary():
    client.post(
        "/api/v1/auth/register",
        json={"username": "user2", "password": "password", "role": "Admin"}
    )
    
    token = client.post(
        "/api/v1/auth/login",
        data={"username": "user2", "password": "password"}
    ).json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/v1/transactions/", headers=headers, json={"amount": 1000, "type": "income", "category": "Salary"})
    client.post("/api/v1/transactions/", headers=headers, json={"amount": 200, "type": "expense", "category": "Rent"})
    
    resp = client.get("/api/v1/transactions/summary", headers=headers)
    assert resp.status_code == 200
    summary = resp.json()
    assert summary["total_income"] == 1000.0
    assert summary["total_expense"] == 200.0
    assert summary["current_balance"] == 800.0
    assert "Salary" in summary["category_breakdown"]
    assert "Rent" in summary["category_breakdown"]
