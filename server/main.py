from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import logging
import os
from player.routes import player_router
from db import db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Database connection lifecycle management."""
    # Startup
    logger.info("Starting up application...")
    connected = await db_manager.connect()
    if not connected:
        logger.error("Failed to connect to database on startup")
        # Continue anyway for development purposes
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await db_manager.disconnect()

app = FastAPI(
    title="GameOn API",
    description="API for GameOn with robust database connectivity",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to GameOn API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint that includes database status."""
    try:
        db_health = await db_manager.health_check()
        
        return {
            "status": "healthy" if db_health["status"] == "healthy" else "degraded",
            "database": db_health,
            "api": "running"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/db/status")
async def database_status():
    """Detailed database connection status."""
    try:
        health_info = await db_manager.health_check()
        return {
            "connected": db_manager.is_connected,
            "health": health_info,
            "client_info": {
                "database_name": os.getenv("DB_NAME", "trashtrek"),
                "has_client": db_manager.client is not None
            }
        }
    except Exception as e:
        logger.error(f"Database status check failed: {e}")
        return {
            "connected": False,
            "error": str(e)
        }

app.include_router(player_router)
