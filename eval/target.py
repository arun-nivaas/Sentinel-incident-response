from typing import Dict, Any
from app.agentic_workflow.nodes.log_analyzer_node import log_analyzer_node
from app.agentic_workflow.nodes.root_cause_node import root_cause_node
from app.database.database import AsyncSessionLocal

async def target(inputs: Dict[str, Any]) -> Dict[str, Any]:
    raw_payload = inputs["input"]["raw_payload"]
    result_state = await log_analyzer_node({"raw_payload": raw_payload})
    return result_state

async def root_cause_target(inputs: Dict[str, Any]) -> Dict[str, Any]:
    incident_input = inputs["input"]
    db = AsyncSessionLocal()
    try:
        state = {
            "service_name": incident_input.get("service_name"),
            "error_type": incident_input.get("error_type"),
            "stack_trace": incident_input.get("stack_trace"),
            "endpoint": incident_input.get("endpoint"),
            "occurrence_count": incident_input.get("occurrence_count"),
            "recurrence_count": incident_input.get("recurrence_count"),
            "root_cause_retry_count": 0,
        }
        result = await root_cause_node(state, {"configurable": {"db": db}})
        return result
    finally:
        await db.close()