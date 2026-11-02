variable "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "kube_context" {
  description = "kubectl context to deploy to (kind cluster default)"
  type        = string
  default     = "kind-kind"
}

variable "namespace" {
  description = "Kubernetes namespace to create"
  type        = string
  default     = "mlops"
}

variable "image" {
  description = "Container image to deploy"
  type        = string
  default     = "iris-api:latest"
}

variable "replicas" {
  description = "Number of pod replicas"
  type        = number
  default     = 2
}
