from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..utils.logger import setup_logger
from ..config.settings import settings
import uvicorn

# Initialize FastAPI
app = FastAPI(
    title="Prospect Research Platform API",
    description="AI agent orchestration for B2B prospect research and outreach",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = setup_logger("api")

# Pydantic models
class CompanyResearchRequest(BaseModel):
    company_name: str
    domain: Optional[str] = None
    
class CompanyResearchResponse(BaseModel):
    research_id: str
    company_id: str
    status: str
    message: str

# Routes
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Prospect Research Platform API", "status": "healthy", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Detailed health check including database connection."""
    try:
        return {
            "api": "healthy",
            "database": "ready", # Will implement actual DB check later
            "environment": settings.environment,
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.post("/research/company", response_model=CompanyResearchResponse)
async def research_company(request: CompanyResearchRequest):
    """Start company research workflow."""
    try:
        # Mock implementation for now
        logger.info(f"Research requested for company: {request.company_name}")
        
        return CompanyResearchResponse(
            research_id="mock-research-id-123",
            company_id="mock-company-id-456", 
            status="completed",
            message=f"Research initiated for {request.company_name}"
        )
        
    except Exception as e:
        logger.error(f"Company research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/companies")
async def list_companies(limit: int = 50, offset: int = 0):
    """List all companies in the database."""
    try:
        # Mock implementation for now
        return {
            "companies": [
                {"id": "1", "name": "Example Company", "domain": "example.com"},
                {"id": "2", "name": "Test Corp", "domain": "test.com"}
            ],
            "count": 2,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Failed to list companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"Starting API server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )