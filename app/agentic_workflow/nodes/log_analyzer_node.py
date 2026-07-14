from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.agents.log_analyzer_agent import LogAnalyzerAgent
from typing import Dict, Any

async def log_analyzer_node(state: IncidentState) -> Dict[str, Any]:
    """LangGraph node — reads raw_payload from state, returns extracted fields to merge into state."""
    result = await LogAnalyzerAgent().analyze_logs(state["raw_payload"])

    return {
        "service_name": result.service_name,
        "error_type": result.error_type,
        "stack_trace": result.stack_trace,
        "endpoint": result.endpoint,
        "occurrence_count": result.occurrence_count,
        "occurred_at": result.occurred_at,
        "severity_hint": result.severity_hint,
    }