"""
Request and response schemas for bug-related endpoints
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class GetBugFixTrendsRequest(BaseModel):
    """Request schema for getting bug fix trends"""
    days_back: int = Field(default=10, ge=1, le=365, description="Number of days to look back")
    project_id: Optional[str] = Field(default=None, description="Optional project ID filter")
    
    class Config:
        json_schema_extra = {
            "example": {
                "days_back": 10,
                "project_id": "PROJ001"
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
