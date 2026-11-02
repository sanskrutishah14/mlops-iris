output "namespace" {
  value = kubernetes_namespace.mlops.metadata[0].name
}

output "deployment" {
  value = kubernetes_deployment.iris_api.metadata[0].name
}

output "port_forward_command" {
  value = "kubectl -n ${var.namespace} port-forward svc/iris-api 8080:80"
}
