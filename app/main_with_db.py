"""
DevOpsMCP with SQLite Database
Full working version with real bug data from Azure DevOps
"""
import logging
import sys
import sqlite3
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from typing import Optional, List
from pathlib import Path
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path(__file__).parent.parent / "devopsmcp.db"


# Schemas
class GetBugFixTrendsRequest(BaseModel):
    """בקשה לקבלת נתוני באגים - project_id או project_name אופציונליים!"""
    days_back: int = Field(
        default=10, 
        ge=1, 
        le=365,
        description="מספר ימים לאחור (1-365)"
    )
    project_id: Optional[int] = Field(
        default=None,
        description="מזהה הפרויקט (מספר) - אופציונלי! לדוגמה: 1 או 2"
    )
    project_name: Optional[str] = Field(
        default=None,
        description="שם הפרויקט (מחרוזת) - אופציונלי! לדוגמה: HotRetailSys או PaymentsGateway"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"days_back": 7},
                {"days_back": 14, "project_id": 1},
                {"days_back": 14, "project_name": "HotRetailSys"},
                {"days_back": 30, "project_id": 2}
            ]
        }
    )


class DailyTrend(BaseModel):
    date: str
    fixed_count: int


class TrendGraphData(BaseModel):
    labels: List[str]
    values: List[int]


class GetBugFixTrendsResponse(BaseModel):
    total_fixed_bugs: int
    daily_aggregation: List[DailyTrend]
    trend_graph_data: TrendGraphData
    sql_query: str
    period_start: str
    period_end: str
    project_id: Optional[str] = None
    project_name: Optional[str] = None


class BugSummary(BaseModel):
    """סיכום באג"""
    bug_id: int
    azure_bug_id: str
    severity: str
    status: str
    fixed_by: Optional[str]
    fixed_date: Optional[str]
    notes: Optional[str]


# Database functions
def init_database():
    """Initialize database with schema and data"""
    if DB_PATH.exists():
        logger.info(f"📊 Database already exists at {DB_PATH}")
        return
    
    logger.info(f"🔨 Creating new database at {DB_PATH}")
    
    # Read schema file
    schema_path = Path(__file__).parent.parent / "schema_sqlite.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Create database and execute schema
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        logger.info("✅ Database created successfully with sample data")
    except Exception as e:
        logger.error(f"❌ Error creating database: {e}")
        raise
    finally:
        conn.close()


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_bug_fix_trends_from_db(days_back: int, project_id: Optional[int] = None, project_name: Optional[str] = None):
    """Get bug fix trends from database - supports both project_id (int) and project_name (string)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    conn = get_db_connection()
    try:
        actual_project_id = None
        resolved_project_name = None
        
        # Build query based on project filter - prioritize project_id if both provided
        if project_id is not None:
            # Use project_id directly (integer)
            project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectId = ?"
            project_row = conn.execute(project_query, (project_id,)).fetchone()
            
            if not project_row:
                raise HTTPException(
                    status_code=404,
                    detail=f"Project with ID '{project_id}' not found. Available IDs: 1 (HotRetailSys), 2 (PaymentsGateway)"
                )
            
            actual_project_id = project_row['ProjectId']
            resolved_project_name = project_row['ProjectName']
            
        elif project_name is not None:
            # Use project_name (string)
            project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectName = ? COLLATE NOCASE"
            project_row = conn.execute(project_query, (project_name,)).fetchone()
            
            if not project_row:
                raise HTTPException(
                    status_code=404,
                    detail=f"Project '{project_name}' not found. Available projects: HotRetailSys, PaymentsGateway"
                )
            
            actual_project_id = project_row['ProjectId']
            resolved_project_name = project_row['ProjectName']
        
        # Build SQL query
        if actual_project_id is not None:
            sql_query = """
                SELECT 
                    DATE(b.FixedDate) as FixDate,
                    COUNT(*) as FixedCount
                FROM Bugs b
                INNER JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
                WHERE 
                    b.FixedDate IS NOT NULL
                    AND b.FixedDate >= ?
                    AND b.FixedDate <= ?
                    AND w.ProjectId = ?
                    AND b.Status = 'Closed'
                GROUP BY DATE(b.FixedDate)
                ORDER BY FixDate
            """
            params = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), actual_project_id)
        else:
            # No project filter - all projects
            sql_query = """
                SELECT 
                    DATE(FixedDate) as FixDate,
                    COUNT(*) as FixedCount
                FROM Bugs
                WHERE 
                    FixedDate IS NOT NULL
                    AND FixedDate >= ?
                    AND FixedDate <= ?
                    AND Status = 'Closed'
                GROUP BY DATE(FixedDate)
                ORDER BY FixDate
            """
            params = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        logger.info(f"🔍 Executing query with params: {params}")
        
        cursor = conn.execute(sql_query, params)
        results = cursor.fetchall()
        
        return results, sql_query, resolved_project_name, actual_project_id
        
    finally:
        conn.close()


def fill_missing_dates(trends: List[DailyTrend], start_date: datetime, end_date: datetime) -> List[DailyTrend]:
    """Fill in missing dates with zero counts"""
    trend_dict = {trend.date: trend.fixed_count for trend in trends}
    
    complete_trends = []
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        fixed_count = trend_dict.get(date_str, 0)
        
        complete_trends.append(DailyTrend(
            date=date_str,
            fixed_count=fixed_count
        ))
        
        current_date += timedelta(days=1)
    
    return complete_trends


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting DevOpsMCP application with SQLite...")
    
    # Initialize database
    try:
        init_database()
        logger.info(f"✅ Database ready at: {DB_PATH}")
        
        # Test connection
        conn = get_db_connection()
        cursor = conn.execute("SELECT COUNT(*) as count FROM Bugs")
        bug_count = cursor.fetchone()['count']
        conn.close()
        logger.info(f"📊 Found {bug_count} bugs in database")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    yield
    
    logger.info("👋 Shutting down DevOpsMCP...")


# Create FastAPI application
app = FastAPI(
    title="DevOpsMCP - Azure DevOps Analytics",
    description="Model Context Protocol API for DevOps Analytics with Real Bug Data",
    version="1.0.2",
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
        "name": "DevOpsMCP",
        "version": "1.0.2",
        "description": "Model Context Protocol API for DevOps Analytics",
        "status": "✅ Running with SQLite database",
        "database": str(DB_PATH),
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "endpoints": {
            "health": "POST /api/health",
            "projects": "POST /api/get_projects",
            "bug_trends": "POST /api/bugs/get_bug_fix_trends",
            "bug_summary": "POST /api/bugs/get_bugs_summary"
        }
    }


@app.post("/api/health", summary="Health Check", description="בדיקת תקינות המערכת והמסד נתונים")
async def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT COUNT(*) as count FROM Bugs")
        bug_count = cursor.fetchone()['count']
        conn.close()
        
        return {
            "status": "healthy",
            "api": "operational",
            "database": "connected",
            "bug_count": bug_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "api": "operational",
            "database": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/get_projects", summary="Get Projects", description="קבלת רשימת כל הפרויקטים")
async def get_projects():
    """קבלת רשימת פרויקטים"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT ProjectId, ProjectName, Description, IsActive
            FROM Projects
            WHERE IsActive = 1
            ORDER BY ProjectName
        """)
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                "project_id": row['ProjectId'],
                "project_name": row['ProjectName'],
                "description": row['Description']
            })
        
        return {
            "projects": projects,
            "count": len(projects)
        }
    finally:
        conn.close()


@app.post(
    "/api/bugs/get_bug_fix_trends",
    response_model=GetBugFixTrendsResponse,
    summary="Get Bug Fix Trends",
    description="מחזיר נתוני טרנד של באגים שתוקנו"
)
async def get_bug_fix_trends(request: GetBugFixTrendsRequest) -> GetBugFixTrendsResponse:
    """
    קבלת טרנד תיקון באגים מהמסד נתונים
    
    Parameters:
    - days_back: מספר ימים לאחור (ברירת מחדל: 10)
    - project_id: מזהה הפרויקט (מספר - אופציונלי) - לדוגמה: 1 או 2
    - project_name: שם הפרויקט (מחרוזת - אופציונלי) - לדוגמה: HotRetailSys או PaymentsGateway
    
    אפשר לשלוח אחד מהם - project_id או project_name!
    
    דוגמאות:
    - {"days_back": 7} - כל הבאגים מ-7 הימים האחרונים
    - {"days_back": 14, "project_id": 1} - רק מפרויקט 1 (HotRetailSys)
    - {"days_back": 14, "project_name": "HotRetailSys"} - רק מפרויקט HotRetailSys
    - {"days_back": 30, "project_id": 2} - רק מפרויקט 2 (PaymentsGateway)
    """
    try:
        logger.info(f"📊 Getting bug fix trends: days_back={request.days_back}, project_id={request.project_id}, project_name={request.project_name}")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=request.days_back)
        
        # Get data from database (now returns 4 values!)
        results, sql_query, resolved_project_name, resolved_project_id = get_bug_fix_trends_from_db(
            request.days_back, 
            request.project_id, 
            request.project_name
        )
        
        # Process results
        daily_aggregation = []
        total_fixed = 0
        
        for row in results:
            fix_date = row['FixDate']
            fixed_count = row['FixedCount']
            
            daily_aggregation.append(DailyTrend(
                date=fix_date,
                fixed_count=fixed_count
            ))
            total_fixed += fixed_count
        
        # Fill in missing dates with zero counts
        daily_aggregation = fill_missing_dates(daily_aggregation, start_date, end_date)
        
        # Prepare trend graph data
        trend_graph_data = TrendGraphData(
            labels=[trend.date for trend in daily_aggregation],
            values=[trend.fixed_count for trend in daily_aggregation]
        )
        
        logger.info(f"✅ Found {total_fixed} fixed bugs in period")
        
        return GetBugFixTrendsResponse(
            total_fixed_bugs=total_fixed,
            daily_aggregation=daily_aggregation,
            trend_graph_data=trend_graph_data,
            sql_query=sql_query,
            period_start=start_date.strftime('%Y-%m-%d'),
            period_end=end_date.strftime('%Y-%m-%d'),
            project_id=str(resolved_project_id) if resolved_project_id else None,
            project_name=resolved_project_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting bug fix trends: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve bug fix trends: {str(e)}"
        )


class GetBugsSummaryRequest(BaseModel):
    """בקשה לקבלת סיכום באגים"""
    status: Optional[str] = Field(
        default=None,
        description="סטטוס לפילטר (Active, Closed, New, Resolved) - אופציונלי"
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="מספר מקסימלי של תוצאות (1-100)"
    )


@app.post(
    "/api/bugs/get_bugs_summary",
    summary="Get Bugs Summary",
    description="קבלת סיכום באגים לפי סטטוס"
)
async def get_bugs_summary(request: GetBugsSummaryRequest):
    """קבלת סיכום באגים לפי סטטוס"""
    conn = get_db_connection()
    try:
        if request.status:
            query = """
                SELECT BugId, AzureBugId, Severity, Status, FixedBy, 
                       FixedDate, Notes
                FROM Bugs
                WHERE Status = ?
                ORDER BY BugId DESC
                LIMIT ?
            """
            params = (request.status, request.limit)
        else:
            query = """
                SELECT BugId, AzureBugId, Severity, Status, FixedBy, 
                       FixedDate, Notes
                FROM Bugs
                ORDER BY BugId DESC
                LIMIT ?
            """
            params = (request.limit,)
        
        cursor = conn.execute(query, params)
        
        bugs = []
        for row in cursor.fetchall():
            bugs.append({
                "bug_id": row['BugId'],
                "azure_bug_id": row['AzureBugId'],
                "severity": row['Severity'],
                "status": row['Status'],
                "fixed_by": row['FixedBy'],
                "fixed_date": row['FixedDate'],
                "notes": row['Notes']
            })
        
        return {
            "bugs": bugs,
            "count": len(bugs),
            "filter": request.status,
            "limit": request.limit
        }
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "app.main_with_db:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
