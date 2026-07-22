from datetime import datetime, timezone
from fastapi import Request
from typing import Dict,Any
from fastapi.responses import JSONResponse
from app.core.logger import logger
from app.base_exception import SentinelException
import traceback

def _now():
    return datetime.now(timezone.utc).isoformat()

def _request_id(request:Request) -> str:
    return getattr(request.state, "request_id", "unknown") 

def _error_body(code: str, message: str, request: Request, details:str | None = None) -> Dict[str,Any]:
    return {
        "status": "error",
        "error": {"code": code, "message": message, "details": details},
        "request_id": _request_id(request),
        "timestamp": _now(),
    }

async def app_exception_handler(request: Request, exc: Exception):

    if not isinstance(exc, SentinelException):
        raise exc
    
    logger.warning(
        f"SentinelException | request_id={_request_id(request)} | "
        f"code={exc.code} | message={exc.message} | path={request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.code, exc.message, request, exc.details),
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    
    logger.critical(
        f"UnhandledException | request_id={_request_id(request)} | "
        f"path={request.url.path} | error={str(exc)}\n{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content=_error_body("INTERNAL_SERVER_ERROR", "An unexpected error occurred", request),
    )
