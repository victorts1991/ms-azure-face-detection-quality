# MS Azure Face Detection Quality 🛡️

Microserviço em FastAPI para validação de qualidade de capturas faciais utilizando **Azure AI Face API**, implantado em **Azure Kubernetes Service (AKS)** com **CI/CD via GitHub Actions**.

## 🚀 Objetivo
Validar se uma foto de rosto atende aos requisitos mínimos para reconhecimento facial (iluminação, acessórios, ângulo) antes de persistir a imagem no Azure Blob Storage.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Framework:** FastAPI
* **IA:** Azure AI Foundry (Face API)
* **Infra:** Azure Kubernetes Service (AKS) & Azure Container Registry (ACR)
* **Storage:** Azure Blob Storage
* **DevOps:** GitHub Actions (CI/CD) & Pytest

---

## 🗺️ Roadmap de Desenvolvimento

### 1. Preparação do Ambiente (Azure Portal)
- [ ] Criar Grupo de Recursos.
- [ ] Provisionar Azure AI Services (Face API).
- [ ] Criar Storage Account e Container de fotos.
- [ ] Criar Azure Container Registry (ACR).
- [ ] Criar Cluster AKS.

### 2. Desenvolvimento do Microserviço
- [ ] Setup do projeto FastAPI e Poetry/Pip.
- [ ] Implementação do Client da Face API (Lógica de validação: glasses, blur, headPose).
- [ ] Implementação do Upload para Blob Storage (fotos aprovadas).
- [ ] Endpoint de recuperação de imagem por ID.

### 3. Containerização e Kubernetes
- [ ] Criação do Dockerfile.
- [ ] Manifestos K8s (Deployment, Service, HPA).
- [ ] Configuração de Secrets no K8s para chaves da Azure.

### 4. CI/CD & Testes
- [ ] Escrita de Testes Unitários com Pytest.
- [ ] Pipeline de CI (Lint, Test, Build & Push ACR).
- [ ] Pipeline de CD (Deploy to AKS).

### 5. Finalização
- [ ] Gravação de vídeo demonstrativo.
- [ ] Documentação dos endpoints (Swagger).

---

## 📖 Guia de Configuração (Manual)
*Esta seção conterá o passo a passo de como configurar os recursos no portal da Azure.*