"""Train a simple Iris classifier and track the run with MLflow.

MLflow is optional: on a light install (e.g. Streamlit Community Cloud)
the model is still trained, just without experiment tracking.
"""
import os
from contextlib import nullcontext

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

try:
    import mlflow
    import mlflow.sklearn
except ImportError:
    mlflow = None

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", "100"))
MAX_DEPTH = int(os.getenv("MAX_DEPTH", "5"))
MIN_ACCURACY = float(os.getenv("MIN_ACCURACY", "0"))  # CI sets this as a quality gate


def main():
    if mlflow:
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
        mlflow.set_experiment("iris-classifier")

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    run = mlflow.start_run() if mlflow else nullcontext()
    with run:
        model = RandomForestClassifier(
            n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH, random_state=42
        )
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))

        if mlflow:
            mlflow.log_param("n_estimators", N_ESTIMATORS)
            mlflow.log_param("max_depth", MAX_DEPTH)
            mlflow.log_metric("accuracy", acc)
            mlflow.sklearn.log_model(model, "model")

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        print(f"Accuracy: {acc:.4f} | model saved to {MODEL_PATH}")

    if acc < MIN_ACCURACY:
        raise SystemExit(f"Quality gate failed: accuracy {acc:.4f} < {MIN_ACCURACY}")
    return acc


if __name__ == "__main__":
    main()
