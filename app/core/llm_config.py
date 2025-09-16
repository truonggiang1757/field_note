import logging
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.embeddings.base import Embeddings
import requests
from langchain_openai import ChatOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

load_dotenv()
class HugEmbeddings(Embeddings):
    """Gọi API embedding qua endpoint HuggingFace."""
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        resp = requests.post(self.endpoint, headers=headers, json={"input": texts})
        resp.raise_for_status()
        data = resp.json()["data"]
        return [d["embedding"] for d in data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]
    
class GeminiProvider:
    """Provider for Google Gemini models."""
    def __init__(self,  temperature: float = 0.4, model_llm: str = None, model_embeddings: str = None):
        self.google_api_key = settings.GEMINI_API_KEY
        self.temperature = temperature
        self.model_llm = model_llm.split('/')[-1] if model_llm is not None else settings.MODEL_LLM.split('/')[-1]
        self.model_embeddings = model_embeddings.split('/')[-1] if model_embeddings is not None else settings.MODEL_EMBEDDINGS.split('/')[-1]   

    def get_chat_model(self):
        logger.info("Using Google Gemini model:", self.model_llm)
        chat_model = ChatGoogleGenerativeAI(
            model=self.model_llm,  # Hoặc model tự host như "gemini-2.5-flash"
            google_api_key=self.google_api_key,
            temperature=self.temperature
        )
        return chat_model
    def get_embedding_model(self):
        return GoogleGenerativeAIEmbeddings(
            model=self.model_embeddings,  # type: ignore
            google_api_key=self.google_api_key  # type: ignore
        )
    def get_num_tokens(self, text):
        """Trả về số token đã sử dụng."""
        # Gemini API không cung cấp thông tin token usage trực tiếp
        return self.get_chat_model().get_num_tokens(text)

class QwenProvider:
    """Provider for Qwen models."""
    def __init__(self, temperature: float = 0.0, model_llm: str = None, model_embeddings: str = None):
        self.api_key = settings.QWEN_TOKEN # Use environment variable or provided key
        self.temperature = temperature
        self.model_llm = model_llm if model_llm is not None else settings.MODEL_LLM
        self.model_embeddings = model_embeddings if model_embeddings is not None else settings.MODEL_EMBEDDINGS

    def get_chat_model(self):
        return ChatOpenAI(
                    model=self.model_llm,  # Hoặc model tự host như "qwen:7b", "mistral", v.v. # type: ignore
                    base_url=settings.QWEN_LLM_URL,  # Self-hosted LLM API endpoint
                    api_key=self.api_key,  # Có thể là dummy key # type: ignore
                    temperature=0.0
                )
    
    def get_embedding_model(self):
        return HugEmbeddings(
            endpoint=settings.QWEN_EMBEDDING_URL,  # type: ignore
            api_key=self.api_key  # type: ignore
        )

class VinternProvider:
    """Provider for Vintern models."""
    def __init__(self, temperature: float = 0.0, model_llm: str = None, model_embeddings: str = None):
        self.api_key = settings.QWEN_TOKEN # Use environment variable or provided key
        self.temperature = temperature
        self.model_llm = model_llm if model_llm is not None else "5CD-AI/Vintern-3B-R-beta"
        self.model_embeddings = model_embeddings if model_embeddings is not None else settings.MODEL_EMBEDDINGS
        self.vlm_base_url = settings.VINTERN_LLM_URL

    def get_chat_model(self):
        return ChatOpenAI(
                    model=self.model_llm, 
                    base_url=self.vlm_base_url,
                    api_key=self.api_key,
                    temperature=0.5,
                    max_tokens=2048
                )
    
    def get_embedding_model(self):
        return HugEmbeddings(
            endpoint=settings.QWEN_EMBEDDING_URL,  # type: ignore
            api_key=self.api_key  # type: ignore
        )

from typing import Optional

def get_chat_model(model: Optional[str] = None):
    if model is None:
        model = settings.MODEL_LLM or "Qwen/Qwen3-8B"
    temp = model.split("/")
    if len(temp) == 2 and temp[0].lower() == "qwen":
        return QwenProvider(model_llm=model).get_chat_model()
    elif len(temp) == 2 and temp[0].lower() == "gemini":
        return GeminiProvider(model_llm=model).get_chat_model()
    elif len(temp) == 2 and temp[0].lower() == "5cd-ai":
        return VinternProvider(model_llm=model).get_chat_model()
    else:
        raise ValueError("Unsupported model type or provider. Or you forget to provide the provider")

def get_embedding_model(model: Optional[str] = None):
    if model is None:
        model = settings.MODEL_LLM or "Qwen/Qwen3-8B"
    temp = model.split("/")
    logger.info(temp)
    if len(temp) == 2 and temp[0].lower() == "qwen":
        return QwenProvider(model_embeddings=model).get_embedding_model()
    elif len(temp) == 2 and temp[0].lower() == "gemini":
        return GeminiProvider(model_embeddings=model).get_embedding_model()
    else:
        raise ValueError("Unsupported embedding model type or provider. Or you forget to provide the provider")

# class CrewModelConfig:
#     """Singleton cho cấu hình LLM/Embeddings."""
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#         return cls._instance

#     def get_llm_model(self):
#         # print("hehe", os.getenv("QWEN_TOKEN"))
#         """Khởi tạo model theo loại và provider."""
#         provider = settings.PROVIDER
#         if provider == "google":
#                 return ChatGoogleGenerativeAI(
#                     model=os.getenv("MODEL", "gemini-2.5-flash"),  # Hoặc model tự host như "gemini-2.5-flash"
#                     google_api_key=os.getenv("GOOGLE_API_KEY"),
#                     temperature=0.4
#                 )
#         elif provider == "qwen":
#                 return ChatOpenAI(
#                     model=os.getenv("MODEL", "Qwen/Qwen3-8B"),  # Hoặc model tự host như "qwen:7b", "mistral", v.v.
#                     base_url=settings.QWEN_LLM_URL,  # Self-hosted LLM API endpoint
#                     api_key=os.getenv("QWEN_TOKEN"),  # Có thể là dummy key # type: ignore
#                     temperature=0.0
#                 )

#         raise ValueError("model_type hoặc provider không hợp lệ.")
#     def get_embedding_model(self):
#         """Khởi tạo model embedding theo loại và provider."""
#         provider = os.getenv("PROVIDER", "qwen").lower()
#         if provider == "google":
#             return GoogleGenerativeAIEmbeddings(
#                 model=os.getenv("MODEL_EMBEDDINGS", "text-embedding-004"),
#                 google_api_key=os.getenv("GOOGLE_API_KEY") # type: ignore
#             )
#         elif provider == "qwen":
#             return HugEmbeddings(
#                 endpoint=settings.QWEN_EMBEDDING_URL, # type: ignore
#                 api_key=os.getenv("QWEN_TOKEN") # type: ignore
#             )
#         raise ValueError("provider không hợp lệ.")
    
# # Hàm tiện lợi để lấy model
# def get_llm_model():
#     """
#     Lấy model theo loại ('llm' hoặc 'embeddings') và provider ('google' hoặc 'qwen').
#     """
#     config = CrewModelConfig()
#     return config.get_llm_model()

# # Ví dụ sử dụng:
# # llm_google = get_llm_model()
# # embeddings_qwen = get_llm_model("embeddings")