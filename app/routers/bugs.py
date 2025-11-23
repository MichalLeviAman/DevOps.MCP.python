"""
Bug-related API endpoints
"""
import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.bug_schemas import GetBugFixTrendsRequest, GetBugFixTrendsResponse
from app.services.bug_service import bug_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/bugs",
    tags=["bugs"]
)


@router.post(
    "/get_bug_fix_trends",
    response_model=GetBugFixTrendsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Bug Fix Trends",
    description="Retrieve statistics and trends for bug fixes over a specified time period"
)
async def get_bug_fix_trends(request: GetBugFixTrendsRequest) -> GetBugFixTrendsResponse:
    """
    Analyze bug fix trends over the last N days.
    
    - **days_back**: Number of days to look back (default: 10, max: 365)
    - **project_id**: Optional project ID to filter results
    
    Returns:
    - Total fixed bugs count
    - Daily aggregation of fixed bugs
    - Trend graph data for visualization
    - SQL query used
    - Period start and end dates
    """
    try:
        logger.info(f"Getting bug fix trends: days_back={request.days_back}, project_id={request.project_id}")
        result = bug_service.get_bug_fix_trends(request)
        return result
    except Exception as e:
        logger.error(f"Error getting bug fix trends: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve bug fix trends: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the bugs API is operational"
)
async def health_check():
    """Health check endpoint for bugs router"""
    return {
        "status": "healthy",
        "service": "bugs",
        "timestamp": "2025-11-20T00:00:00Z"
    }
