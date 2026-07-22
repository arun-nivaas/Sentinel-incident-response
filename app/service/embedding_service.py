# app/services/embedding_service.py
import logging
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

MODEL_CACHE_DIR = Path("./model_cache")


class EmbeddingServiceError(Exception):
    pass


class EmbeddingService:
    def __init__(self):
        try:
            cache_dir = MODEL_CACHE_DIR / "embedding"
            cache_dir.mkdir(parents=True, exist_ok=True)

            self.model = HuggingFaceEmbeddings(
                model_name="BAAI/bge-base-en-v1.5",
                cache_folder=str(cache_dir),
                model_kwargs={'device': "cpu"},
                encode_kwargs={'normalize_embeddings': True}
            )
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise EmbeddingServiceError("Could not initialize embedding service") from e

    def embed_text(self, text: str) -> list[float]:
        return self.model.embed_query(text)