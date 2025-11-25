"""
Configuration management for DevOpsMCP
Loads environment variables and provides application settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration - SQLite
    db_path: str = "devops_mcp.db"
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
    
    @property
    def database_path(self) -> str:
        """Get absolute path to SQLite database"""
        if os.path.isabs(self.db_path):
            return self.db_path
        # If relative path, create in project root
        project_root = Path(__file__).parent.parent
        return str(project_root / self.db_path)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
