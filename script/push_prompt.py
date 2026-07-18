from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from app.prompt_library.prompts import LOG_ANALYZER_PROMPT,ROOT_CAUSE_PROMPT,SEVERITY_PROMPT,REMEDIATION_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

client = Client()

print(client)

print("API KEY:", os.getenv("LANGSMITH_API_KEY"))
print("ENDPOINT:", os.getenv("LANGSMITH_ENDPOINT"))
print("WORKSPACE:", os.getenv("LANGSMITH_WORKSPACE"))


#Log Analyzer 

log_analyzer_prompt = ChatPromptTemplate.from_messages([
                ("system", LOG_ANALYZER_PROMPT),
                ("human", "### RAW LOG:\n{raw_payload}\n\nExtract all relevant fields precisely.")
            ])

client.push_prompt("sentinel-log-analyzer", object=log_analyzer_prompt)

# RootCause Analyzer

root_cause_prompt = ChatPromptTemplate.from_messages([
                ("system", ROOT_CAUSE_PROMPT),
                ("human", (
                    "### INCIDENT DETAILS:\n"
                    "Service: {service_name}\n"
                    "Error type: {error_type}\n"
                    "Stack trace: {stack_trace}\n"
                    "Endpoint: {endpoint}\n"
                    "Occurrence count: {occurrence_count}\n\n"
                    "Analyze and provide a root cause hypothesis."
                )),
            ])

client.push_prompt("sentinel-rootcause-analyzer", object=root_cause_prompt)

#Severity Analyzer

severity_prompt =ChatPromptTemplate.from_messages([
                ("system", SEVERITY_PROMPT),
                ("human", 
                    "### INCIDENT DETAILS:\n"
                    "Service: {service_name}\n"
                    "Error type: {error_type}\n"
                    "Endpoint: {endpoint}\n"
                    "Occurrence count: {occurrence_count}\n\n"
                    "### ROOT CAUSE ANALYSIS:\n"
                    "Hypothesis: {root_cause_hypothesis}\n"
                    "Confidence: {root_cause_confidence}\n\n"
                    "Classify the severity."
                ),
            ])

client.push_prompt("sentinel-severity-analyzer", object=severity_prompt)

#Remediation Analyzer

remediation_prompt =ChatPromptTemplate.from_messages([
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

client.push_prompt("sentinel-remediation-analyzer", object=remediation_prompt)