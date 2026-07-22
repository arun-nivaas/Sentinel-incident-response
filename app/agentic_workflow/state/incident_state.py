from typing import TypedDict, Optional

class IncidentState(TypedDict):
    raw_incident_id: int
    raw_payload: str
    service_name: Optional[str]
    error_type: Optional[str]
    stack_trace: Optional[str]
    endpoint: Optional[str]
    occurrence_count: Optional[int]
    occurred_at: Optional[str]
    severity_hint: Optional[str]
    root_cause_hypothesis: Optional[str]
    root_cause_confidence: Optional[str]
    rag_grounded: Optional[bool]
    root_cause_retry_count: Optional[int]
    recurrence_count: Optional[int]
    severity_level: Optional[str]
    severity_reasoning: Optional[str]
    severity_confidence: Optional[str]
    suggested_fix: Optional[str]
    fix_confidence: Optional[str]
    github_issue_body: Optional[str]
    github_issue_url: Optional[str]
    github_issue_number: Optional[int]



      