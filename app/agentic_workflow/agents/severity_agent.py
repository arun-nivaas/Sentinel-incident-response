from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.constant import Constants
from pydantic import SecretStr
import os
from app.core.exception import LLMInvocationError, LLMInitializationError
from app.schemas import SeveritySchema
from typing import Optional, Any
from app.core.logger import logger
from langsmith import traceable #type: ignore
from app.core.prompt_registry import PromptRegistry


class SeverityAgent:

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
            raise LLMInitializationError(message=f"Unable to initialize {Constants.GEMINI_3_5} LLM",details=str(e)) from e
    @traceable(name="severity", tags=["severity"])
    async def analyze_severity(
        self,
        service_name: Optional[str],
        error_type: Optional[str],
        endpoint: Optional[str],
        occurrence_count: Optional[int],
        root_cause_hypothesis: Optional[str],
        root_cause_confidence: Optional[str],
    ) -> SeveritySchema:
        try:
            structured_llm: Any = self.llm.with_structured_output(SeveritySchema) #type: ignore

            prompt = self.prompt.get_prompt("sentinel-severity-analyzer")

            chain = prompt | structured_llm
            response: SeveritySchema = await chain.ainvoke({
                "service_name": service_name or "unknown",
                "error_type": error_type or "unknown",
                "endpoint": endpoint or "unknown",
                "occurrence_count": occurrence_count or "unknown",
                "root_cause_hypothesis": root_cause_hypothesis or "not available",
                "root_cause_confidence": root_cause_confidence or "unknown",
            })

            logger.debug(f"Severity Response: {response}")  
            return response

        except Exception as e:
            raise LLMInvocationError(message = f"Failed to invoke {Constants.GEMINI_3_1}", details = str(e)) from e