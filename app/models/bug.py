"""
Database models for Bug entity
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Bug(BaseModel):
    """Bug database model"""
    id: int
    title: Optional[str] = None
    project_id: Optional[str] = None
    created_at: datetime
    closed_at: Optional[datetime] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True


class BugCreate(BaseModel):
    """Model for creating a new bug"""
    title: str
    project_id: Optional[str] = None
    status: str = "Open"


class BugUpdate(BaseModel):
    """Model for updating an existing bug"""
    title: Optional[str] = None
    project_id: Optional[str] = None
    closed_at: Optional[datetime] = None
    status: Optional[str] = None
