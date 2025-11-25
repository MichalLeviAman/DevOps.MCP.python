"""
Request and response schemas for bug-related endpoints
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class GetBugFixTrendsRequest(BaseModel):
    """Request schema for getting bug fix trends"""
    days_back: int = Field(default=10, ge=1, le=365, description="Number of days to look back")
    project_id: Optional[str] = Field(default=None, description="Optional project ID filter (numeric)")
    project_name: Optional[str] = Field(default=None, description="Optional project name filter (e.g., 'HotRetailSys')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "days_back": 10,
                "project_id": "1"
            }
        }


class DailyTrend(BaseModel):
    """Daily bug fix trend data"""
    date: str
    fixed_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-11-15",
                "fixed_count": 5
            }
        }


class TrendGraphData(BaseModel):
    """Trend graph visualization data"""
    labels: List[str]
    values: List[int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "labels": ["2025-11-11", "2025-11-12", "2025-11-13"],
                "values": [3, 5, 2]
            }
        }


class GetBugFixTrendsResponse(BaseModel):
    """Response schema for bug fix trends"""
    total_fixed_bugs: int = Field(description="Total number of bugs fixed in the period")
    daily_aggregation: List[DailyTrend] = Field(description="Daily breakdown of fixed bugs")
    trend_graph_data: TrendGraphData = Field(description="Data formatted for chart visualization")
    sql_query: str = Field(description="SQL query used to fetch the data")
    period_start: str = Field(description="Start date of the analysis period")
    period_end: str = Field(description="End date of the analysis period")
    project_id: Optional[str] = Field(default=None, description="Project ID filter applied")
    project_name: Optional[str] = Field(default=None, description="Project name filter applied")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_fixed_bugs": 15,
                "daily_aggregation": [
                    {"date": "2025-11-11", "fixed_count": 3},
                    {"date": "2025-11-12", "fixed_count": 5}
                ],
                "trend_graph_data": {
                    "labels": ["2025-11-11", "2025-11-12"],
                    "values": [3, 5]
                },
                "sql_query": "SELECT ...",
                "period_start": "2025-11-11",
                "period_end": "2025-11-20",
                "project_id": "PROJ001"
            }
        }


class GetActiveBugsRequest(BaseModel):
    """Request schema for getting active bugs"""
    project_id: Optional[str] = Field(default=None, description="Optional project ID filter (numeric)")
    project_name: Optional[str] = Field(default=None, description="Optional project name filter (e.g., 'HotRetailSys')")
    severity: Optional[str] = Field(default=None, description="Filter by severity (Low, Medium, High, Critical)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "1",
                "severity": "High"
            }
        }


class BugItem(BaseModel):
    """Individual bug item"""
    bug_id: int
    azure_bug_id: str
    title: str
    severity: Optional[str]
    status: str
    created_date: Optional[str]
    notes: Optional[str]


class GetActiveBugsResponse(BaseModel):
    """Response schema for active bugs"""
    total_active_bugs: int
    bugs: List[BugItem]
    filters_applied: Dict[str, Any]
    project_id: Optional[str] = Field(default=None, description="Project ID if filtered")
    project_name: Optional[str] = Field(default=None, description="Project name if filtered")
    

class GetBugsByStatusRequest(BaseModel):
    """Request schema for getting bugs by status"""
    status: str = Field(description="Bug status (Active, Closed, New)")
    project_id: Optional[str] = Field(default=None, description="Optional project ID filter (numeric)")
    project_name: Optional[str] = Field(default=None, description="Optional project name filter (e.g., 'HotRetailSys')")
    limit: int = Field(default=50, ge=1, le=500, description="Maximum number of results")


class GetBugsByStatusResponse(BaseModel):
    """Response schema for bugs by status"""
    status: str
    total_count: int
    bugs: List[BugItem]
    project_id: Optional[str] = Field(default=None, description="Project ID if filtered")
    project_name: Optional[str] = Field(default=None, description="Project name if filtered")


class GetBugStatisticsRequest(BaseModel):
    """Request schema for bug statistics"""
    project_id: Optional[str] = Field(default=None, description="Optional project ID filter (numeric)")
    project_name: Optional[str] = Field(default=None, description="Optional project name filter (e.g., 'HotRetailSys')")


class BugStatistics(BaseModel):
    """Bug statistics summary"""
    total_bugs: int
    active_bugs: int
    closed_bugs: int
    new_bugs: int
    by_severity: Dict[str, int]
    by_project: List[Dict[str, Any]]


class GetBugStatisticsResponse(BaseModel):
    """Response schema for bug statistics"""
    statistics: BugStatistics
    generated_at: str
    project_id: Optional[str] = Field(default=None, description="Project ID if filtered")
    project_name: Optional[str] = Field(default=None, description="Project name if filtered")
