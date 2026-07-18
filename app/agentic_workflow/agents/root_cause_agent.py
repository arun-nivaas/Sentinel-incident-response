import os
import logging
from typing import Optional, Any
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas import RootCauseSchema
from app.core.exceptions import LLMInvocationError,LLMInitializationError
from app.core.constant import Constants
from langsmith import traceable # type:ignore
from app.core.prompt_registry import PromptRegistry 

logger = logging.getLogger(__name__)

class RootCauseAgent:
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
            model = Constants.GEMINI_3_5,
            temperature = 0,
            max_output_tokens = 1000,
            api_key = SecretStr(os.getenv("GOOGLE_API_KEY") or ""),
            )
            self.prompt = PromptRegistry()
        except Exception as e:
            raise LLMInitializationError(f"Unable to initialize {Constants.GEMINI_3_5} LLM: {e}") from e
        
    @traceable(name="root_cause", tags=["root-cause"])
    async def analyze_root_cause(
        self,
        service_name: Optional[str],
        error_type: Optional[str],
        stack_trace: Optional[str],
        endpoint: Optional[str],
        occurrence_count: Optional[int],
    ) -> RootCauseSchema:
        try:
            structured_llm:Any = self.llm.with_structured_output(RootCauseSchema) #type: ignore

            prompt = self.prompt.get_prompt("sentinel-rootcause-analyzer")

            chain = prompt | structured_llm
            response: RootCauseSchema = await chain.ainvoke({
                "service_name": service_name or "unknown",
                "error_type": error_type or "unknown",
                "stack_trace": stack_trace or "not available",
                "endpoint": endpoint or "unknown",
                "occurrence_count": occurrence_count or "unknown",
            })

            logger.debug(f"Root Cause Response: {response}")
            return response

        except Exception as e:
            raise LLMInvocationError(f"Failed to invoke {Constants.GEMINI_3_5} LLM: {e}") from e