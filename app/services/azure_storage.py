from azure.storage.blob import BlobServiceClient
from app.core.config import settings
import uuid

class StorageService:
    def __init__(self):
        self.client = BlobServiceClient.from_connection_string(settings.STORAGE_CONNECTION_STRING)

    async def upload_image(self, file_content: bytes, original_name: str):
        # Gera nome único: uuid + extensão original
        file_ext = original_name.split(".")[-1]
        blob_name = f"{uuid.uuid4()}.{file_ext}"
        
        blob_client = self.client.get_blob_client(
            container=settings.STORAGE_CONTAINER_NAME, 
            blob=blob_name
        )
        
        blob_client.upload_blob(file_content, overwrite=True)
        return blob_client.url