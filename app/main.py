import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.azure_face import FaceService
from app.services.azure_storage import StorageService
from app.schemas.face import FaceAnalysisResponse, FaceValidationError, StorageError
from azure.core.exceptions import AzureError

app = FastAPI(title="MS Azure Face Detection Quality")

# Use funções para obter os serviços (Lazy Instantiation)
def get_face_service():
    return FaceService()

def get_storage_service():
    return StorageService()

@app.get("/health")
def health():
    return {"status": "alive", "cloud": "azure"}

@app.post(
        "/analyze-face",
        response_model=FaceAnalysisResponse,
        responses={400: {"model": FaceValidationError}, 502: {"model": StorageError}}
)
async def analyze_face(file: UploadFile = File(...)):

    # Instancia apenas quando o endpoint é chamado
    face_ai = get_face_service()
    storage = get_storage_service()

    content = await file.read()
    
    # 1. Validação com a Face API
    validation = await face_ai.validate_image_quality(io.BytesIO(content))
    
    
    if not validation["valid"]:

        error_message = validation.get("error", "Qualidade insuficiente")
        
        raise HTTPException(
            status_code=400, 
            detail={
                "error": error_message,
                "details": validation.get("details"),
                "service": "Azure Face API"
            }
        )

    # 2. Upload para o Storage com tratamento de erro
    try:
        url = await storage.upload_image(content, file.filename)
    except AzureError as e:
        # Erro 502 (Bad Gateway) é comum quando um serviço dependente (Storage) falha
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Falha no armazenamento",
                "message": str(e),
                "service": "Azure Blob Storage"
            }
        )

    return {
        "status": "aprovado",
        "face_id": validation.get("face_id"),
        "storage_url": url,
        "message": "Processamento concluído com sucesso."
    }