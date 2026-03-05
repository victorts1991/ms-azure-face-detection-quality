# MS Azure Face Detection Quality 🛡️

![Status: Em Desenvolvimento](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge&logo=github)

Microserviço em FastAPI para validação de qualidade de capturas faciais utilizando **Azure AI Face API**, implantado em **Azure Kubernetes Service (AKS)** com infraestrutura e deploy 100% automatizados.

## 🚀 Objetivo
Validar se uma foto de rosto atende aos requisitos mínimos para reconhecimento facial (iluminação, acessórios, ângulo) antes de persistir a imagem no Azure Blob Storage.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.11+
* **Framework:** FastAPI
* **IA:** Azure AI Foundry (Face API)
* **Infra:** Azure Kubernetes Service (AKS) & Azure Container Registry (ACR)
* **Provisionamento:** Terraform (IaC)
* **CI/CD:** GitHub Actions
* **Storage:** Azure Blob Storage
* **Testes:** Pytest & Pytest-asyncio (QA Automatizado e Mocks)
* **SDKs:** Azure SDK for Python (Face & Storage Blob)
* **Containerização:** Docker

---

## 🗺️ Roadmap de Desenvolvimento

### 1. Infraestrutura como Código (Terraform)
- [x] Script de Bootstrap para Backend Remoto (Blob Storage para .tfstate).
- [x] Módulo de Serviços (Face API + Storage Account).
- [x] Módulo de Cluster (AKS + ACR + Role Assignment).
- [x] Provisionamento Automatizado via `terraform apply`.

### 2. Desenvolvimento do Microserviço
- [x] Setup do projeto FastAPI e dependências.
- [x] Implementação do Client da Face API (SDK Oficial).
- [x] Implementação do Upload para Blob Storage (Persistência).
- [x] Lógica de filtragem (Boné, Óculos de Sol, Ângulo e Qualidade).
- [x] Documentação Swagger/OpenAPI integrada.
- [x] Implementação de Testes Unitários Automatizados (Pytest).

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
Os seguintes valores são gerados pelo Terraform e configurados no arquivo `.env` (local) ou como *Secrets* (K8s):

* **FACE_API_ENDPOINT:** URL da API de IA.
* **FACE_API_KEY:** Chave de autenticação da Face API.
* **STORAGE_ACCOUNT_NAME:** Nome da conta de armazenamento.
* **STORAGE_CONTAINER_NAME:** Nome do container de destino (`validated-faces`).
* **AZURE_STORAGE_CONNECTION_STRING:** String de conexão completa para persistência de dados.

> **Dica:** Para extrair esses valores após o deploy da infra, utilize:
> `terraform output -raw AZURE_STORAGE_CONNECTION_STRING`

---

## 🔐 Configuração das Variáveis de Ambiente (.env)

Após o provisionamento da infraestrutura (Etapa 1), você deve configurar as credenciais no seu ambiente local em um arquivo chamado **.env**. 

### Criando o arquivo .env
Crie um arquivo chamado **.env** na raiz do projeto e preencha com os valores obtidos acima:

```env
FACE_API_ENDPOINT=valor_obtido_no_terraform
FACE_API_KEY=valor_obtido_no_terraform
AZURE_STORAGE_CONNECTION_STRING=valor_obtido_no_terraform
STORAGE_CONTAINER_NAME=validated-faces
```

## 🛠️ Comandos de Execução Local

Siga este fluxo no seu terminal para validar o microserviço:

```bash
# 1. Configurar o ambiente Python
python -m venv venv

# No Linux ou macOS
source venv/bin/activate
# No Windows (Prompt de Comando - CMD)
venv\Scripts\activate
# No Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

# 2. Executar a suíte de testes (QA Automatizado)
pytest -v

# 3. Subir a API localmente
uvicorn app.main:app --reload
```

## 🧪 Plano de Testes de Qualidade (QA)

O microserviço foi homologado e validado nos seguintes cenários:

* **Foto Padrão:** Status 200 OK (Aprovado e Salvo na Azure).
* **Uso de Boné:** Status 400 Bad Request (Bloqueado corretamente).
* **Óculos de Sol:** Status 400 Bad Request (Bloqueado corretamente).
* **Rosto de Perfil:** Status 400 Bad Request (Bloqueado por ângulo).
* **Baixa Iluminação:** Status 400 Bad Request (Bloqueado por exposição).
* **Óculos de Grau:** Status 200 OK (Permitido conforme regra de negócio).
* **Ausência de Rosto:** Status 400 Bad Request (Bloqueado por ângulo).

### ✅ Status da Etapa 1: Homologada via IaC
Infraestrutura provisionada, modularizada e versionada com sucesso.

### ✅ Status da Etapa 2: Concluída e Validada
O microserviço está filtrando imagens com precisão e integrando perfeitamente com o Storage Account da Azure.