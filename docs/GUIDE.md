# Step-by-step Guide (GitHub + Docker + Kubernetes + Streamlit)

## 1. Local setup & run
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
python src/train.py
flake8 .
pytest
mlflow ui          # open http://localhost:5000, see experiment "iris-classifier"
uvicorn src.app:app --reload
curl -X POST localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

## 2. Git basics
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git init
git add .
git commit -m "Initial commit: iris ML project"
git branch -M main
```

## 3. GitHub
Create an empty repo on github.com (no README), then:
```bash
git remote add origin https://github.com/<username>/mlops-project.git
git push -u origin main
```
Practice branching/PR workflow (good for your report):
```bash
git checkout -b feature/tune-model
# edit N_ESTIMATORS default in src/train.py
git add src/train.py
git commit -m "Tune n_estimators"
git push -u origin feature/tune-model
# open Pull Request on GitHub -> CI runs -> merge
git checkout main && git pull
git log --oneline --graph
```
Other useful commands: `git status`, `git diff`, `git stash`, `git merge`, `git rebase`, `git revert <sha>`, `git tag v1.0 && git push --tags`.

## 4. GitHub Actions (CI)
`ci.yml` runs on every push/PR: lint (flake8), train with MLflow + accuracy quality gate, pytest + coverage, Docker build + container smoke test + Trivy scan. Check the **Actions** tab. Full pipeline explanation, repo settings and release flow: see `docs/CICD.md`.

Run the same checks locally with `make lint` and `make test`.

## 5. MLflow
- Runs log to `./mlruns`. View: `mlflow ui`.
- Compare runs by changing hyperparameters:
  ```bash
  N_ESTIMATORS=50 MAX_DEPTH=3 python src/train.py
  N_ESTIMATORS=200 MAX_DEPTH=8 python src/train.py
  ```
  (Windows PowerShell: `$env:N_ESTIMATORS=50; python src/train.py`)
- Optional: model registry needs a DB backend: `mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts` then `export MLFLOW_TRACKING_URI=http://localhost:5000`.

## 6. Docker
```bash
docker build -t iris-api:latest .
docker run -d -p 8000:8000 --name iris iris-api:latest
curl localhost:8000/health
docker logs iris
docker stop iris && docker rm iris
```

## 7. Kubernetes locally first (kind or minikube)
```bash
# option A: minikube
minikube start
minikube image load iris-api:latest
# option B: kind
kind create cluster
kind load docker-image iris-api:latest

kubectl apply -f k8s/
kubectl get pods
kubectl get svc
kubectl port-forward svc/iris-api 8080:80
curl localhost:8080/health
kubectl scale deployment iris-api --replicas=3
kubectl logs deploy/iris-api
```

## 8. Automated CD with GitHub Actions (GHCR + Kubernetes)
`.github/workflows/cd.yml` runs after CI succeeds on `main`:
1. builds the Docker image and pushes it to **GitHub Container Registry** (`ghcr.io/<you>/iris-api:<sha>`)
2. creates a temporary Kubernetes cluster with **kind**
3. deploys `k8s/` manifests, waits for the rollout
4. smoke-tests `/health` and `/predict`

No secrets needed (it uses the built-in `GITHUB_TOKEN`). Check the **Actions** tab and the **Packages** section of your repo/profile.
Run it manually any time: Actions -> "CD" -> Run workflow.

## 9. Streamlit deployment (public URL)
1. Make sure everything is pushed to GitHub (the repo must be public, or grant Streamlit access to private repos).
2. Test locally first:
   ```bash
   streamlit run streamlit_app.py      # http://localhost:8501
   ```
3. Go to https://share.streamlit.io and sign in with GitHub.
4. Click **Create app** -> "Deploy a public app from GitHub":
   - Repository: `<username>/mlops-project`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. (Optional) Advanced settings -> choose Python 3.11 to match the Dockerfile.
6. Click **Deploy**. First start takes a few minutes (installs requirements, trains the model). You get a URL like `https://<app-name>.streamlit.app`.
7. Every `git push` to `main` auto-redeploys the app.

You can also run Streamlit in Docker:
```bash
docker run -p 8501:8501 iris-api:latest streamlit run streamlit_app.py
```


## Troubleshooting
- Pod `ImagePullBackOff` locally: load the image into the cluster (Step 7).
- Streamlit deploy fails on install: check the logs in "Manage app"; try Python 3.11 in Advanced settings.
- CD fails at "Log in to GHCR": check repo Settings -> Actions -> General -> Workflow permissions is "Read and write".
