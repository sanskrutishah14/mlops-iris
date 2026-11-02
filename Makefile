.PHONY: install lint train test mlflow api ui docker k8s clean

install:
	pip install -r requirements-dev.txt
lint:
	flake8 .
train:
	python src/train.py
test:
	pytest --cov=src
mlflow:
	mlflow ui
api:
	uvicorn src.app:app --reload
ui:
	streamlit run streamlit_app.py
docker:
	docker build -t iris-api:latest .
k8s:
	kubectl apply -f k8s/
clean:
	rm -rf mlruns models/*.joblib .pytest_cache .coverage coverage.xml
