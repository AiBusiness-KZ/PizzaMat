"""
PizzaMatIF FastAPI Application
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.config import settings
from app.database import init_db, close_db
from app.core.i18n import get_translator

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    logger.info("Starting PizzaMatIF Backend...")
    
    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down PizzaMatIF Backend...")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="PizzaMatIF API",
    description="Backend API for pizza ordering automation via Telegram",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "service": "pizzamatif-backend"
    }


@app.get("/debug-info")
async def debug_info():
    """Debug info endpoint - shows current configuration"""
    from app.config import settings
    return {
        "DEBUG": settings.DEBUG,
        "docs_enabled": app.docs_url is not None,
        "docs_url": app.docs_url,
        "redoc_url": app.redoc_url,
        "ALLOWED_ORIGINS": settings.origins[:2] if len(settings.origins) > 0 else [],
        "WEBAPP_URL": settings.WEBAPP_URL,
        "DATABASE_CONNECTED": "Check /health for status",
        "UPLOAD_DIR": settings.UPLOAD_DIR,
        "MAX_FILE_SIZE": settings.MAX_FILE_SIZE,
    }


@app.get("/")
async def root():
    """Root endpoint"""
    _ = get_translator()
    return {
        "message": _.t("welcome"),
        "service": "PizzaMatIF API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else None
    }


# Import and include routers
from app.routes import menu, locations, admin, auth

app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(locations.router)
app.include_router(admin.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
