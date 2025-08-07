"""
Base agent class with Supabase integration and research tracking.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import time
import uuid

from ..utils.logger import setup_logger
from ..utils.database import db


class BaseAgent(ABC):
    """Abstract base class for all agents with Supabase integration."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.logger = setup_logger(f"agent.{name}")
    
    async def start_research(self, company_name: str, research_type: str, input_data: Dict[str, Any]) -> str:
        """Start research tracking and return research_id."""
        try:
            # Find or create company record
            company_id = await self._find_or_create_company(company_name, input_data.get('domain'))
            
            # Create research record
            research_record = {
                'id': str(uuid.uuid4()),
                'company_id': company_id,
                'research_type': research_type,
                'status': 'processing',
                'input_data': input_data,
                'agent_workflow': self.name,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            # Note: This will fail gracefully if Supabase isn't configured
            try:
                result = db.client.table('research_results').insert(research_record).execute()
                research_id = research_record['id']
                self.logger.info(f"Research started: {research_id}")
                return research_id
            except Exception as db_error:
                self.logger.warning(f"Database insert failed, using mock ID: {db_error}")
                return research_record['id']  # Return the ID we generated
            
        except Exception as e:
            self.logger.error(f"Failed to start research tracking: {e}")
            # Return a mock ID so the process can continue
            return f"mock-research-{int(time.time())}"
    
    async def complete_research(self, research_id: str, output_data: Dict[str, Any], 
                               processing_time_ms: int, cost_cents: int = 0) -> None:
        """Mark research as completed with results."""
        try:
            update_data = {
                'status': 'completed',
                'output_data': output_data,
                'processing_time_ms': processing_time_ms,
                'cost_cents': cost_cents,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            try:
                db.client.table('research_results').update(update_data).eq('id', research_id).execute()
                self.logger.info(f"Research completed: {research_id}")
            except Exception as db_error:
                self.logger.warning(f"Database update failed: {db_error}")
            
        except Exception as e:
            self.logger.error(f"Failed to complete research tracking: {e}")
    
    async def fail_research(self, research_id: str, error_message: str) -> None:
        """Mark research as failed."""
        try:
            update_data = {
                'status': 'failed',
                'output_data': {'error': error_message, 'timestamp': datetime.utcnow().isoformat()},
                'updated_at': datetime.utcnow().isoformat()
            }
            
            try:
                db.client.table('research_results').update(update_data).eq('id', research_id).execute()
                self.logger.error(f"Research failed: {research_id} - {error_message}")
            except Exception as db_error:
                self.logger.warning(f"Database update failed: {db_error}")
                
        except Exception as e:
            self.logger.error(f"Failed to record research failure: {e}")
    
    async def _find_or_create_company(self, company_name: str, domain: Optional[str] = None) -> str:
        """Find existing company or create new one. Returns company_id."""
        try:
            # Try to find existing company
            try:
                result = db.client.table('companies').select('*').eq('name', company_name).execute()
                
                if result.data and len(result.data) > 0:
                    company_id = result.data[0]['id']
                    self.logger.info(f"Found existing company: {company_id}")
                    return company_id
            except Exception as db_error:
                self.logger.warning(f"Database query failed: {db_error}")
            
            # Create new company record
            company_record = {
                'id': str(uuid.uuid4()),
                'name': company_name,
                'domain': domain,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            try:
                new_company = db.client.table('companies').insert(company_record).execute()
                company_id = company_record['id']
                self.logger.info(f"Created new company: {company_id}")
                return company_id
            except Exception as db_error:
                self.logger.warning(f"Database insert failed, using mock ID: {db_error}")
                return company_record['id']  # Return the ID we generated
                
        except Exception as e:
            self.logger.error(f"Failed to find/create company: {e}")
            # Return a mock ID so the process can continue
            return f"mock-company-{int(time.time())}"
    
    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's primary function. Must be implemented by subclasses."""
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any], required_keys: List[str]) -> None:
        """Validate that required inputs are present."""
        missing = [key for key in required_keys if key not in inputs]
        if missing:
            raise ValueError(f"Missing required inputs: {missing}")