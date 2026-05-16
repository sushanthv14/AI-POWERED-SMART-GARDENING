from PIL import Image
import io

def bytes_to_pil(image_bytes: bytes):
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")