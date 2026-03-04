# Instância da Face API
resource "azurerm_cognitive_account" "face" {
  name                = "${var.prefix}-ai-face"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "Face"
  sku_name            = "S0"
}

# Storage Account para fotos aprovadas
resource "azurerm_storage_account" "st" {
  name                     = "${var.prefix}storage${var.suffix}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Container de Blobs
resource "azurerm_storage_container" "photos" {
  name                  = "validated-faces"
  storage_account_name  = azurerm_storage_account.st.name
  container_access_type = "private"
}

# Outputs para o módulo raiz ler
output "face_endpoint" { value = azurerm_cognitive_account.face.endpoint }
output "face_key"      { value = azurerm_cognitive_account.face.primary_access_key }
output "storage_account_name" { value = azurerm_storage_account.st.name }