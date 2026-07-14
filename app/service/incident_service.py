from typing import cast
from sqlalchemy.orm import Session
from app.models.raw_incident import RawIncident
from app.models.parsed_incident import ParsedIncident
from app.models.agent_finding import AgentFinding
from app.models.github_action import GithubActionFinding
from app.agentic_workflow.state.incident_state import IncidentState
from app.agentic_workflow.graph.incident_graph import incident_graph
from app.core.utils import compute_fingerprint
from typing import Dict,Any
from langsmith import traceable #type: ignore


class IncidentService:
    def __init__(self, db: Session):
        self.db = db
    @traceable(name="process_incident_pipeline")
    async def process_incident(self, raw: RawIncident) -> tuple[ParsedIncident, Dict[str,Any]]:
        initial_state: IncidentState = cast(IncidentState, {
            "raw_incident_id": raw.id,
            "raw_payload": raw.raw_payload,
            **{k: None for k in IncidentState.__annotations__
               if k not in ("raw_incident_id", "raw_payload")},
        })

        final_state = await incident_graph.ainvoke(initial_state) # type: ignore
        return self._persist(raw, final_state)

    def _persist(self, raw: RawIncident, final_state: Dict[str,Any]) -> tuple[ParsedIncident, Dict[str,Any]]:
        fingerprint = compute_fingerprint(
            final_state.get("service_name"), final_state.get("error_type"), final_state.get("endpoint")
        )
        parsed = ParsedIncident(
            raw_incident_id=raw.id,
            service_name=final_state.get("service_name"),
            error_type=final_state.get("error_type"),
            stack_trace=final_state.get("stack_trace"),
            endpoint=final_state.get("endpoint"),
            occurrence_count=final_state.get("occurrence_count"),
            occurred_at=final_state.get("occurred_at"),
            severity_hint=final_state.get("severity_hint"),
            fingerprint=fingerprint,
        )
        self.db.add(parsed)

        for agent_name, keys, conf_key in [
            ("root_cause", ["root_cause_hypothesis"], "root_cause_confidence"),
            ("severity", ["severity_level", "severity_reasoning"], "severity_confidence"),
            ("remediation", ["suggested_fix", "github_issue_body"], "fix_confidence"),
        ]:
            self.db.add(AgentFinding(
                raw_incident_id=raw.id,
                agent_name=agent_name,
                output={k: final_state.get(k) for k in keys},
                confidence=final_state.get(conf_key),
            ))

        self.db.add(GithubActionFinding(
            raw_incident_id=raw.id,
            issue_url=final_state.get("github_issue_url"),
            issue_number=final_state.get("github_issue_number"),
        ))

        raw.status = "processed"
        self.db.commit()
        self.db.refresh(parsed)
        return parsed, final_state 