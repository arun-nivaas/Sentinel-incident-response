import httpx
from typing import Dict, Any
from app.agentic_workflow.nodes.log_analyzer_node import log_analyzer_node


async def target(inputs: Dict[str, Any]) -> Dict[str, Any]:
    raw_payload = inputs["input"]["raw_payload"]
    result_state = await log_analyzer_node({"raw_payload": raw_payload})
    return result_state