from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from app.core.config import settings
import io

class FaceService:
    def __init__(self):
        self.client = FaceClient(
            settings.FACE_API_ENDPOINT, 
            CognitiveServicesCredentials(settings.FACE_API_KEY)
        )

    async def validate_image_quality(self, image_stream: io.BytesIO):
        try:
            # Resetamos o ponteiro do arquivo para garantir a leitura do início
            image_stream.seek(0)

            # Chamada usando o SDK oficial
            detected_faces = self.client.face.detect_with_stream(
                image=image_stream,
                # 'accessories' é a chave para pegar o boné, mas só funciona no detection_01
                return_face_attributes=['blur', 'exposure', 'headPose', 'accessories', 'glasses'],
                detection_model='detection_01',
                return_face_id=False # Obrigatório ser False para evitar erro de permissão (Privacidade Azure)
            )

            if not detected_faces:
                return {"valid": False, "error": "Nenhum rosto encontrado na imagem."}

            # Pegamos os atributos do primeiro rosto detectado
            face = detected_faces[0].face_attributes
            
            # 1. VALIDAÇÃO DE ACESSÓRIOS (Aqui pegamos o boné)
            if face.accessories:
                for acc in face.accessories:
                    tipo = acc.type.lower()
                    if acc.confidence > 0.6:
                        if tipo == 'headwear':
                            return {"valid": False, "error": "Por favor, retire o boné ou chapéu para a foto."}

            # 2. VALIDAÇÃO DE ÓCULOS
            # ReadingGlasses costumam ser aceitos, Sunglasses não.
            if face.glasses and face.glasses.value.lower() == "sunglasses":
                return {"valid": False, "error": "Por favor, retire os óculos de sol."}

            # 3. VALIDAÇÃO DE POSE (Ângulos do rosto)
            if abs(face.head_pose.yaw) > 15 or abs(face.head_pose.pitch) > 15:
                return {"valid": False, "error": "Posicione o rosto de frente para a câmera."}

            # 4. VALIDAÇÃO DE QUALIDADE (Luz e Nitidez)
            if face.blur.blur_level.value.lower() == "high":
                return {"valid": False, "error": "A imagem está muito borrada. Tente novamente."}
            
            if face.exposure.exposure_level.value.lower() == "underexposure":
                return {"valid": False, "error": "Ambiente muito escuro. Melhore a iluminação do rosto."}

            # SUCESSO
            return {
                "valid": True, 
                "face_id": "validated-sdk", 
                "message": "Qualidade da imagem aprovada."
            }

        except Exception as e:
            # Captura erros de InvalidRequest ou problemas de conexão
            print(f"ERRO SDK AZURE: {str(e)}")
            return {"valid": False, "error": f"Erro na análise: {str(e)}"}