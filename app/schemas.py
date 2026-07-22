from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class IncidentCreate(BaseModel):
    raw_payload: str
    source: str = "webhook"

class IncidentResponse(BaseModel):
    id: int
    received_at: datetime
    source: str
    status: str

    class Config:
        from_attributes = True

class ParsedIncidentResponse(BaseModel):
    id: int
    raw_incident_id: int
    service_name: Optional[str]
    error_type: Optional[str]
    stack_trace: Optional[str]
    endpoint: Optional[str]
    occurrence_count: Optional[int]
    occurred_at: Optional[datetime]
    parsed_at: datetime
    severity_hint: Optional[str]
    fingerprint: str

class RootCauseFindingResponse(BaseModel):
    id: int
    raw_incident_id: int
    root_cause_hypothesis: Optional[str]
    root_cause_confidence: Optional[str]

class SeverityFindingResponse(BaseModel):
    id: int
    raw_incident_id: int
    severity_level: Optional[str]
    severity_reasoning: Optional[str]
    severity_confidence: Optional[str]

class RemediationFindingResponse(BaseModel):
    id: int
    raw_incident_id: int
    suggested_fix: Optional[str]
    fix_confidence: Optional[str]
    github_issue_body: Optional[str]

class GithubActionFindingResponse(BaseModel):
    id: int
    raw_incident_id: int
    issue_url: Optional[str]
    issue_number: Optional[int]

class LogAnalysisSchema(BaseModel):
    service_name: Optional[str] = Field(description="Name of the affected service")
    error_type: Optional[str] = Field(description="Type of error, e.g. NullPointerException")
    stack_trace: Optional[str] = Field(description="Extracted stack trace, if present")
    endpoint: Optional[str] = Field(description="Affected API endpoint, if mentioned")
    occurrence_count: Optional[int] = Field(description="Number of times this error occurred")
    occurred_at: Optional[str] = Field(description="Timestamp when the error occurred, ISO format")
    severity_hint: Optional[str] = Field(description="Quick severity guess: low, medium, high, or critical")

class RootCauseSchema(BaseModel):
    root_cause_hypothesis: Optional[str] = Field(description="A concise, specific hypothesis for what likely caused this incident")
    root_cause_confidence: Optional[str] = Field(description="Confidence in this hypothesis: low, medium, or high")

class SeveritySchema(BaseModel):
    severity_level: Optional[str] = Field(description="One of: P1, P2, P3, P4 (P1 = most critical)")
    severity_reasoning: Optional[str] = Field(description="Brief justification for this severity level")
    severity_confidence: Optional[str] = Field(description="Confidence in this severity assessment: low, medium, or high")

class RemediationSchema(BaseModel):
    suggested_fix: Optional[str] = Field(description="Concrete, specific suggested fix or next investigation step")
    fix_confidence: Optional[str] = Field(description="Confidence in this fix suggestion: low, medium, or high")
    github_issue_body: Optional[str] = Field(description="A well-formatted GitHub issue body summarizing the incident, root cause, severity, and suggested fix")

class ProcessedIncidentResponse(BaseModel):
    id: int
    raw_incident_id: int
    service_name: Optional[str]
    error_type: Optional[str]
    stack_trace: Optional[str]
    endpoint: Optional[str]
    occurrence_count: Optional[int]
    occurred_at: Optional[datetime]
    parsed_at: datetime
    severity_hint: Optional[str]
    root_cause_hypothesis: Optional[str]
    root_cause_confidence: Optional[str]
    rag_grounded: Optional[bool]
    root_cause_retry_count: Optional[int]
    severity_level: Optional[str]
    severity_reasoning: Optional[str]
    severity_confidence: Optional[str]
    suggested_fix: Optional[str]
    fix_confidence: Optional[str]
    github_issue_body: Optional[str]
    github_issue_url: Optional[str]
    github_issue_number: Optional[int]

    
    class Config:
        from_attributes = True

