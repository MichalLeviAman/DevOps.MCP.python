"""
Simple demo version of DevOpsMCP without database dependency
For quick testing and Cloud Run deployment
"""
import logging
import sys
import random
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


# Schemas
class GetBugFixTrendsRequest(BaseModel):
    """בקשה לקבלת נתוני באגים - project_id הוא אופציונלי!"""
    days_back: int = Field(
        default=10, 
        ge=1, 
        le=365,
        description="מספר ימים לאחור (1-365)"
    )
    project_id: Optional[str] = Field(
        default=None,
        description="מזהה פרויקט - אופציונלי! אפשר לשלוח בלי"
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {"days_back": 7},
                {"days_back": 14, "project_id": "PROJ001"},
                {"days_back": 30, "project_id": "MyProject"}
            ]
        }


class DailyTrend(BaseModel):
    date: str
    fixed_count: int


class TrendGraphData(BaseModel):
    labels: list[str]
    values: list[int]


class GetBugFixTrendsResponse(BaseModel):
    total_fixed_bugs: int
    daily_aggregation: list[DailyTrend]
    trend_graph_data: TrendGraphData
    sql_query: str
    period_start: str
    period_end: str
    project_id: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting DevOpsMCP Demo application...")
    logger.info("✅ Running in demo mode (no database required)")
    yield
    logger.info("👋 Shutting down DevOpsMCP...")


# Create FastAPI application
app = FastAPI(
    title="DevOpsMCP Demo",
    description="Model Context Protocol API for DevOps Analytics - Demo Version",
    version="1.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "DevOpsMCP Demo",
        "version": "1.0.1",
        "description": "Model Context Protocol API for DevOps Analytics",
        "status": "✅ Running in demo mode",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "health_url": "/health"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api": "operational",
        "mode": "demo",
        "timestamp": datetime.now().isoformat()
    }


@app.post(
    "/api/bugs/get_bug_fix_trends",
    response_model=GetBugFixTrendsResponse,
    summary="Get Bug Fix Trends",
    description="Returns demo bug fix trends data"
)
async def get_bug_fix_trends(request: GetBugFixTrendsRequest) -> GetBugFixTrendsResponse:
    """
    Get bug fix trends - Demo version with sample data
    
    Parameters:
    - days_back: מספר ימים לאחור (ברירת מחדל: 10)
    - project_id: מזהה פרויקט אופציונלי (אפשר להשאיר ריק!)
    
    דוגמה:
    {"days_back": 7} - רק עם ימים
    {"days_back": 14, "project_id": "PROJ001"} - עם פרויקט
    """
    logger.info(f"📊 Getting bug fix trends: days_back={request.days_back}, project_id={request.project_id}")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=request.days_back)
    
    # Generate sample data
    daily_aggregation = []
    total_fixed = 0
    
    current_date = start_date
    while current_date <= end_date:
        # Simulate varying bug fix counts (demo data)
        fixed_count = random.randint(0, 8)
        
        daily_aggregation.append(DailyTrend(
            date=current_date.strftime('%Y-%m-%d'),
            fixed_count=fixed_count
        ))
        total_fixed += fixed_count
        current_date += timedelta(days=1)
    
    # Prepare trend graph data
    trend_graph_data = TrendGraphData(
        labels=[trend.date for trend in daily_aggregation],
        values=[trend.fixed_count for trend in daily_aggregation]
    )
    
    sql_query = f"SELECT * FROM Bugs WHERE ClosedAt >= '{start_date}' AND ProjectId = '{request.project_id or 'ALL'}'"
    
    logger.info(f"✅ Generated demo data: {total_fixed} bugs fixed")
    
    return GetBugFixTrendsResponse(
        total_fixed_bugs=total_fixed,
        daily_aggregation=daily_aggregation,
        trend_graph_data=trend_graph_data,
        sql_query=sql_query,
        period_start=start_date.strftime('%Y-%m-%d'),
        period_end=end_date.strftime('%Y-%m-%d'),
        project_id=request.project_id
    )


@app.get("/api/bugs/health")
async def bugs_health():
    """Bugs API health check"""
    return {
        "status": "healthy",
        "service": "bugs",
        "mode": "demo",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "app.main_demo:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
