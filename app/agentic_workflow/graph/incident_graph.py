from langgraph.graph import StateGraph, END #type: ignore
from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.nodes.log_analyzer_node import log_analyzer_node
from app.agentic_workflow.nodes.root_cause_node import root_cause_node
from app.agentic_workflow.nodes.severity_node import severity_node
from app.agentic_workflow.nodes.remediation_node import remediation_node
from app.agentic_workflow.nodes.github_action_node import github_action_node

MAX_ROOT_CAUSE_RETRIES = 1


def route_after_root_cause(state: IncidentState) -> str:
    confidence = state.get("root_cause_confidence")
    grounded = state.get("rag_grounded", False)
    retry_count = state.get("root_cause_retry_count", 0) or 0

    if confidence == "low" and not grounded and retry_count <= MAX_ROOT_CAUSE_RETRIES:
        return "retry"
    return "continue"


class IncidentGraphBuilder:
    def __init__(self):
        self._graph = StateGraph(IncidentState)
        self._register_nodes()
        self._register_edges()

    def _register_nodes(self) -> None:
        self._graph.add_node("log_analyzer", log_analyzer_node)      # type: ignore
        self._graph.add_node("root_cause", root_cause_node)          # type: ignore
        self._graph.add_node("severity", severity_node)              # type: ignore
        self._graph.add_node("remediation", remediation_node)        # type: ignore
        self._graph.add_node("github_action", github_action_node)    # type: ignore

    def _register_edges(self) -> None:
        self._graph.set_entry_point("log_analyzer")
        self._graph.add_edge("log_analyzer", "root_cause")
        self._graph.add_conditional_edges(
            "root_cause",
            route_after_root_cause,
            {"retry": "root_cause", "continue": "severity"},
        )
        self._graph.add_edge("severity", "remediation")
        self._graph.add_edge("remediation", "github_action")
        self._graph.add_edge("github_action", END)

    def build(self):
        return self._graph.compile()  # type: ignore


incident_graph = IncidentGraphBuilder().build()