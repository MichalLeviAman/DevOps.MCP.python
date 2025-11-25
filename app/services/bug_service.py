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
            request: GetBugFixTrendsRequest containing days_back and optional project_id/project_name
            
        Returns:
            GetBugFixTrendsResponse with trend analysis data
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=request.days_back)
        
        # Format dates for SQLite
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        # Build SQL query based on project filter
        if request.project_id or request.project_name:
            # Join with WorkItems and Projects to support both project_id and project_name
            sql_query = """
                SELECT 
                    DATE(b.FixedDate) as FixDate,
                    COUNT(*) as FixedCount
                FROM Bugs b
                LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
                LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
                WHERE 
                    b.FixedDate IS NOT NULL
                    AND DATE(b.FixedDate) >= ?
                    AND DATE(b.FixedDate) <= ?
                    AND b.Status = 'Closed'
            """
            
            if request.project_id:
                sql_query += " AND p.ProjectId = ?"
                params = (start_date_str, end_date_str, request.project_id)
            else:  # project_name
                sql_query += " AND p.ProjectName = ?"
                params = (start_date_str, end_date_str, request.project_name)
            
            sql_query += """
                GROUP BY DATE(b.FixedDate)
                ORDER BY FixDate
            """
        else:
            # No project filter - all projects
            sql_query = """
                SELECT 
                    DATE(FixedDate) as FixDate,
                    COUNT(*) as FixedCount
                FROM Bugs
                WHERE 
                    FixedDate IS NOT NULL
                    AND DATE(FixedDate) >= ?
                    AND DATE(FixedDate) <= ?
                    AND Status = 'Closed'
                GROUP BY DATE(FixedDate)
                ORDER BY FixDate
            """
            params = (start_date_str, end_date_str)
        
        logger.info(f"Executing bug fix trends query for {request.days_back} days back")
        
        # Get project details if filtered by project
        project_id_result = None
        project_name_result = None
        
        if request.project_id or request.project_name:
            if request.project_id:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectId = ?"
                project_params = (request.project_id,)
            else:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectName = ?"
                project_params = (request.project_name,)
            
            project_info = self.db.execute_query(project_query, project_params)
            if project_info:
                project_id_result = str(project_info[0]['ProjectId'])
                project_name_result = project_info[0]['ProjectName']
        
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
            project_id=project_id_result,
            project_name=project_name_result
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
    
    def get_active_bugs(self, request) -> Dict[str, Any]:
        """Get all active bugs with optional filters"""
        from app.schemas.bug_schemas import GetActiveBugsResponse, BugItem
        
        # Get project details if filtered
        project_id_result = None
        project_name_result = None
        
        if request.project_id or request.project_name:
            if request.project_id:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectId = ?"
                project_params = (request.project_id,)
            else:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectName = ?"
                project_params = (request.project_name,)
            
            project_info = self.db.execute_query(project_query, project_params)
            if project_info:
                project_id_result = str(project_info[0]['ProjectId'])
                project_name_result = project_info[0]['ProjectName']
        
        # Build query with filters
        sql_parts = ["""
            SELECT 
                b.BugId, b.AzureBugId, w.Title, b.Severity, b.Status,
                w.CreatedDate, b.Notes
            FROM Bugs b
            LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
            LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
            WHERE b.Status = 'Active'
        """]
        
        params = []
        
        if request.project_id:
            sql_parts.append("AND p.ProjectId = ?")
            params.append(request.project_id)
        elif request.project_name:
            sql_parts.append("AND p.ProjectName = ?")
            params.append(request.project_name)
        
        if request.severity:
            sql_parts.append("AND b.Severity = ?")
            params.append(request.severity)
        
        sql_query = " ".join(sql_parts)
        results = self.db.execute_query(sql_query, tuple(params) if params else None)
        
        bugs = []
        for row in results:
            bugs.append(BugItem(
                bug_id=row['BugId'],
                azure_bug_id=row['AzureBugId'],
                title=row.get('Title', 'N/A'),
                severity=row.get('Severity'),
                status=row['Status'],
                created_date=str(row.get('CreatedDate')) if row.get('CreatedDate') else None,
                notes=row.get('Notes')
            ))
        
        return GetActiveBugsResponse(
            total_active_bugs=len(bugs),
            bugs=bugs,
            filters_applied={
                "project_id": request.project_id,
                "project_name": request.project_name,
                "severity": request.severity
            },
            project_id=project_id_result,
            project_name=project_name_result
        )
    
    def get_bugs_by_status(self, request) -> Dict[str, Any]:
        """Get bugs filtered by status"""
        from app.schemas.bug_schemas import GetBugsByStatusResponse, BugItem
        
        # Get project details if filtered
        project_id_result = None
        project_name_result = None
        
        if request.project_id or request.project_name:
            if request.project_id:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectId = ?"
                project_params = (request.project_id,)
            else:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectName = ?"
                project_params = (request.project_name,)
            
            project_info = self.db.execute_query(project_query, project_params)
            if project_info:
                project_id_result = str(project_info[0]['ProjectId'])
                project_name_result = project_info[0]['ProjectName']
        
        sql_query = """
            SELECT 
                b.BugId, b.AzureBugId, w.Title, b.Severity, b.Status,
                w.CreatedDate, b.Notes
            FROM Bugs b
            LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
            LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
            WHERE b.Status = ?
        """
        
        params = [request.status]
        
        if request.project_id:
            sql_query += " AND p.ProjectId = ?"
            params.append(request.project_id)
        elif request.project_name:
            sql_query += " AND p.ProjectName = ?"
            params.append(request.project_name)
        
        sql_query += f" LIMIT {request.limit}"
        
        results = self.db.execute_query(sql_query, tuple(params))
        
        bugs = []
        for row in results:
            bugs.append(BugItem(
                bug_id=row['BugId'],
                azure_bug_id=row['AzureBugId'],
                title=row.get('Title', 'N/A'),
                severity=row.get('Severity'),
                status=row['Status'],
                created_date=str(row.get('CreatedDate')) if row.get('CreatedDate') else None,
                notes=row.get('Notes')
            ))
        
        return GetBugsByStatusResponse(
            status=request.status,
            total_count=len(bugs),
            bugs=bugs,
            project_id=project_id_result,
            project_name=project_name_result
        )
    
    def get_bug_statistics(self, request) -> Dict[str, Any]:
        """Get comprehensive bug statistics"""
        from app.schemas.bug_schemas import GetBugStatisticsResponse, BugStatistics
        
        # Get project details if filtered
        project_id_result = None
        project_name_result = None
        
        if request.project_id or request.project_name:
            if request.project_id:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectId = ?"
                project_params = (request.project_id,)
            else:
                project_query = "SELECT ProjectId, ProjectName FROM Projects WHERE ProjectName = ?"
                project_params = (request.project_name,)
            
            project_info = self.db.execute_query(project_query, project_params)
            if project_info:
                project_id_result = str(project_info[0]['ProjectId'])
                project_name_result = project_info[0]['ProjectName']
        
        # Total bugs by status
        status_query = """
            SELECT Status, COUNT(*) as Count
            FROM Bugs
            GROUP BY Status
        """
        
        if request.project_id:
            status_query = """
                SELECT b.Status, COUNT(*) as Count
                FROM Bugs b
                LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
                LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
                WHERE p.ProjectId = ?
                GROUP BY b.Status
            """
        elif request.project_name:
            status_query = """
                SELECT b.Status, COUNT(*) as Count
                FROM Bugs b
                LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
                LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
                WHERE p.ProjectName = ?
                GROUP BY b.Status
            """
        
        if request.project_id:
            status_results = self.db.execute_query(status_query, (request.project_id,))
        elif request.project_name:
            status_results = self.db.execute_query(status_query, (request.project_name,))
        else:
            status_results = self.db.execute_query(status_query)
        
        total_bugs = 0
        active_bugs = 0
        closed_bugs = 0
        new_bugs = 0
        
        for row in status_results:
            count = row['Count']
            total_bugs += count
            if row['Status'] == 'Active':
                active_bugs = count
            elif row['Status'] == 'Closed':
                closed_bugs = count
            elif row['Status'] == 'New':
                new_bugs = count
        
        # By severity
        severity_query = """
            SELECT Severity, COUNT(*) as Count
            FROM Bugs
            WHERE Severity IS NOT NULL
            GROUP BY Severity
        """
        
        if request.project_id:
            severity_query = """
                SELECT b.Severity, COUNT(*) as Count
                FROM Bugs b
                LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
                LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
                WHERE p.ProjectId = ? AND b.Severity IS NOT NULL
                GROUP BY b.Severity
            """
        elif request.project_name:
            severity_query = """
                SELECT b.Severity, COUNT(*) as Count
                FROM Bugs b
                LEFT JOIN WorkItems w ON b.WorkItemId = w.WorkItemId
                LEFT JOIN Projects p ON w.ProjectId = p.ProjectId
                WHERE p.ProjectName = ? AND b.Severity IS NOT NULL
                GROUP BY b.Severity
            """
        
        if request.project_id:
            severity_results = self.db.execute_query(severity_query, (request.project_id,))
        elif request.project_name:
            severity_results = self.db.execute_query(severity_query, (request.project_name,))
        else:
            severity_results = self.db.execute_query(severity_query)
        by_severity = {row['Severity']: row['Count'] for row in severity_results}
        
        # By project
        project_query = """
            SELECT p.ProjectName, COUNT(b.BugId) as BugCount
            FROM Projects p
            LEFT JOIN WorkItems w ON p.ProjectId = w.ProjectId
            LEFT JOIN Bugs b ON w.WorkItemId = b.WorkItemId
            GROUP BY p.ProjectName
            ORDER BY BugCount DESC
        """
        
        project_results = self.db.execute_query(project_query)
        by_project = [{"project": row['ProjectName'], "count": row['BugCount']} for row in project_results]
        
        statistics = BugStatistics(
            total_bugs=total_bugs,
            active_bugs=active_bugs,
            closed_bugs=closed_bugs,
            new_bugs=new_bugs,
            by_severity=by_severity,
            by_project=by_project
        )
        
        return GetBugStatisticsResponse(
            statistics=statistics,
            generated_at=datetime.now().isoformat(),
            project_id=project_id_result,
            project_name=project_name_result
        )


# Singleton instance
bug_service = BugService()
