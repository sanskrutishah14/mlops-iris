terraform {
  required_version = ">= 1.5.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.33"
    }
  }
}

provider "kubernetes" {
  config_path    = var.kubeconfig_path
  config_context = var.kube_context
}

resource "kubernetes_namespace" "mlops" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_deployment" "iris_api" {
  metadata {
    name      = "iris-api"
    namespace = kubernetes_namespace.mlops.metadata[0].name
    labels = {
      app = "iris-api"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "iris-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "iris-api"
        }
      }

      spec {
        container {
          name              = "iris-api"
          image             = var.image
          image_pull_policy = "IfNotPresent"

          port {
            container_port = 8000
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "iris_api" {
  metadata {
    name      = "iris-api"
    namespace = kubernetes_namespace.mlops.metadata[0].name
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "iris-api"
    }

    port {
      port        = 80
      target_port = 8000
    }
  }
}
