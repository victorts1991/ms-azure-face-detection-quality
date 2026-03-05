import pytest
from unittest.mock import patch

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive", "cloud": "azure"}

# Testando os cenários de erro que validamos manualmente
@pytest.mark.parametrize("error_msg, expected_detail", [
    ("Por favor, retire o boné ou chapéu para a foto.", "Por favor, retire o boné"),
    ("Por favor, retire os óculos de sol.", "retire os óculos de sol"),
    ("Posicione o rosto de frente para a câmera.", "rosto de frente"),
    ("Ambiente muito escuro.", "Ambiente muito escuro"),
    ("Nenhum rosto encontrado na imagem.", "Nenhum rosto encontrado"),
])
@patch("app.services.azure_face.FaceService.validate_image_quality")
def test_analyze_face_quality_errors(mock_face, client, error_msg, expected_detail):
    # Simula a resposta negativa da Azure conforme o cenário
    mock_face.return_value = {"valid": False, "error": error_msg}
    
    files = {"file": ("test.jpg", b"fakecontent", "image/jpeg")}
    response = client.post("/analyze-face", files=files)
    
    assert response.status_code == 400
    assert expected_detail in response.json()["detail"]["error"]

@patch("app.services.azure_face.FaceService.validate_image_quality")
@patch("app.services.azure_storage.StorageService.upload_image")
def test_analyze_face_success(mock_storage, mock_face, client):
    # Simula o "Caminho Feliz"
    mock_face.return_value = {"valid": True, "face_id": "validated-sdk"}
    mock_storage.return_value = "https://facequalitystorage.blob.core.windows.net/validated-faces/foto.jpg"
    
    files = {"file": ("rosto_perfeito.jpg", b"imagebytes", "image/jpeg")}
    response = client.post("/analyze-face", files=files)
    
    assert response.status_code == 200
    assert response.json()["status"] == "aprovado"
    assert "storage_url" in response.json()