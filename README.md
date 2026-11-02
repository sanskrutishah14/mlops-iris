# Iris MLOps Project

Simple Iris classifier used to practice: Git/GitHub, GitHub Actions, MLflow, Docker, Kubernetes (kind), GHCR, Streamlit Community Cloud.

```
src/train.py    -> trains model, logs params/metrics to MLflow
src/app.py      -> FastAPI: GET /health, POST /predict
streamlit_app.py -> Streamlit UI (deploy on Streamlit Community Cloud)
tests/          -> pytest
Dockerfile      -> builds image (trains model at build time)
k8s/            -> Deployment + Service
.github/workflows/ci.yml, cd.yml
docs/GUIDE.md   -> step-by-step commands for everything
docs/CICD.md    -> CI/CD pipeline explained
.github/        -> ci.yml, cd.yml, release.yml, dependabot, PR template
Makefile        -> make lint / test / train / docker / ui
```

Quick start:
```
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python src/train.py
mlflow ui                      # http://localhost:5000
uvicorn src.app:app --reload   # http://localhost:8000/docs
```
Full walkthrough: see `docs/GUIDE.md`.
