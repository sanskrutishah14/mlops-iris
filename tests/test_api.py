from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_predict_setosa():
    r = client.post("/predict", json={
        "sepal_length": 5.1, "sepal_width": 3.5,
        "petal_length": 1.4, "petal_width": 0.2})
    assert r.status_code == 200
    assert r.json()["prediction"] == "setosa"


def test_predict_validation_error():
    r = client.post("/predict", json={"sepal_length": "abc"})
    assert r.status_code == 422


def test_metrics_endpoint():
    client.post("/predict", json={
        "sepal_length": 5.1, "sepal_width": 3.5,
        "petal_length": 1.4, "petal_width": 0.2})
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "iris_predictions_total" in r.text
    assert "http_requests_total" in r.text
