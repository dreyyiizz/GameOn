# Database Connection Quick Start Guide

## Overview

This GameOn project now includes a robust database connection system that can connect to MongoDB with comprehensive error handling, health monitoring, and connection management.

## Quick Setup

### 1. Environment Configuration
Create a `.env` file in the server directory:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=trashtrek
```

### 2. Install Dependencies
```bash
cd server
pip install -r requirements.txt
```

### 3. Test Database Connection
```bash
python test_db_connection.py
```

### 4. Start the API Server
```bash
uvicorn main:app --reload
```

## Key Features

### ✅ Robust Connection Management
- Automatic connection retry and timeout handling
- Connection pooling with configurable pool sizes
- Graceful startup/shutdown with database lifecycle management

### ✅ Health Monitoring
- Real-time health check endpoints
- Database connection status monitoring
- Detailed error reporting and logging

### ✅ Error Handling
- Comprehensive exception handling for all database operations
- Proper HTTP status codes for different error scenarios
- Input validation for ObjectId formats and data types

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API welcome message |
| `GET /health` | Overall health check (includes database) |
| `GET /db/status` | Detailed database connection status |
| `POST /players/` | Create a new player |
| `GET /players/` | Get all players |
| `GET /players/{id}` | Get specific player |
| `PUT /players/{id}` | Update player |
| `DELETE /players/{id}` | Delete player |
| `PATCH /players/{id}/coins` | Add/remove coins |

## Code Examples

### Basic Database Connection
```python
from db import db_manager

# Connect to database
connected = await db_manager.connect()
if connected:
    print("Connected to MongoDB!")

# Check health
health = await db_manager.health_check()
print(f"Status: {health['status']}")
```

### Using Player Service
```python
from player.service import PlayerService
from player.schemas import PlayerIn

service = PlayerService()

# Create player
player_data = PlayerIn(name="Alice", coins=100)
player = await service.create_player(player_data)

# Get all players
players = await service.get_players()
```

## Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `MONGO_URL` | MongoDB connection string | Required |
| `DB_NAME` | Database name | `trashtrek` |

## Testing

Run the included test script to verify your setup:
```bash
python test_db_connection.py
```

This will:
- Test database connection
- Verify health checks
- Test basic CRUD operations
- Provide usage examples

## Troubleshooting

### Connection Issues
1. Verify MongoDB is running
2. Check `MONGO_URL` in `.env` file
3. Test with: `python test_db_connection.py`

### API Issues
1. Check server logs for errors
2. Visit `/health` endpoint for status
3. Use `/db/status` for detailed database info

## Production Deployment

For production, update your `.env` with:
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=production_db
```

## Documentation

- Full API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`
- Complete README: `server/README.md`