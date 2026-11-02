# Terraform + Grafana

## Terraform (infrastructure as code for Kubernetes)
`terraform/` creates a namespace `mlops` + the iris-api Deployment + Service on your local kind cluster.
```bash
kind create cluster
kind load docker-image iris-api:latest
cd terraform
terraform init
terraform plan
terraform apply          # type yes
kubectl -n mlops get pods,svc
kubectl -n mlops port-forward svc/iris-api 8080:80
terraform destroy        # cleanup, type yes
```
Change replicas without touching YAML: `terraform apply -var="replicas=4"`.
CI runs `terraform init` + `terraform validate` on every push.

## Grafana + Prometheus (monitoring)
The API exposes `/metrics`. Prometheus scrapes it, Grafana shows the dashboard "Iris API Monitoring".
```bash
docker compose up -d --build
python scripts/generate_traffic.py 300
```
- API docs:    http://localhost:8000/docs
- Metrics:     http://localhost:8000/metrics
- Prometheus:  http://localhost:9090  (Status -> Targets: iris-api should be UP)
- Grafana:     http://localhost:3000  (login admin / admin, skip password change) -> Dashboards -> Iris API Monitoring

Stop: `docker compose down`
