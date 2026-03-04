# Registro de Containers (Docker)
resource "azurerm_container_registry" "acr" {
  name                = "${var.prefix}registry${var.suffix}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}

# Cluster AKS
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${var.prefix}-aks"
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "${var.prefix}k8s"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2ds_v5"
    zones      = []
  }

  identity {
    type = "SystemAssigned"
  }
}

# Role Assignment: Permite o AKS puxar imagens do ACR sem senha
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}

# Output para o módulo raiz ler
output "acr_login_server" { value = azurerm_container_registry.acr.login_server }