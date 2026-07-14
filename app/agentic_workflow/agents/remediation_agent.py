from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.exceptions import LLMInvocationError, LLMInitializationError
from app.core.constant import Constants
from app.schemas import RemediationSchema
from typing import Optional,Any
import os
from app.prompt_library.prompts import REMEDIATION_PROMPT
from app.core.logger import logger
from langsmith import traceable # type:ignore

class RemediationAgent:
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
        
    @traceable(name="remediation", tags=["remediation"])  
    async def analyze_remediation(self,service_name: Optional[str],error_type: Optional[str],
        stack_trace: Optional[str],
        endpoint: Optional[str],
        occurrence_count: Optional[int],
        root_cause_hypothesis: Optional[str],
        root_cause_confidence: Optional[str],
        severity_level: Optional[str],
        severity_reasoning: Optional[str],
        severity_confidence: Optional[str]) -> RemediationSchema:
        try:
            structured_llm: Any = self.llm.with_structured_output(RemediationSchema) #type:ignore

            prompt = ChatPromptTemplate.from_messages([
            ("system", REMEDIATION_PROMPT),
            ("human", (
                "### INCIDENT SUMMARY:\n"
                "Service: {service_name}\n"
                "Error type: {error_type}\n"
                "Stack trace: {stack_trace}\n"
                "Endpoint: {endpoint}\n"
                "Occurrence count: {occurrence_count}\n\n"
                "### ROOT CAUSE:\n{root_cause_hypothesis} "
                "(confidence: {root_cause_confidence})\n\n"
                "### SEVERITY:\n{severity_level} — {severity_reasoning} "
                "(confidence: {severity_confidence})\n\n"
                "Provide a suggested fix and a GitHub issue body."
            )),
        ])

            chain = prompt | structured_llm
            response: RemediationSchema = await chain.ainvoke({
                "service_name": service_name or "unknown",
                "error_type": error_type or "unknown",
                "stack_trace": stack_trace or "not available",
                "endpoint": endpoint or "unknown",
                "occurrence_count": occurrence_count or "unknown",
                "root_cause_hypothesis": root_cause_hypothesis or "not available",
                "root_cause_confidence": root_cause_confidence or "unknown",
                "severity_level": severity_level or "unknown",
                "severity_reasoning": severity_reasoning or "not available",
                "severity_confidence": severity_confidence or "unknown",
            })

            logger.debug(f"Remediation Response: {response}")
            return response

        except Exception as e:
            raise LLMInvocationError(f"Failed to invoke {Constants.GEMINI_3_1} LLM: {e}") from e