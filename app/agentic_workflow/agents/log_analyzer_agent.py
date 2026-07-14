from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
import os
from langchain_core.runnables import Runnable
from langchain_core.language_models import LanguageModelInput
from app.schemas import LogAnalysisSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.exceptions import LLMInvocationError,LLMInitializationError
from app.core.constant import Constants
from app.prompt_library.prompts import LOG_ANALYZER_PROMPT
from app.core.logger import logger
from langsmith import traceable # type:ignore


class LogAnalyzerAgent:
    def __init__(self):
        try:
              self.llm = ChatGoogleGenerativeAI(
                model = Constants.GEMINI_3_1,
                temperature = 0,
                max_output_tokens = 1000,
                api_key = SecretStr(os.getenv("GOOGLE_API_KEY") or ""),
            )
        except Exception as e:
            raise LLMInitializationError(f"Unable to initialize {Constants.GEMINI_3_1} LLM: {e}") from e

    @traceable(name="log_analyzer", tags=["log-analyzer"])
    async def analyze_logs(self, raw_payload: str):
        try:
            structured_llm: Runnable[LanguageModelInput, LogAnalysisSchema] = self.llm.with_structured_output(LogAnalysisSchema) #type: ignore
            prompt = ChatPromptTemplate.from_messages([
                ("system", LOG_ANALYZER_PROMPT),
                ("human", "### RAW LOG:\n{raw_payload}\n\nExtract all relevant fields precisely.")
            ])

            chain = prompt | structured_llm  # type: ignore
            response = await chain.ainvoke({"raw_payload": raw_payload})  # type: ignore


            logger.debug(f"Log Analysis Response: {response}")
            return response  # type: ignore

        except Exception as e:
            raise LLMInvocationError(f"Failed to invoke {Constants.GEMINI_3_1} LLM: {e}") from e