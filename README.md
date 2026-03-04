# MS Azure Face Detection Quality 🛡️

![Status: Em Desenvolvimento](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge&logo=github)

Microserviço em FastAPI para validação de qualidade de capturas faciais utilizando **Azure AI Face API**, implantado em **Azure Kubernetes Service (AKS)** com infraestrutura e deploy 100% automatizados.

## 🚀 Objetivo
Validar se uma foto de rosto atende aos requisitos mínimos para reconhecimento facial (iluminação, acessórios, ângulo) antes de persistir a imagem no Azure Blob Storage.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Framework:** FastAPI
* **IA:** Azure AI Foundry (Face API)
* **Infra:** Azure Kubernetes Service (AKS) & Azure Container Registry (ACR)
* **Provisionamento:** Terraform (IaC)
* **CI/CD:** GitHub Actions
* **Storage:** Azure Blob Storage

---

## 🗺️ Roadmap de Desenvolvimento

### 1. Infraestrutura como Código (Terraform)
- [x] Script de Bootstrap para Backend Remoto (Blob Storage para .tfstate).
- [x] Módulo de Serviços (Face API + Storage Account).
- [x] Módulo de Cluster (AKS + ACR + Role Assignment).
- [x] Provisionamento Automatizado via `terraform apply`.

### 2. Desenvolvimento do Microserviço
- [ ] Setup do projeto FastAPI e dependências.
- [ ] Implementação do Client da Face API.
- [ ] Implementação do Upload para Blob Storage.
- [ ] Documentação Swagger/OpenAPI.

### 3. Containerização e Kubernetes
- [ ] Criação do Dockerfile (Multi-stage build).
- [ ] Manifestos K8s (Deployment, Service LoadBalancer).
- [ ] Configuração de Segredos (Secrets) no Cluster.

### 4. Automação Full CI/CD (GitHub Actions)
- [ ] Pipeline de **Integração Contínua (CI)**: Lint, Testes Unitários e Build/Push da imagem Docker para o ACR.
- [ ] Pipeline de **Entrega Contínua (CD)**: Atualização automática do Cluster AKS com a nova versão da imagem.
- [ ] Gerenciamento de Secrets do GitHub para autenticação na Azure via Service Principal.

---

## 🛠️ Guia de Configuração da Infraestrutura (Início Rápido)

Este guia detalha como subir toda a infraestrutura na Azure utilizando Terraform.

### 1. Pré-requisitos
* **Azure CLI** instalado e logado (`az login`).
* **Terraform** (v1.0+) instalado.
* **Docker Desktop** rodando.
* **Assinatura Azure** ativa.

### 2. Passo a Passo Inicial

#### A. Bootstrap (Preparação do Cofre)
O Terraform precisa de um lugar seguro para guardar o estado da sua infraestrutura. Execute o script de automação inicial:

```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

*Este script criará um Resource Group chamado `rg-terraform-state`. **Anote o nome da Storage Account gerada no final.***

#### B. Configuração do Backend
Abra o arquivo `terraform/main.tf` e atualize o bloco `backend "azurerm"` com o nome da Storage Account gerada:

```hcl
backend "azurerm" {
  resource_group_name  = "rg-terraform-state"
  storage_account_name = "ST_GERADA_AQUI"
  container_name       = "tfstate"
  key                  = "face-quality.terraform.tfstate"
}
```

#### C. Provisionamento (Deploy)
Agora, dispare a criação de todos os recursos:

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

### 3. Conectando ao Ambiente
Após o `apply` finalizar, configure seu terminal:

```bash
# 1. Obter credenciais do AKS
az aks get-credentials --resource-group rg-face-quality-prod --name facequality-aks

# 2. Login no Registro de Containers (ACR)
az acr login --name facequalityregistryb814a9

# 3. Validar conexão com o cluster
kubectl get nodes
```

---

## 🔑 Variáveis de Ambiente Críticas
Os seguintes valores serão gerados pelo Terraform e devem ser usados na API:
* **FACE_API_ENDPOINT:** Obtido via `terraform output FACE_API_ENDPOINT`
* **FACE_API_KEY:** Obtido via `terraform output FACE_API_KEY`
* **STORAGE_ACCOUNT_NAME:** Obtido via `terraform output STORAGE_ACCOUNT_NAME`

---

### ✅ Status da Etapa 1: Homologada via IaC
Infraestrutura provisionada, modularizada e versionada com sucesso.