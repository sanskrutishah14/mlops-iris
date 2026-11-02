"""FastAPI service that serves the trained model."""
import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
CLASSES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris Classifier API")
model = joblib.load(MODEL_PATH)


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
    return {"prediction": CLASSES[idx], "class_index": idx}
