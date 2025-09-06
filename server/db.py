import os
import logging
from typing import Optional
from pymongo import AsyncMongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database connection manager with error handling and health checks."""
    
    def __init__(self):
        self.client: Optional[AsyncMongoClient] = None
        self.db = None
        self.is_connected = False
        self._setup_connection()
    
    def _setup_connection(self):
        """Set up database connection with validation."""
        mongo_url = os.getenv("MONGO_URL")
        
        if not mongo_url:
            logger.error("MONGO_URL environment variable is not set")
            raise ValueError("MONGO_URL environment variable is required")
        
        try:
            # Create client with connection parameters
            self.client = AsyncMongoClient(
                mongo_url,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                maxPoolSize=50,
                minPoolSize=5,
                retryWrites=True
            )
            
            # Set database name (using env variable or default)
            db_name = os.getenv("DB_NAME", "trashtrek")
            self.db = self.client[db_name]
            
            logger.info(f"Database connection configured for: {db_name}")
            
        except Exception as e:
            logger.error(f"Failed to setup database connection: {e}")
            raise
    
    async def connect(self):
        """Test database connection."""
        try:
            # Test connection by pinging the server
            await self.client.admin.command('ping')
            self.is_connected = True
            logger.info("Successfully connected to MongoDB")
            return True
            
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            self.is_connected = False
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            self.is_connected = False
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    async def disconnect(self):
        """Close database connection."""
        if self.client:
            await self.client.close()
            self.is_connected = False
            logger.info("Disconnected from MongoDB")
    
    async def health_check(self):
        """Check database health."""
        try:
            if not self.client:
                return {"status": "error", "message": "No client connection"}
            
            # Test with ping command
            result = await self.client.admin.command('ping')
            
            if result.get('ok') == 1:
                db_name = os.getenv("DB_NAME", "trashtrek")
                return {
                    "status": "healthy", 
                    "message": "Database connection is active",
                    "database": db_name
                }
            else:
                return {"status": "error", "message": "Ping command failed"}
                
        except Exception as e:
            return {"status": "error", "message": f"Health check failed: {str(e)}"}
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database."""
        if self.db is None:
            raise RuntimeError("Database not initialized")
        return self.db[collection_name]

# Create global database manager instance
db_manager = DatabaseManager()

# Backward compatibility - maintain existing API
client = db_manager.client
db = db_manager.db

# Collections
players_collection = db_manager.get_collection("players")
