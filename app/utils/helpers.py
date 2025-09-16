import base64
from PIL import Image
from io import BytesIO
import json
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

def load_prompt(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise
    except IOError as e:
        raise

def resize_image(image_bytes: bytes, max_dimension: int = 1024) -> bytes:
        try:
            img = Image.open(BytesIO(image_bytes))
            if max(img.width, img.height) <= max_dimension:
                return image_bytes

            img.thumbnail((max_dimension, max_dimension))
            
            buffer = BytesIO()
            image_format = img.format if img.format in ["JPEG", "PNG"] else "JPEG"
            img.save(buffer, format=image_format)
            
            return buffer.getvalue()
        except Exception as e:
            print(f"Warning: Could not resize image, using original. Error: {e}")
            return image_bytes

def prepare_image(file_content: bytes, prompt: str) -> list:
    resized_content = resize_image(file_content)
    base64_image = base64.b64encode(resized_content).decode('utf-8')
    return [
        HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        )
    ]