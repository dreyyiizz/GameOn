#!/usr/bin/env python3
"""
Database Connection Test Script for GameOn

This script demonstrates how to connect to the database and perform basic operations.
It can be used to verify that your database connection is working properly.

Usage:
    python test_db_connection.py

Make sure to have your .env file configured with MONGO_URL before running.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from db import db_manager
from player.schemas import PlayerIn

# Load environment variables
load_dotenv()

async def test_database_connection():
    """Test database connection and basic operations."""
    print("🔌 Testing GameOn Database Connection...")
    print("=" * 50)
    
    # Test connection
    print("1. Testing database connection...")
    connected = await db_manager.connect()
    
    if connected:
        print("✅ Successfully connected to MongoDB!")
    else:
        print("❌ Failed to connect to MongoDB!")
        return False
    
    # Test health check
    print("\n2. Running health check...")
    health = await db_manager.health_check()
    print(f"📊 Health Status: {health['status']}")
    print(f"💬 Message: {health['message']}")
    
    if health['status'] != 'healthy':
        print("⚠️  Database is not healthy!")
        return False
    
    # Test basic database operations
    print("\n3. Testing basic database operations...")
    
    try:
        # Import after connection is established
        from player.service import PlayerService
        player_service = PlayerService()
        
        # Create a test player
        test_player = PlayerIn(name="TestPlayer", coins=100)
        print(f"📝 Creating test player: {test_player.name}")
        
        created_player = await player_service.create_player(test_player)
        if created_player:
            print(f"✅ Created player with ID: {created_player._id}")
            
            # Get the player back
            retrieved_player = await player_service.get_player(created_player._id)
            if retrieved_player:
                print(f"✅ Retrieved player: {retrieved_player.name} (Coins: {retrieved_player.coins})")
            
            # Update player coins
            updated_player = await player_service.add_coins(created_player._id, 50)
            if updated_player:
                print(f"✅ Updated player coins: {updated_player.coins}")
            
            # Clean up - delete test player
            deleted = await player_service.delete_player(created_player._id)
            if deleted:
                print("✅ Cleaned up test player")
            
        else:
            print("❌ Failed to create test player")
            return False
            
    except Exception as e:
        print(f"❌ Error during database operations: {e}")
        return False
    
    print("\n4. Connection test completed successfully! 🎉")
    return True

async def show_database_info():
    """Display database connection information."""
    print("\n📋 Database Configuration:")
    print("-" * 30)
    print(f"MongoDB URL: {os.getenv('MONGO_URL', 'Not set')}")
    print(f"Database Name: {os.getenv('DB_NAME', 'trashtrek (default)')}")
    print(f"Connected: {db_manager.is_connected}")
    
    if db_manager.db is not None:
        db_name = os.getenv("DB_NAME", "trashtrek")
        print(f"Active Database: {db_name}")

def print_usage_examples():
    """Print usage examples for database connection."""
    print("\n📚 Database Connection Usage Examples:")
    print("=" * 50)
    
    print("""
1. Basic Connection (already done in this script):
   ```python
   from db import db_manager
   
   # Connect to database
   connected = await db_manager.connect()
   if connected:
       print("Connected!")
   ```

2. Using the Player Service:
   ```python
   from player.service import PlayerService
   from player.schemas import PlayerIn
   
   service = PlayerService()
   
   # Create a player
   player_data = PlayerIn(name="John", coins=0)
   player = await service.create_player(player_data)
   
   # Get all players
   players = await service.get_players()
   
   # Get specific player
   player = await service.get_player(player_id)
   ```

3. Health Check:
   ```python
   health = await db_manager.health_check()
   print(f"Status: {health['status']}")
   ```

4. Environment Variables (.env file):
   ```
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=trashtrek
   ```

5. Running the FastAPI Server:
   ```bash
   uvicorn main:app --reload
   ```
   
   Then visit:
   - http://localhost:8000/health (Health check)
   - http://localhost:8000/db/status (Database status)
   - http://localhost:8000/docs (API documentation)
""")

async def main():
    """Main function to run all tests."""
    try:
        await show_database_info()
        
        success = await test_database_connection()
        
        if success:
            print_usage_examples()
            print("\n🎉 All tests passed! Your database connection is ready to use.")
            return 0
        else:
            print("\n❌ Some tests failed. Please check your database configuration.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1
    finally:
        # Cleanup
        await db_manager.disconnect()

if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.getenv("MONGO_URL"):
        print("❌ Error: MONGO_URL environment variable is not set!")
        print("Please create a .env file with:")
        print("MONGO_URL=mongodb://localhost:27017")
        sys.exit(1)
    
    # Run the async main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)