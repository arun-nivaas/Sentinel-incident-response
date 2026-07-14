from typing import Any,Dict
from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.agents.remediation_agent import RemediationAgent

async def remediation_node(state:IncidentState) -> Dict[str, Any]:
    
    result = await RemediationAgent().analyze_remediation(
        service_name=state.get("service_name"),
        error_type=state.get("error_type"),
        stack_trace=state.get("stack_trace"),
        endpoint=state.get("endpoint"),
        occurrence_count=state.get("occurrence_count"),
        root_cause_hypothesis=state.get("root_cause_hypothesis"),
        root_cause_confidence=state.get("root_cause_confidence"),
        severity_level=state.get("severity_level"),
        severity_reasoning=state.get("severity_reasoning"),
        severity_confidence=state.get("severity_confidence")
    )

    return {
        "suggested_fix": result.suggested_fix,
        "fix_confidence": result.fix_confidence,
        "github_issue_body": result.github_issue_body,
    }