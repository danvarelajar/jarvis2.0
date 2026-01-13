"""
FastAPI Backend for Vulnerable-by-Design AI Agent Laboratory
Integrates CopilotKit Runtime, Opik Observability, and CrewAI
"""

import os
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from copilotkit.runtime import CopilotRuntime
from opik import Opik, configure_opik
from pydantic import BaseModel

from app.crew import execute_user_request

# Initialize FastAPI app
app = FastAPI(
    title="Vulnerable AI Agent Laboratory",
    description="Educational platform demonstrating OWASP Top 10 LLM and MCP vulnerabilities",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Opik for observability
OPIK_API_KEY = os.getenv("OPIK_API_KEY", "")
OPIK_ENDPOINT = os.getenv("OPIK_ENDPOINT", "https://api.opik.ai")

# Support both cloud (with API key) and local (without API key) Opik instances
# For local Opik, set OPIK_ENDPOINT to your local instance (e.g., http://localhost:5173)
# and leave OPIK_API_KEY empty or set to a dummy value
if OPIK_ENDPOINT and OPIK_ENDPOINT != "https://api.opik.ai":
    # Local Opik instance - may not require API key
    configure_opik(
        api_key=OPIK_API_KEY or "local",
        endpoint=OPIK_ENDPOINT,
        service_name="vulnerable-ai-lab",
        environment="educational"
    )
    opik = Opik()
elif OPIK_API_KEY:
    # Cloud Opik instance - requires API key
    configure_opik(
        api_key=OPIK_API_KEY,
        endpoint=OPIK_ENDPOINT,
        service_name="vulnerable-ai-lab",
        environment="educational"
    )
    opik = Opik()
else:
    opik = None
    print("WARNING: OPIK not configured. Set OPIK_ENDPOINT for local or OPIK_API_KEY for cloud.")

# Initialize CopilotKit Runtime
copilot_runtime = CopilotRuntime()

# Get project root for MCP filesystem access
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()


class UserRequest(BaseModel):
    """User request model"""
    message: str
    thread_id: str | None = None


class AgentResponse(BaseModel):
    """Agent response model"""
    response: str
    trace_id: str | None = None
    thread_id: str | None = None
    opik_dashboard_url: str | None = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Vulnerable-by-Design AI Agent Laboratory",
        "status": "operational",
        "vulnerabilities": [
            "LLM01: Prompt Injection",
            "MCP02: Privilege Escalation",
            "MCP05: Command Injection",
            "LLM06: Excessive Agency"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "opik_configured": opik is not None}


@app.post("/api/agent/execute", response_model=AgentResponse)
async def execute_agent(request: UserRequest) -> AgentResponse:
    """
    Execute a user request through the vulnerable NaiveClerk agent.
    
    This endpoint demonstrates multiple vulnerabilities:
    - LLM01: No input sanitization
    - LLM06: No human approval required
    - MCP02: Full filesystem access
    - MCP05: Command injection possible
    """
    try:
        # Execute the request through the vulnerable flow (synchronous, run in thread pool)
        import asyncio
        result = await asyncio.to_thread(
            execute_user_request,
            request.message,
            PROJECT_ROOT
        )
        
        # Build Opik dashboard URL if trace_id is available
        opik_url = None
        if result.get("trace_id") and opik:
            opik_url = f"{OPIK_ENDPOINT}/traces/{result['trace_id']}"
        
        return AgentResponse(
            response=str(result.get("result", "No response generated")),
            trace_id=result.get("trace_id"),
            thread_id=result.get("thread_id"),
            opik_dashboard_url=opik_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


# Register CopilotKit endpoints
@app.post("/api/copilotkit/chat")
async def copilotkit_chat(request: Dict[str, Any]):
    """CopilotKit chat endpoint"""
    # This integrates with the CopilotKit Runtime
    # The actual agent execution happens through execute_agent
    return await copilot_runtime.process_chat_request(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
