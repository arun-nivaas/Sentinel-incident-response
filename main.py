from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.incident_router import router as raw_incident_router
import uvicorn

app = FastAPI(title = "Sentinel - Incident Response System",
              description= "Autonomous multi-agent incident response system using LangGraph, MCP, and LLMs — diagnoses production errors, classifies severity, and auto-files GitHub issues.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(raw_incident_router)

if __name__ == "__main__":
   
    uvicorn.run("main:app",host="127.0.0.1",port=8001,reload=True)
