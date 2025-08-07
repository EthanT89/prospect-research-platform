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
        logger.info(f"Research requested for company: {request.company_name}")
        
        # Import and use the real research agent
        from ..agents.research.company_research_agent import CompanyResearchAgent
        
        # Execute research
        agent = CompanyResearchAgent()
        result = await agent.execute({
            "company_name": request.company_name,
            "domain": request.domain
        })
        
        return CompanyResearchResponse(
            research_id=result.get("research_id", "unknown"),
            company_id=result.get("insights", {}).get("company_profile", {}).get("name", "unknown"),
            status=result.get("status", "completed"),
            message=f"Research completed for {request.company_name} in {result.get('processing_time_ms', 0)}ms"
        )
        
    except Exception as e:
        logger.error(f"Company research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/{research_id}/results")
async def get_research_results(research_id: str):
    """Get detailed research results by research ID."""
    try:
        # For now, return mock detailed results
        # In production, this would query the database
        return {
            "research_id": research_id,
            "status": "completed",
            "insights": {
                "company_profile": {
                    "name": "Example Company",
                    "industry": "Technology",
                    "description": "A technology company focused on innovation"
                },
                "business_intelligence": {
                    "business_model": {"type": "B2B SaaS"},
                    "revenue_model": ["Subscription", "Professional Services"]
                },
                "outreach_opportunities": {
                    "pain_points": ["Scaling operations", "Customer acquisition"],
                    "timing_triggers": ["Recent funding round", "Product launches"]
                }
            },
            "confidence_score": 0.85
        }
    except Exception as e:
        logger.error(f"Failed to get research results: {e}")
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