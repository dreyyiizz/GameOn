# GameOn API Server

A robust FastAPI backend for the GameOn application with MongoDB database connectivity.

## Database Connection Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB instance (local or remote)
- All required dependencies installed

### Quick Start

1. **Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Linux/MacOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Database Configuration**
   
   Create a `.env` file in the server directory:
   ```env
   # Database Configuration
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=trashtrek
   
   # Optional: Advanced Configuration
   # MONGO_MAX_POOL_SIZE=50
   # MONGO_MIN_POOL_SIZE=5
   # MONGO_SERVER_SELECTION_TIMEOUT_MS=5000
   ```

3. **Test Database Connection**
   ```bash
   python test_db_connection.py
   ```

4. **Run the API Server**
   ```bash
   # Development server with auto-reload
   uvicorn main:app --reload
   
   # Production server
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Database Connection Features

#### ✅ Robust Connection Management
- Automatic connection retry logic
- Connection pooling with configurable pool sizes
- Graceful connection lifecycle management
- Health monitoring and status checks

#### ✅ Error Handling
- Comprehensive error catching and logging
- Proper HTTP status codes for different error types
- Input validation for ObjectId formats
- Database operation timeout handling

#### ✅ Monitoring & Health Checks
- Real-time connection status monitoring
- Database health check endpoints
- Detailed error reporting and logging
- Connection diagnostics

### API Endpoints

#### Health & Status
- `GET /` - API welcome message
- `GET /health` - Overall health check (includes database status)
- `GET /db/status` - Detailed database connection status

#### Player Management
- `POST /players/` - Create a new player
- `GET /players/` - Get all players
- `GET /players/{id}` - Get specific player
- `PUT /players/{id}` - Update player
- `DELETE /players/{id}` - Delete player
- `PATCH /players/{id}/coins` - Add/remove coins

### Database Connection Code Examples

#### Basic Connection
```python
from db import db_manager

# Connect to database
connected = await db_manager.connect()
if connected:
    print("Successfully connected to MongoDB!")

# Check connection health
health = await db_manager.health_check()
print(f"Database status: {health['status']}")
```

#### Using Player Service
```python
from player.service import PlayerService
from player.schemas import PlayerIn

# Create service instance
service = PlayerService()

# Create a new player
player_data = PlayerIn(name="Alice", coins=100)
new_player = await service.create_player(player_data)

# Get all players
players = await service.get_players()

# Get specific player
player = await service.get_player(player_id)

# Update player
updated_player = await service.update_player(player_id, player_data)

# Add coins
player_with_coins = await service.add_coins(player_id, 50)
```

#### Error Handling Example
```python
from fastapi import HTTPException
from player.service import PlayerService

try:
    player = await PlayerService().get_player("invalid_id")
except HTTPException as e:
    print(f"HTTP Error: {e.status_code} - {e.detail}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Configuration Options

#### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGO_URL` | MongoDB connection string | - | Yes |
| `DB_NAME` | Database name | `trashtrek` | No |
| `MONGO_MAX_POOL_SIZE` | Maximum connection pool size | `50` | No |
| `MONGO_MIN_POOL_SIZE` | Minimum connection pool size | `5` | No |
| `MONGO_SERVER_SELECTION_TIMEOUT_MS` | Server selection timeout | `5000` | No |

#### MongoDB Connection String Examples
```bash
# Local MongoDB
MONGO_URL=mongodb://localhost:27017

# MongoDB with authentication
MONGO_URL=mongodb://username:password@localhost:27017

# MongoDB Atlas (cloud)
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/

# MongoDB with custom options
MONGO_URL=mongodb://localhost:27017/?retryWrites=true&w=majority
```

### Troubleshooting

#### Common Issues

1. **Connection Failed**
   - Verify MongoDB is running
   - Check `MONGO_URL` in `.env` file
   - Ensure network connectivity
   - Verify credentials if using authentication

2. **Database Not Found**
   - Database will be created automatically on first write
   - Verify `DB_NAME` in configuration

3. **Permission Errors**
   - Check MongoDB user permissions
   - Verify authentication credentials

4. **Timeout Errors**
   - Adjust `MONGO_SERVER_SELECTION_TIMEOUT_MS`
   - Check network latency
   - Verify MongoDB server status

#### Debugging Commands
```bash
# Test database connection
python test_db_connection.py

# Check API health
curl http://localhost:8000/health

# Check database status
curl http://localhost:8000/db/status

# View server logs
uvicorn main:app --log-level debug
```

### Development Tips

1. **Use the test script** regularly to verify your database connection
2. **Monitor the health endpoints** in production
3. **Check server logs** for detailed error information
4. **Use proper environment variables** for different environments
5. **Test with different connection strings** for development vs production

### API Documentation

When the server is running, visit:
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)
- http://localhost:8000/redoc - Alternative API documentation

This provides a complete interface to test all database operations through the web interface.
