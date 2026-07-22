from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.incident_router import router as raw_incident_router
from app.api.health.router import router as health_router
import uvicorn
from app.core.exception.middleware import RequestIDMiddleware
from app.core.exception.base_exception import SentinelException
from fastapi.exceptions import HTTPException
from app.core.exception.exception_handler import app_exception_handler, unhandled_exception_handler,http_exception_handler

app = FastAPI(title = "Sentinel - Incident Response System",
              description= "Autonomous multi-agent incident response system using LangGraph, MCP, and LLMs — diagnoses production errors, classifies severity, and auto-files GitHub issues.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)

app.add_exception_handler(SentinelException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(HTTPException,http_exception_handler)

app.include_router(raw_incident_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8001,reload=True)
