from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Supabase Configuration
    supabase_url: str = Field("https://example.supabase.co", env="SUPABASE_URL")
    supabase_anon_key: str = Field("example_anon_key", env="SUPABASE_ANON_KEY") 
    supabase_service_role_key: str = Field("example_service_role_key", env="SUPABASE_SERVICE_ROLE_KEY")
    
    # AI Configuration
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Web Search Configuration
    serper_api_key: Optional[str] = Field(None, env="SERPER_API_KEY")
    brave_api_key: Optional[str] = Field(None, env="BRAVE_API_KEY")
    
    # GitHub Integration
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    
    # Application Settings
    log_level: str = Field("INFO", env="LOG_LEVEL")
    environment: str = Field("development", env="ENVIRONMENT")
    
    # Rate Limiting
    max_requests_per_minute: int = Field(60, env="MAX_REQUESTS_PER_MINUTE")
    
    # API Settings
    api_host: str = Field("127.0.0.1", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()