from typing import Dict, Any
from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.agents.root_cause_agent import RootCauseAgent


async def root_cause_node(state: IncidentState) -> Dict[str, Any]:
    result = await RootCauseAgent().analyze_root_cause(
        service_name=state.get("service_name"),
        error_type=state.get("error_type"),
        stack_trace=state.get("stack_trace"),
        endpoint=state.get("endpoint"),
        occurrence_count=state.get("occurrence_count"),
    )

    return {
        "root_cause_hypothesis": result.root_cause_hypothesis,
        "root_cause_confidence": result.root_cause_confidence,
    }