import os
import logging
from typing import Optional, Any,Dict
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas import RootCauseSchema
from app.core.exceptions import LLMInvocationError,LLMInitializationError
from app.core.constant import Constants
from langsmith import traceable # type:ignore
from app.core.prompt_registry import PromptRegistry
from app.service.embedding_service import EmbeddingService
from app.service.retrieval_service import RetrievalService 
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class RootCauseAgent:
    def __init__(self,db: Session):
        try:
            self.llm = ChatGoogleGenerativeAI(
            model = Constants.GEMINI_3_5,
            temperature = 0,
            max_output_tokens = 1000,
            api_key = SecretStr(os.getenv("GOOGLE_API_KEY") or ""),
            )
            self.prompt = PromptRegistry()
            self.embedding_service = EmbeddingService()
            self.retrieval_service = RetrievalService(db)
        except Exception as e:
            raise LLMInitializationError(f"Unable to initialize {Constants.GEMINI_3_5} LLM: {e}") from e
        
    def _build_context(self, matches: list[Dict[str,Any]]) -> str:
        if not matches:
            return "No sufficiently similar past incidents found in the knowledge base."
        return "\n\n".join(
            f"- Past incident ({m['postmortem'].service_name}, {m['postmortem'].error_type}, "
            f"similarity distance {m['distance']:.3f}): {m['postmortem'].summary}"
            for m in matches
        )
        
    @traceable(name="root_cause", tags=["root-cause"])
    async def analyze_root_cause(
        self,
        service_name: Optional[str],
        error_type: Optional[str],
        stack_trace: Optional[str],
        endpoint: Optional[str],
        occurrence_count: Optional[int],
        recurrence_count: Optional[int] = None,
        broad_retrieval: bool = False,
    ) -> Dict[str,Any]:
        try:
            query_text = f"{error_type or ''} in {service_name or ''}: {stack_trace or ''}"
            query_embedding = self.embedding_service.embed_text(query_text)
            matches = self.retrieval_service.find_similar_postmortems(
                query_embedding, top_k=2, broad=broad_retrieval
            )
            retrieved_context = self._build_context(matches)
            grounded = len(matches) > 0

            structured_llm: Any = self.llm.with_structured_output(RootCauseSchema) #type: ignore
            prompt = self.prompt.get_prompt("sentinel-rootcause-analyzer")
            chain = prompt | structured_llm

            response: RootCauseSchema = await chain.ainvoke({
                "service_name": service_name or "unknown",
                "error_type": error_type or "unknown",
                "stack_trace": stack_trace or "not available",
                "endpoint": endpoint or "unknown",
                "occurrence_count": occurrence_count or "unknown",
                "recurrence_count": recurrence_count or "unknown",
                "retrieved_context": retrieved_context,
            })

            logger.debug(f"Root Cause Response (grounded={grounded}): {response}")

            return {
                "root_cause_hypothesis": response.root_cause_hypothesis,
                "root_cause_confidence": response.root_cause_confidence,
                "rag_grounded": grounded,
            }

        except Exception as e:
            logger.error("LLM invocation failed for root cause analysis", exc_info=True)
            raise LLMInvocationError("Root Cause LLM failed during analysis") from e