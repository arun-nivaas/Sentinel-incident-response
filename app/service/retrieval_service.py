from sqlalchemy.orm import Session
from app.models.postmortem import Postmortem
from app.core.logger import logger
from typing import Dict,Any


STRICT_THRESHOLD = 0.35
BROAD_THRESHOLD = 0.55


class RetrievalService:
    def __init__(self, db: Session):
        self.db = db

    def find_similar_postmortems(
        self, query_embedding: list[float], top_k: int = 2, broad: bool = False
    ) -> list[Dict[str,Any]]:
        threshold = BROAD_THRESHOLD if broad else STRICT_THRESHOLD
        try:
            results = (
                self.db.query(
                    Postmortem,
                    Postmortem.embedding.cosine_distance(query_embedding).label("distance"),
                )
                .order_by("distance")
                .limit(top_k)
                .all()
            )

            relevant:Any = [
                {"postmortem": pm, "distance": float(distance)}
                for pm, distance in results
                if distance <= threshold
            ]
            return relevant

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []