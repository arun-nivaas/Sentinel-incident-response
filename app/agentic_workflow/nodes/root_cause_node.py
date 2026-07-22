from typing import Dict, Any
from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.agents.root_cause_agent import RootCauseAgent
from sqlalchemy.orm import Session
from langchain_core.runnables import RunnableConfig


async def root_cause_node(state: IncidentState,config:RunnableConfig) -> Dict[str,Any]:

    configurable:Any = config.get("configurable") or {}
    db: Session = configurable.get("db")

    retry_count = state.get("root_cause_retry_count", 0) or 0
    broad_retrieval = retry_count > 0  # use looser threshold on retry

    agent = RootCauseAgent(db=db)
    result = await agent.analyze_root_cause(
        service_name=state.get("service_name"),
        error_type=state.get("error_type"),
        stack_trace=state.get("stack_trace"),
        endpoint=state.get("endpoint"),
        occurrence_count=state.get("occurrence_count"),
        recurrence_count=state.get("recurrence_count"),
        broad_retrieval=broad_retrieval,
    )

    return {
        "root_cause_hypothesis": result["root_cause_hypothesis"],
        "root_cause_confidence": result["root_cause_confidence"],
        "rag_grounded": result["rag_grounded"],
        "root_cause_retry_count": retry_count + 1,
    }