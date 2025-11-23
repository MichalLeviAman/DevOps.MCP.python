"""
DevOpsMCP - Model Context Protocol API for DevOps Analytics
Main FastAPI application entry point
"""
import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import get_settings
from app.database import db_manager
from app.routers import bugs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting DevOpsMCP application...")
    settings = get_settings()
    logger.info(f"Database host: {settings.db_host}")
    logger.info(f"Database name: {settings.db_name}")
    
    # Test database connection
    if db_manager.test_connection():
        logger.info("Database connection successful")
    else:
        logger.error("Database connection failed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down DevOpsMCP application...")


# Create FastAPI application
app = FastAPI(
    title="DevOpsMCP",
    description="Model Context Protocol API for DevOps Analytics, Bug Tracking, and Automation",
    version="1.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Request validation failed"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "message": "An unexpected error occurred"
        }
    )


# Include routers
app.include_router(bugs.router)


# Root endpoint
@app.get(
    "/",
    summary="Root Endpoint",
    description="Welcome endpoint with API information"
)
async def root():
    """Root endpoint"""
    return {
        "name": "DevOpsMCP",
        "version": "1.0.1",
        "description": "Model Context Protocol API for DevOps Analytics",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "health_url": "/health"
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Check API health and database connectivity"
)
async def health():
    """Health check endpoint"""
    db_healthy = db_manager.test_connection()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "api": "operational",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": "2025-11-20T00:00:00Z"
    }


# Entry point for local development
if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        log_level=settings.log_level.lower()
    )
