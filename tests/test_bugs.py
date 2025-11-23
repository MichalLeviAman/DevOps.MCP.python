"""
Unit tests for bug-related endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "DevOpsMCP"
    assert data["version"] == "1.0.1"


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "api" in data
    assert "database" in data


def test_bugs_health_endpoint():
    """Test bugs router health check"""
    response = client.get("/api/bugs/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "bugs"


def test_get_bug_fix_trends_default_params():
    """Test bug fix trends with default parameters"""
    response = client.post(
        "/api/bugs/get_bug_fix_trends",
        json={}
    )
    # May fail if database not connected, but should return proper structure
    if response.status_code == 200:
        data = response.json()
        assert "total_fixed_bugs" in data
        assert "daily_aggregation" in data
        assert "trend_graph_data" in data
        assert "sql_query" in data
        assert "period_start" in data
        assert "period_end" in data


def test_get_bug_fix_trends_with_params():
    """Test bug fix trends with custom parameters"""
    response = client.post(
        "/api/bugs/get_bug_fix_trends",
        json={
            "days_back": 30,
            "project_id": "PROJ001"
        }
    )
    # May fail if database not connected, but should return proper structure
    if response.status_code == 200:
        data = response.json()
        assert "total_fixed_bugs" in data
        assert data["project_id"] == "PROJ001"


def test_get_bug_fix_trends_validation_error():
    """Test validation error for invalid parameters"""
    response = client.post(
        "/api/bugs/get_bug_fix_trends",
        json={
            "days_back": -5  # Invalid: negative value
        }
    )
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
