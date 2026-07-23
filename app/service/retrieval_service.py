
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.postmortem import Postmortem
from app.core.logger import logger
from typing import Dict,Any


STRICT_THRESHOLD = 0.35
BROAD_THRESHOLD = 0.55



class RetrievalService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_similar_postmortems(
        self, query_embedding: list[float], top_k: int = 2, broad: bool = False
    ) -> list[Dict[str, Any]]:
        threshold = BROAD_THRESHOLD if broad else STRICT_THRESHOLD
        try:
            distance_col = Postmortem.embedding.cosine_distance(query_embedding).label("distance")

            stmt = (
                select(Postmortem, distance_col)
                .order_by(distance_col)
                .limit(top_k)
            )

            result = await self.db.execute(stmt)
            rows = result.all()

            relevant: Any = [
                {"postmortem": pm, "distance": float(distance)}
                for pm, distance in rows
                if distance <= threshold
            ]
            return relevant

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []