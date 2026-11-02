"""FastAPI service that serves the trained model (with Prometheus metrics)."""
import os

import joblib
from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
CLASSES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris Classifier API")
model = joblib.load(MODEL_PATH)

PREDICTIONS = Counter("iris_predictions", "Predictions made, by species", ["species"])
Instrumentator().instrument(app).expose(app)  # adds GET /metrics


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: IrisInput):
    features = [[data.sepal_length, data.sepal_width,
                 data.petal_length, data.petal_width]]
    idx = int(model.predict(features)[0])
    PREDICTIONS.labels(species=CLASSES[idx]).inc()
    return {"prediction": CLASSES[idx], "class_index": idx}
