from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.agents.severity_agent import SeverityAgent
from typing import Dict, Any

async def severity_node(state: IncidentState) -> Dict[str, Any]:
    result = await SeverityAgent().analyze_severity(
        service_name=state.get("service_name"),
        error_type=state.get("error_type"),
        endpoint=state.get("endpoint"),
        occurrence_count=state.get("occurrence_count"),
        root_cause_hypothesis=state.get("root_cause_hypothesis"),
        root_cause_confidence=state.get("confidence"),
    )

    return {
        "severity_level": result.severity_level,
        "severity_reasoning": result.severity_reasoning,
        "severity_confidence": result.severity_confidence,
    }