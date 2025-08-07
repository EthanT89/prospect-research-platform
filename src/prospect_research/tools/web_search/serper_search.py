"""
Serper web search tool for company research.
Uses Serper API for Google search results.
"""

import httpx
import json
from typing import Dict, List, Any, Optional
from ...config.settings import settings
from ...utils.logger import setup_logger

logger = setup_logger("tools.serper_search")

class SerperSearchTool:
    """Web search tool using Serper API for Google search results."""
    
    def __init__(self):
        self.api_key = settings.serper_api_key
        self.base_url = "https://google.serper.dev/search"
        
        if not self.api_key:
            logger.warning("Serper API key not found in environment variables")
    
    async def search_company(self, company_name: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """Search for comprehensive company information."""
        search_queries = [
            f"{company_name} company overview",
            f"{company_name} recent news 2024",
            f"{company_name} leadership team executives",
            f"{company_name} funding revenue business model",
        ]
        
        if domain:
            search_queries.append(f"site:{domain} about company")
        
        all_results = {}
        
        for query in search_queries:
            try:
                results = await self._perform_search(query)
                query_key = query.split()[-1]  # Use last word as key
                all_results[query_key] = results
                logger.info(f"Successfully searched: {query}")
            except Exception as e:
                logger.error(f"Search failed for '{query}': {e}")
                all_results[query.split()[-1]] = {"error": str(e)}
        
        return all_results
    
    async def search_company_news(self, company_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """Search for recent company news and updates."""
        query = f"{company_name} news recent updates past {days} days"
        
        try:
            results = await self._perform_search(query)
            return results.get("organic", [])[:10]  # Return top 10 news results
        except Exception as e:
            logger.error(f"News search failed for {company_name}: {e}")
            return []
    
    async def search_company_people(self, company_name: str) -> List[Dict[str, Any]]:
        """Search for company leadership and key personnel."""
        queries = [
            f"{company_name} CEO founder leadership team",
            f"{company_name} executives management team",
            f"{company_name} board of directors"
        ]
        
        people_results = []
        
        for query in queries:
            try:
                results = await self._perform_search(query)
                organic_results = results.get("organic", [])
                people_results.extend(organic_results[:3])  # Top 3 from each query
            except Exception as e:
                logger.error(f"People search failed for '{query}': {e}")
        
        return people_results[:10]  # Return top 10 overall
    
    async def _perform_search(self, query: str) -> Dict[str, Any]:
        """Perform the actual search request to Serper API."""
        if not self.api_key:
            raise ValueError("Serper API key not configured")
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": 10  # Number of results
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.json()
    
    def is_configured(self) -> bool:
        """Check if the tool is properly configured."""
        return bool(self.api_key)