from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "telecom-telemetry-dashboard"}

def test_ingest_telemetry_normal():
    payload = {
        "device_id": "router-TEST-01",
        "latency_ms": 35.5,
        "packet_loss_percent": 0.5,
        "signal_strength_dbm": -60,
        "status": "ACTIVE"
    }
    response = client.post("/telemetry", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == "router-TEST-01"
    assert data["alert_triggered"] is False

def test_ingest_telemetry_alert():
    payload = {
        "device_id": "router-TEST-02",
        "latency_ms": 150.0,
        "packet_loss_percent": 1.0,
        "signal_strength_dbm": -75,
        "status": "WARNING"
    }
    response = client.post("/telemetry", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["alert_triggered"] is True
    assert "High latency detected" in data["reason"]