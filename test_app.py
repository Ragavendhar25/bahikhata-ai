import os
os.environ.setdefault("GROQ_API_KEY", "test-key")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app, get_db
from database import Base

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_home():
    assert client.get("/").status_code == 200

def test_balance():
    r = client.post("/customers", json={"name": "Ramesh", "phone": "9876543210"})
    cid = r.json()["id"]
    client.post("/purchase", json={"customer_id": cid, "item": "rice", "quantity": 2, "price": 60})
    client.post("/payment", json={"customer_id": cid, "amount": 100})
    b = client.get(f"/customers/{cid}/balance").json()
    assert b["balance_due"] == 20