from fastapi import APIRouter,status
from fastapi.responses import JSONResponse
from typing import Dict,Any

router = APIRouter(prefix="/health",tags=["Health"])

@router.get("/live", summary="Liveness probe")
async def liveness():
    """
    Confirms the process is running and can respond.
    No dependency checks here — keep this fast, always DB-free.
    """
    return {"status": "ok"}


@router.get("/ready", summary="Readiness probe")
async def readiness():
    """
    Placeholder for now — no dependencies connected yet.
    Once DB/Redis/etc. are added, checks go here (see readiness template below).
    """
    checks:Dict[str,Any] = {}  # e.g. will become {"database": True, "pgvector": True}

    all_ok = all(checks.values()) if checks else True

    return JSONResponse(
        status_code=status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "ok" if all_ok else "unhealthy", "checks": checks},
    )


@router.get("", summary="Generic health alias")
async def health():
    return {"status": "ok"}