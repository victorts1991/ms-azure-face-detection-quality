# MS Azure Face Detection Quality 🛡️

![Status: Concluído](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen?style=for-the-badge&logo=github)
![Kubernetes](https://img.shields.io/badge/Kubernetes-AKS-blue?style=for-the-badge&logo=kubernetes)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?style=for-the-badge&logo=terraform)

Microserviço em FastAPI para validação de qualidade de capturas faciais utilizando **Azure AI Face API**, implantado em **Azure Kubernetes Service (AKS)** com infraestrutura e deploy 100% automatizados.

## 🚀 Objetivo
O projeto visa garantir que fotos de rostos enviadas para sistemas de identidade atendam aos requisitos mínimos de qualidade (iluminação adequada, ausência de acessórios como óculos de sol ou bonés e ângulo frontal) antes de serem persistidas no **Azure Blob Storage**.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.11+
* **Framework:** FastAPI
* **IA:** Azure AI Foundry (Azure AI Face API)
* **Infra:** Azure Kubernetes Service (AKS) & Azure Container Registry (ACR)
* **Provisionamento:** Terraform (IaC)
* **CI/CD:** GitHub Actions (Estratégia de Artifact Sharing)
* **Storage:** Azure Blob Storage
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
- [X] Criação do Dockerfile (Multi-stage build).
- [X] Manifestos K8s (Deployment, Service LoadBalancer).
- [X] Configuração de Segredos (Secrets) no Cluster.

### 4. Automação Full CI/CD (GitHub Actions)
- [x] **Integração Contínua (CI):** Linting, execução de testes unitários com mocks e Build/Push multi-estágio para o ACR.
- [x] **Entrega Contínua (CD):** Deploy automatizado no AKS com estratégia de atualização de imagem via Rollout.
- [x] **Auto-Discovery de Infraestrutura:** Scripting para descoberta dinâmica de endpoints e chaves pós-provisionamento.
- [x] **Gestão de Segredos Resiliente:** Implementação de Artifact Sharing para garantir a integridade de Connection Strings complexas.
- [x] **Deploy Idempotente:** Sincronização de Secrets do Kubernetes utilizando `dry-run` e `apply` para evitar conflitos de recursos.

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

Após o `apply` finalizar, configure seu terminal capturando os nomes gerados. Como o Resource Group segue o padrão do seu prefixo, usaremos a variável diretamente:

```bash
# 1. Definir o prefixo usado (ex: facequality)
PREFIX="seu_prefixo_aqui"
RG_NAME="rg-${PREFIX}-prod"

# 2. Obter credenciais do AKS (usando o output fixo do seu terraform)
# Caso não esteja na raiz do projeto, retorne com "cd .."
AZ_AKS=$(terraform -chdir=terraform output -raw aks_cluster_name)
az aks get-credentials --resource-group "$RG_NAME" --name "$AZ_AKS" --overwrite-existing

# 3. Login no Registro de Containers (usando seu output acr_name)
AZ_ACR=$(terraform -chdir=terraform output -raw acr_name)
az acr login --name "$AZ_ACR"

# 4. Validar conexão com o cluster
kubectl get nodes
```

---

## 🔑 Variáveis de Ambiente Críticas
Os seguintes valores são gerados pelo Terraform e configurados no arquivo `.env` (local) ou como *Secrets* (K8s):

* **FACE_API_ENDPOINT:** URL da API de IA.
* **FACE_API_KEY:** Chave de autenticação da Face API.
* **STORAGE_ACCOUNT_NAME:** Nome da conta de armazenamento.
* **STORAGE_CONTAINER_NAME:** Nome do container de destino (`validated-faces`).
* **STORAGE_CONNECTION_STRING:** String de conexão completa para persistência de dados.

> **Dica:** Para extrair esses valores após o deploy da infra, utilize:
> `terraform output -raw STORAGE_CONNECTION_STRING`

---

## 🔐 Configuração das Variáveis de Ambiente (.env)

Após o provisionamento da infraestrutura (Etapa 1), você deve configurar as credenciais no seu ambiente local em um arquivo chamado **.env**. 

### Criando o arquivo .env

# 1. Recupere os valores do Terraform

```bash

cd ./terraform
terraform output -raw FACE_API_ENDPOINT
terraform output -raw FACE_API_KEY
terraform output -raw STORAGE_ACCOUNT_NAME
terraform output -raw STORAGE_CONTAINER_NAME
terraform output -raw STORAGE_CONNECTION_STRING
```

# 2. Crie um arquivo chamado **.env** na raiz da pasta app e preencha com os valores obtidos acima:

```env
FACE_API_ENDPOINT=valor_obtido_no_terraform
FACE_API_KEY=valor_obtido_no_terraform
STORAGE_ACCOUNT_NAME=valor_obtido_no_terraform
STORAGE_CONTAINER_NAME=valor_obtido_no_terraform
STORAGE_CONNECTION_STRING=valor_obtido_no_terraform
```

## 🛠️ Comandos de Execução Local

Vá para a raiz do projeto no terminal e siga o fluxo abaixo para validar o microserviço:

```bash
# 1. Configurar o ambiente Python
python -m venv venv

# No Linux ou macOS
source venv/bin/activate
# No Windows (Prompt de Comando - CMD)
venv\Scripts\activate
# No Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r app/requirements.txt

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

### 📦 3. Containerização e Kubernetes (Deploy em Nuvem)

Esta etapa detalha como empacotar o microserviço e realizar o deploy manual no cluster **AKS**.

#### A. Preparação da Imagem Docker
Primeiro, é necessário capturar o endereço do seu Registro de Containers (ACR) e realizar o build da imagem local:

```bash
export ACR_LOGIN_SERVER=$(terraform -chdir=terraform output -raw ACR_LOGIN_SERVER)

docker build -t $ACR_LOGIN_SERVER/face-detection-quality:latest .

docker push $ACR_LOGIN_SERVER/face-detection-quality:latest
```

#### B. Configuração de Segredos (Secrets) no Cluster
O Kubernetes precisa das credenciais da Azure para funcionar. O comando abaixo captura os outputs do Terraform e cria a Secret no AKS de forma segura:

```bash
export K_ENDPOINT=$(terraform -chdir=terraform output -raw FACE_API_ENDPOINT) && \
export K_KEY=$(terraform -chdir=terraform output -raw FACE_API_KEY) && \
export K_ST_NAME=$(terraform -chdir=terraform output -raw STORAGE_ACCOUNT_NAME) && \
export K_ST_CONT=$(terraform -chdir=terraform output -raw STORAGE_CONTAINER_NAME) && \
export K_ST_CONN=$(terraform -chdir=terraform output -raw STORAGE_CONNECTION_STRING)

kubectl create secret generic face-api-secrets \
  --from-literal=FACE_API_ENDPOINT="$K_ENDPOINT" \
  --from-literal=FACE_API_KEY="$K_KEY" \
  --from-literal=STORAGE_ACCOUNT_NAME="$K_ST_NAME" \
  --from-literal=STORAGE_CONTAINER_NAME="$K_ST_CONT" \
  --from-literal=STORAGE_CONNECTION_STRING="$K_ST_CONN"

```

#### C. Deploy dos Manifestos
Utilizamos o utilitário **envsubst** para injetar dinamicamente o nome do ACR no manifesto de deployment, garantindo portabilidade entre diferentes ambientes:

```bash
envsubst < k8s/deployment.yaml | kubectl apply -f -

kubectl apply -f k8s/service.yaml
```

#### D. Verificação do Status e Acesso
Após o deploy, acompanhe a criação do IP público para realizar os testes através do IP listado em **EXTERNAL-IP**:

```bash
kubectl get pods

kubectl get service face-quality-service --watch
```

---

# 🚀 Guia de Setup: Deploy Automatizado (GitHub Actions)

Este guia descreve como provisionar a infraestrutura e realizar o deploy do microserviço de forma 100% automatizada, utilizando o pipeline de CI/CD configurado.

## 1. Preparação da Identidade (Bootstrap)
Antes de disparar o pipeline, você precisa criar as credenciais que permitirão ao GitHub Actions gerenciar sua conta Azure. 

1. Certifique-se de estar logado via Azure CLI através do comando **az login**.
2. Execute o script de bootstrap na raiz do projeto:

```bash

chmod +x bootstrap.sh
./bootstrap.sh

```

3. **Importante:** Ao final, o script imprimirá um JSON (identificado como **AZURE_CREDENTIALS**) e o nome de uma Storage Account. Guarde esses valores com cuidado.

## 2. Configuração de Segredos no GitHub
Para que o workflow tenha permissão de execução, você deve configurar os seguintes **Actions Secrets** no seu repositório, acessando as abas **Settings > Secrets and variables > Actions**:

* **AZURE_CREDENTIALS**: Insira o JSON completo gerado pelo script de bootstrap.
* **PREFIX**: Escolha um nome curto para identificar seus recursos de forma única (ex: **facequality**).

## 3. Vinculação do Terraform ao Backend
Abra o arquivo **terraform/main.tf** e localize o bloco identificado como **backend "azurerm"**. Você deve atualizar o campo **storage_account_name** com o nome exato da conta de armazenamento gerada no passo do bootstrap. Isso garante que o estado da sua infraestrutura seja salvo na nuvem e não localmente.

## 4. Executando o Pipeline
Com as configurações acima realizadas, o deploy torna-se automático. Basta realizar um **git push** para a branch **main** e observar o progresso na aba **Actions** do seu repositório.

## 🔍 Monitorando o Deploy após a conclusão
Após o pipeline finalizar, você pode validar a saúde da aplicação diretamente pelo seu terminal:

1. Atualize seu acesso local ao cluster com o comando **az aks get-credentials --resource-group "rg-${PREFIX}-prod" --name "${PREFIX}-aks" --overwrite-existing**.
2. Verifique se os pods estão em execução com o comando **kubectl get pods**.
3. Acompanhe o processamento das imagens em tempo real utilizando o comando **kubectl logs -f deployment/face-quality-api**.

---

## ⚙️ Funcionamento do Pipeline (GitHub Actions)

O workflow `Full CI/CD` foi desenhado seguindo princípios de **GitOps** e **Infraestrutura como Código (IaC)**, dividindo-se em 5 etapas principais:

### 1. Detectar Alterações 🔍
* O pipeline utiliza filtros de caminho (`paths-filter`) para otimizar o tempo de execução.
* Ele identifica se as mudanças ocorreram na pasta `terraform/` (infraestrutura).
* Se não houver mudanças na infraestrutura, o estágio de Terraform é ignorado para economizar recursos.

### 2. Provisionamento de Infraestrutura (IaC) 🏗️
* Realiza o `terraform init` e `terraform apply` de forma automatizada.
* Garante que o cluster AKS, o Registro de Containers (ACR) e os serviços de IA (Face API) estejam no estado desejado.
* Utiliza um **Backend Remoto** para garantir a consistência do estado entre diferentes execuções.

### 3. Auto-Discovery & Secrets Management 🔐
* Esta é a inteligência do pipeline: ele utiliza a **Azure CLI** para descobrir dinamicamente os endpoints e chaves gerados pelo Terraform.
* Os dados são exportados para um arquivo protegido (`azure.env`) e carregados como um **Artifact** do GitHub.
* **Resiliência:** Esta etapa protege caracteres especiais das Connection Strings, evitando corrupção de dados no deploy.

### 4. CI: QA & Docker Build 🛠️
* **Qualidade (QA):** Executa a suíte de testes unitários com `Pytest` em um ambiente virtualizado.
* **Build:** Se os testes passarem, o Docker constrói a imagem da aplicação.
* **Push:** A imagem é tagueada e enviada para o **Azure Container Registry (ACR)** privado.

### 5. CD: Deploy & Rollout AKS 🚀
* **Sync de Secrets:** Injeta as credenciais descobertas no estágio 3 diretamente no Kubernetes via `kubectl apply`.
* **Manifestos Dinâmicos:** Utiliza o `envsubst` para injetar o endereço do ACR nos arquivos YAML de deployment.
* **Zero Downtime:** Executa um `rollout restart` para que os pods antigos sejam substituídos pelos novos sem interromper o serviço.
* **Health Check:** O pipeline aguarda o status do rollout para confirmar que a aplicação subiu com sucesso.