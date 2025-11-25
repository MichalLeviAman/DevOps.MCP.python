"""
Bug-related API endpoints
"""
import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.bug_schemas import (
    GetBugFixTrendsRequest, GetBugFixTrendsResponse,
    GetActiveBugsRequest, GetActiveBugsResponse,
    GetBugsByStatusRequest, GetBugsByStatusResponse,
    GetBugStatisticsRequest, GetBugStatisticsResponse
)
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


@router.post(
    "/get_active_bugs",
    response_model=GetActiveBugsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Active Bugs",
    description="Retrieve all currently active bugs with optional filters"
)
async def get_active_bugs(request: GetActiveBugsRequest) -> GetActiveBugsResponse:
    """
    Get all active bugs, optionally filtered by project and severity.
    
    - **project_id**: Filter by specific project
    - **severity**: Filter by severity level (Low, Medium, High, Critical)
    """
    try:
        logger.info(f"Getting active bugs: project_id={request.project_id}, severity={request.severity}")
        result = bug_service.get_active_bugs(request)
        return result
    except Exception as e:
        logger.error(f"Error getting active bugs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve active bugs: {str(e)}"
        )


@router.post(
    "/get_bugs_by_status",
    response_model=GetBugsByStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Bugs by Status",
    description="Retrieve bugs filtered by status (Active, Closed, New)"
)
async def get_bugs_by_status(request: GetBugsByStatusRequest) -> GetBugsByStatusResponse:
    """
    Get bugs filtered by their status.
    
    - **status**: Bug status (Active, Closed, New)
    - **project_id**: Optional project filter
    - **limit**: Maximum number of results (default: 50)
    """
    try:
        logger.info(f"Getting bugs by status: status={request.status}, project_id={request.project_id}")
        result = bug_service.get_bugs_by_status(request)
        return result
    except Exception as e:
        logger.error(f"Error getting bugs by status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve bugs by status: {str(e)}"
        )


@router.post(
    "/get_bug_statistics",
    response_model=GetBugStatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Bug Statistics",
    description="Get comprehensive statistics about bugs across all projects"
)
async def get_bug_statistics(request: GetBugStatisticsRequest) -> GetBugStatisticsResponse:
    """
    Get comprehensive bug statistics including:
    - Total bugs by status
    - Bugs by severity
    - Bugs by project
    
    - **project_id**: Optional project filter
    """
    try:
        logger.info(f"Getting bug statistics: project_id={request.project_id}")
        result = bug_service.get_bug_statistics(request)
        return result
    except Exception as e:
        logger.error(f"Error getting bug statistics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve bug statistics: {str(e)}"
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
        "timestamp": "2025-11-25T00:00:00Z"
    }
