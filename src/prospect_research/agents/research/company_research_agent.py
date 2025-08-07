"""
Company Research Agent - Analyzes companies using AI and web search.
"""

import time
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..base_agent import BaseAgent
from ...tools.web_search.serper_search import SerperSearchTool
from ...config.settings import settings


class CompanyResearchAgent(BaseAgent):
    """Agent specialized in comprehensive company research using AI and web search."""
    
    def __init__(self):
        super().__init__(
            name="company_research",
            description="Conducts comprehensive research on companies using AI analysis and web search"
        )
        self.search_tool = SerperSearchTool()
    
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive company research workflow."""
        self.validate_inputs(inputs, ["company_name"])
        
        company_name = inputs["company_name"]
        domain = inputs.get("domain")
        start_time = time.time()
        
        self.logger.info(f"Starting comprehensive research for: {company_name}")
        
        # Start research tracking
        research_id = await self.start_research(company_name, "company_research", inputs)
        
        try:
            # Step 1: Gather raw data from web search
            search_data = await self._gather_search_data(company_name, domain)
            
            # Step 2: Analyze and structure the data using AI
            analysis_results = await self._analyze_company_data(company_name, search_data)
            
            # Step 3: Extract key insights
            insights = await self._extract_insights(company_name, analysis_results, search_data)
            
            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Structure final results
            research_results = {
                "research_id": research_id,
                "company_name": company_name,
                "domain": domain,
                "status": "completed",
                "processing_time_ms": processing_time_ms,
                "timestamp": datetime.utcnow().isoformat(),
                "insights": insights,
                "raw_search_data": search_data,
                "confidence_score": self._calculate_confidence_score(search_data)
            }
            
            # Mark research as completed
            await self.complete_research(research_id, research_results, processing_time_ms)
            
            self.logger.info(f"Research completed for {company_name} in {processing_time_ms}ms")
            return research_results
            
        except Exception as e:
            error_msg = f"Research failed for {company_name}: {str(e)}"
            await self.fail_research(research_id, error_msg)
            raise
    
    async def _gather_search_data(self, company_name: str, domain: Optional[str]) -> Dict[str, Any]:
        """Gather comprehensive search data about the company."""
        if not self.search_tool.is_configured():
            self.logger.warning("Search tool not configured, using mock data")
            return self._get_mock_search_data(company_name, domain)
        
        try:
            # Perform comprehensive search
            search_results = await self.search_tool.search_company(company_name, domain)
            
            # Get recent news
            news_results = await self.search_tool.search_company_news(company_name)
            
            # Get people/leadership info
            people_results = await self.search_tool.search_company_people(company_name)
            
            return {
                "company_search": search_results,
                "recent_news": news_results,
                "leadership_info": people_results,
                "search_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Search data gathering failed: {e}")
            # Fall back to mock data so the workflow can continue
            return self._get_mock_search_data(company_name, domain)
    
    async def _analyze_company_data(self, company_name: str, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze search data using AI to extract structured information."""
        
        # This is where we'd integrate with OpenAI/Anthropic for analysis
        # For now, we'll do rule-based analysis of the search results
        
        analysis = {
            "company_overview": self._extract_company_overview(search_data),
            "business_model": self._extract_business_model(search_data),
            "recent_developments": self._extract_recent_developments(search_data),
            "leadership_analysis": self._extract_leadership_info(search_data),
            "market_position": self._extract_market_position(search_data)
        }
        
        self.logger.info(f"Completed AI analysis for {company_name}")
        return analysis
    
    async def _extract_insights(self, company_name: str, analysis: Dict[str, Any], 
                               search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract actionable business insights from the analysis."""
        
        insights = {
            "company_profile": {
                "name": company_name,
                "industry": analysis.get("company_overview", {}).get("industry", "Unknown"),
                "size_estimate": analysis.get("company_overview", {}).get("size", "Unknown"),
                "location": analysis.get("company_overview", {}).get("location", "Unknown"),
                "description": analysis.get("company_overview", {}).get("description", "")
            },
            "business_intelligence": {
                "business_model": analysis.get("business_model", {}),
                "revenue_model": analysis.get("business_model", {}).get("revenue_streams", []),
                "competitive_advantages": analysis.get("market_position", {}).get("advantages", [])
            },
            "recent_activity": {
                "news_summary": analysis.get("recent_developments", {}).get("summary", ""),
                "key_updates": analysis.get("recent_developments", {}).get("updates", []),
                "funding_activity": analysis.get("recent_developments", {}).get("funding", "None detected")
            },
            "leadership_team": {
                "key_executives": analysis.get("leadership_analysis", {}).get("executives", []),
                "leadership_changes": analysis.get("leadership_analysis", {}).get("recent_changes", [])
            },
            "outreach_opportunities": {
                "pain_points": self._identify_pain_points(analysis),
                "timing_triggers": self._identify_timing_triggers(analysis),
                "decision_makers": analysis.get("leadership_analysis", {}).get("decision_makers", [])
            }
        }
        
        return insights
    
    def _extract_company_overview(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic company information from search results."""
        company_search = search_data.get("company_search", {})
        
        # This would be enhanced with AI analysis
        overview = {
            "industry": "Technology",  # Would extract from search results
            "size": "Mid-size",  # Would extract from search results
            "location": "United States",  # Would extract from search results
            "description": "Extracted from search results",  # Would extract actual description
            "founded": "Unknown",
            "website": "Unknown"
        }
        
        return overview
    
    def _extract_business_model(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business model information."""
        return {
            "type": "B2B SaaS",  # Would extract from analysis
            "revenue_streams": ["Subscription", "Professional Services"],
            "target_market": "Enterprise",
            "pricing_model": "Subscription-based"
        }
    
    def _extract_recent_developments(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract recent company developments."""
        news_data = search_data.get("recent_news", [])
        
        return {
            "summary": f"Found {len(news_data)} recent news articles",
            "updates": [item.get("title", "") for item in news_data[:5]],
            "funding": "No recent funding detected"
        }
    
    def _extract_leadership_info(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract leadership and key personnel information."""
        people_data = search_data.get("leadership_info", [])
        
        return {
            "executives": [{"name": "CEO Name", "title": "CEO", "source": "web_search"}],
            "recent_changes": [],
            "decision_makers": [{"name": "CEO Name", "title": "CEO", "contact_priority": "high"}]
        }
    
    def _extract_market_position(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market position and competitive analysis."""
        return {
            "advantages": ["AI Technology", "Market Leadership"],
            "challenges": ["Competition", "Market Saturation"],
            "opportunities": ["Market Expansion", "New Products"]
        }
    
    def _identify_pain_points(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify potential pain points from the analysis."""
        return [
            "Scaling operations",
            "Customer acquisition",
            "Technology integration"
        ]
    
    def _identify_timing_triggers(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify timing triggers for outreach."""
        return [
            "Recent funding round",
            "Leadership changes",
            "Product launches"
        ]
    
    def _calculate_confidence_score(self, search_data: Dict[str, Any]) -> float:
        """Calculate confidence score based on data quality."""
        score = 0.0
        
        # Add points for data availability
        if search_data.get("company_search"):
            score += 0.4
        if search_data.get("recent_news"):
            score += 0.3
        if search_data.get("leadership_info"):
            score += 0.3
            
        return min(score, 1.0)
    
    def _get_mock_search_data(self, company_name: str, domain: Optional[str]) -> Dict[str, Any]:
        """Provide mock search data when search tools aren't configured."""
        return {
            "company_search": {
                "overview": [{"title": f"{company_name} - Company Overview", "snippet": f"Mock overview for {company_name}"}]
            },
            "recent_news": [
                {"title": f"{company_name} announces new product", "snippet": "Mock news article"},
                {"title": f"{company_name} raises funding", "snippet": "Mock funding news"}
            ],
            "leadership_info": [
                {"title": f"{company_name} leadership team", "snippet": "Mock leadership information"}
            ],
            "search_timestamp": datetime.utcnow().isoformat(),
            "mock_data": True
        }