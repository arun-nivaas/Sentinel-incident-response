from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.raw_incident import RawIncident
from app.models.parsed_incident import ParsedIncident
from app.schemas import IncidentCreate, IncidentResponse, ProcessedIncidentResponse
from app.service.incident_service import IncidentService
from app.core.exception import NotFoundException

router = APIRouter(prefix="/api/v1",tags=["Incident"])


@router.post("/incident", response_model=IncidentResponse)
async def create_raw_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    existing = db.query(RawIncident).filter(RawIncident.raw_payload == incident.raw_payload).first()
    if existing:
        return existing
    new_incident = RawIncident(raw_payload=incident.raw_payload, source=incident.source)
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident

@router.post("/incident/{incident_id}/process", response_model=ProcessedIncidentResponse)
async def process_raw_incident(incident_id: int, db: Session = Depends(get_db)):
    raw = db.query(RawIncident).filter(RawIncident.id == incident_id).first()
    if not raw:
        raise NotFoundException(
            message="Raw incident not found",
            details=f"No incident with id {incident_id}"
        )

    existing = db.query(ParsedIncident).filter(ParsedIncident.raw_incident_id == incident_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="This incident has already been processed")

    service = IncidentService(db)
    parsed, final_state = await service.process_incident(raw)

    return ProcessedIncidentResponse(
    id=parsed.id, raw_incident_id=parsed.raw_incident_id,
    service_name=parsed.service_name, error_type=parsed.error_type,
    stack_trace=parsed.stack_trace, endpoint=parsed.endpoint,
    occurrence_count=parsed.occurrence_count, occurred_at=parsed.occurred_at,
    parsed_at=parsed.parsed_at, severity_hint=parsed.severity_hint,
    root_cause_hypothesis=final_state.get("root_cause_hypothesis"),
    root_cause_confidence=final_state.get("root_cause_confidence"),
    root_cause_retry_count=final_state.get("root_cause_retry_count"),
    rag_grounded=final_state.get("rag_grounded"),
    severity_level=final_state.get("severity_level"),
    severity_reasoning=final_state.get("severity_reasoning"),
    severity_confidence=final_state.get("severity_confidence"),
    suggested_fix=final_state.get("suggested_fix"),
    fix_confidence=final_state.get("fix_confidence"),
    github_issue_body=final_state.get("github_issue_body"),
    github_issue_url=final_state.get("github_issue_url"),
    github_issue_number=final_state.get("github_issue_number"),
)