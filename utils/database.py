from supabase import create_client, Client
from config.settings import settings
from utils.logger import setup_logger
from typing import Optional
import asyncio

logger = setup_logger("database")

class SupabaseClient:
    """Singleton Supabase client with connection management."""
    
    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> 'SupabaseClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def client(self) -> Client:
        """Get or create Supabase client."""
        if self._client is None:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_anon_key
            )
            logger.info("Supabase client initialized")
        return self._client
    
    async def health_check(self) -> bool:
        """Check if Supabase connection is healthy."""
        try:
            # Simple query to test connection
            result = self.client.table('_health_check').select('*').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase health check failed: {e}")
            return False

# Global database instance
db = SupabaseClient()