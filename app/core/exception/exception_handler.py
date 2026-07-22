from datetime import datetime, timezone
from fastapi import Request
from typing import Dict,Any,cast
from fastapi.responses import JSONResponse
from app.core.logger import logger
from app.core.exception.base_exception import SentinelException
from fastapi.exceptions import HTTPException as FastAPIHTTPException
import traceback

def _now():
    return datetime.now(timezone.utc).isoformat()

def _request_id(request:Request) -> str:
    return getattr(request.state, "request_id", "unknown") 

def _with_request_id_header(response: JSONResponse, request: Request) -> JSONResponse:
    response.headers["X-Request-ID"] = _request_id(request)
    return response

def _error_body(code: str, message: str, request: Request, details:str | None = None) -> Dict[str,Any]:
    return {
        "status": "error",
        "error": {"code": code, "message": message, "details": details},
        "request_id": _request_id(request),
        "timestamp": _now(),
    }

async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    if not isinstance(exc, SentinelException):
        raise exc
    
    logger.warning(
        f"SentinelException | request_id={_request_id(request)} | "
        f"code={exc.code} | message={exc.message} | path={request.url.path}"
    )
    response = JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.code, exc.message, request, exc.details),
    )
    return _with_request_id_header(response, request)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.critical(
        f"UnhandledException | request_id={_request_id(request)} | "
        f"path={request.url.path} | error={str(exc)}\n{traceback.format_exc()}"
    )
    response = JSONResponse(
        status_code=500,
        content=_error_body("INTERNAL_SERVER_ERROR", "An unexpected error occurred", request),
    )
    return _with_request_id_header(response, request)


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    exc = cast(FastAPIHTTPException, exc)
    logger.warning(
        f"HTTPException | request_id={_request_id(request)} | "
        f"status={exc.status_code} | detail={exc.detail} | path={request.url.path}"
    )
    response = JSONResponse(
        status_code=exc.status_code,
        content=_error_body("HTTP_ERROR", str(exc.detail), request),
    )
    return _with_request_id_header(response, request)