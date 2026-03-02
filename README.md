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
- [X] Criar Grupo de Recursos.
- [X] Provisionar Azure AI Services (Face API).
- [X] Criar Storage Account e Container de fotos.
- [X] Criar Azure Container Registry (ACR).
- [X] Criar Cluster AKS.

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

## 🛠️ Guia de Configuração da Infraestrutura (Etapa 1)

Este guia detalha o protocolo de provisionamento do ambiente na **Azure** para o projeto de Análise de Qualidade Facial. A execução depende da validação manual do administrador em cada etapa para garantir a compatibilidade dos recursos.

### 1. Preparação da Camada de Assinatura
* **Elevação de Privilégios:** A assinatura deve ser convertida para o modelo **Pay-As-You-Go** (Assinatura do Azure 1) para permitir o provisionamento de recursos de computação.
* **Gestão Financeira:** Validação manual do saldo de créditos promocionais (R$ 1.028,70) no painel de *Gerenciamento de Custos* para garantir a cobertura dos serviços.

### 2. Configuração de Recursos Críticos (Pré-requisitos)
Antes do deploy do cluster, os seguintes serviços de suporte devem estar operacionais:
* **Network & Compute:** Definição da região estratégica (recomendado: **East US 2**) para disponibilidade de hardware.
* **Azure AI Services:** Instância da **Face API** provisionada para processamento de biometria e análise de atributos.
* **Storage & Registry:** * **Storage Account** configurado para a persistência de blobs (imagens).
    * **Azure Container Registry (ACR)** (`crfacequalityvictor`) estabelecido para o armazenamento privado de imagens Docker.

### 3. Provisionamento do Azure Kubernetes Service (AKS)
A criação do cluster `aks-face-quality` exige a aplicação rigorosa dos seguintes parâmetros de arquitetura:
* **Escalabilidade:** Configuração de **1 nó** em modo **Manual** no pool de sistema (`agentpool`).
* **Hardware:** Seleção da família de máquinas compatível (Ex: Série **DDSv5**) para evitar conflitos de suporte regional.
* **Topologia de Rede:** O campo **Zonas de Disponibilidade** deve ser definido como **"Nenhum"** para mitigar erros de restrição física (`AvailabilityZoneNotSupported`).
* **RBAC & Integração:** Vinculação nativa entre o **ACR** e o **AKS** na aba de integrações para autorizar o *pull* automático de imagens sem necessidade de segredos manuais.

---

### ✅ Status da Etapa 1: Homologada
Infraestrutura provisionada e em execução (Status: *Succeeded*).