"""
Configuration management for DevOpsMCP
Loads environment variables and provides application settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    db_host: str
    db_name: str
    db_user: str
    db_pass: str
    db_port: int = 1433
    
    # Azure DevOps Configuration
    azure_devops_base_url: str = "https://dev.azure.com"
    azure_devops_org: str = ""
    azure_devops_project: str = ""
    azure_devops_pat: str = ""
    azure_devops_access_token: str = ""
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_connection_string(self) -> str:
        """Generate Azure SQL connection string"""
        return (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={self.db_host},{self.db_port};"
            f"DATABASE={self.db_name};"
            f"UID={self.db_user};"
            f"PWD={self.db_pass};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
