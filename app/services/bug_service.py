"""
Business logic for bug-related operations
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.database import db_manager
from app.schemas.bug_schemas import (
    GetBugFixTrendsRequest,
    GetBugFixTrendsResponse,
    DailyTrend,
    TrendGraphData
)

logger = logging.getLogger(__name__)


class BugService:
    """Service class for bug-related business logic"""
    
    def __init__(self):
        self.db = db_manager
    
    def get_bug_fix_trends(self, request: GetBugFixTrendsRequest) -> GetBugFixTrendsResponse:
        """
        Analyze bug fix trends over a specified period
        
        Args:
            request: GetBugFixTrendsRequest containing days_back and optional project_id
            
        Returns:
            GetBugFixTrendsResponse with trend analysis data
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=request.days_back)
        
        # Build SQL query
        if request.project_id:
            sql_query = """
                SELECT 
                    CAST(ClosedAt AS DATE) as FixDate,
                    COUNT(*) as FixedCount
                FROM Bugs
                WHERE 
                    ClosedAt IS NOT NULL
                    AND ClosedAt >= ?
                    AND ClosedAt <= ?
                    AND ProjectId = ?
                    AND Status = 'Closed'
                GROUP BY CAST(ClosedAt AS DATE)
                ORDER BY FixDate
            """
            params = (start_date, end_date, request.project_id)
        else:
            sql_query = """
                SELECT 
                    CAST(ClosedAt AS DATE) as FixDate,
                    COUNT(*) as FixedCount
                FROM Bugs
                WHERE 
                    ClosedAt IS NOT NULL
                    AND ClosedAt >= ?
                    AND ClosedAt <= ?
                    AND Status = 'Closed'
                GROUP BY CAST(ClosedAt AS DATE)
                ORDER BY FixDate
            """
            params = (start_date, end_date)
        
        logger.info(f"Executing bug fix trends query for {request.days_back} days back")
        
        # Execute query
        results = self.db.execute_query(sql_query, params)
        
        # Process results
        daily_aggregation = []
        total_fixed = 0
        
        for row in results:
            fix_date = row['FixDate']
            fixed_count = row['FixedCount']
            
            # Convert date to string format
            date_str = fix_date.strftime('%Y-%m-%d') if isinstance(fix_date, datetime) else str(fix_date)
            
            daily_aggregation.append(DailyTrend(
                date=date_str,
                fixed_count=fixed_count
            ))
            total_fixed += fixed_count
        
        # Fill in missing dates with zero counts
        daily_aggregation = self._fill_missing_dates(
            daily_aggregation, 
            start_date, 
            end_date
        )
        
        # Prepare trend graph data
        trend_graph_data = TrendGraphData(
            labels=[trend.date for trend in daily_aggregation],
            values=[trend.fixed_count for trend in daily_aggregation]
        )
        
        logger.info(f"Bug fix trends analysis complete: {total_fixed} bugs fixed")
        
        return GetBugFixTrendsResponse(
            total_fixed_bugs=total_fixed,
            daily_aggregation=daily_aggregation,
            trend_graph_data=trend_graph_data,
            sql_query=sql_query,
            period_start=start_date.strftime('%Y-%m-%d'),
            period_end=end_date.strftime('%Y-%m-%d'),
            project_id=request.project_id
        )
    
    def _fill_missing_dates(
        self, 
        trends: List[DailyTrend], 
        start_date: datetime, 
        end_date: datetime
    ) -> List[DailyTrend]:
        """
        Fill in missing dates in the trend data with zero counts
        
        Args:
            trends: List of existing daily trends
            start_date: Start of the period
            end_date: End of the period
            
        Returns:
            Complete list of daily trends with no gaps
        """
        # Create a dictionary for quick lookup
        trend_dict = {trend.date: trend.fixed_count for trend in trends}
        
        # Generate all dates in range
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


# Singleton instance
bug_service = BugService()
