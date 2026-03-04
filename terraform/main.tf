terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stfacequalitytfb814a9"
    container_name       = "tfstate"
    key                  = "face-quality.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# Grupo de Recursos Principal
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# Chamada do Módulo de IA e Storage
module "services" {
  source              = "./modules/services"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  prefix              = var.prefix
  suffix              = var.suffix
}

# Chamada do Módulo de Kubernetes e Registro
module "cluster" {
  source              = "./modules/cluster"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  prefix              = var.prefix
  suffix              = var.suffix
}