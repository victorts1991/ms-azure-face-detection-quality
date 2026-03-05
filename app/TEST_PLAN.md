# 📑 Plano de Testes Manual - Validação Facial (Azure Face API)

Este documento descreve o roteiro de homologação para garantir que o microserviço está filtrando corretamente as imagens antes de persisti-las no Azure Blob Storage.

---

## 🧪 Cenários de Teste

| ID | Cenário de Teste | Ação (Envio de Foto) | Resultado Esperado (JSON) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Sucesso (Caminho Feliz)** | Foto de frente, sem acessórios, iluminação uniforme. | `200 OK` + `storage_url` | [X] |
| **02** | **Bloqueio de Boné** | Foto utilizando boné (aba para frente ou lado). | `400 Bad Request`: "Por favor, retire o boné..." | [X] |
| **03** | **Óculos Escuros** | Foto utilizando óculos de sol ou espelhados. | `400 Bad Request`: "Por favor, retire os óculos de sol." | [X] |
| **04** | **Rosto Desalinhado** | Foto olhando para os lados (perfil) ou muito para cima. | `400 Bad Request`: "Posicione o rosto de frente..." | [X] |
| **05** | **Baixa Iluminação** | Foto em ambiente escuro ou contra a luz. | `400 Bad Request`: "Ambiente muito escuro..." | [X] |
| **06** | **Ausência de Rosto** | Foto de uma parede, paisagem ou objeto. | `400 Bad Request`: "Nenhum rosto encontrado..." | [X] |
| **07** | **Óculos de Grau** | Foto com óculos de lente transparente. | `200 OK` (Deve ser permitido pelo sistema). | [X] |

---

## 📂 Validação de Armazenamento

Para cada teste com resultado **200 OK**:
1. Valide via Azure Storage Explorer;
2. Confirme se a imagem foi salva no container `validated-faces`.

