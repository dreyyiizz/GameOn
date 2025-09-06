import logging
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.errors import PyMongoError
from db import players_collection, db_manager
from player.schemas import PlayerIn, PlayerOut
from typing import Optional, List
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class PlayerService:
    """Player service with robust database error handling."""
    
    def __init__(self):
        self.collection = players_collection

    async def _ensure_connection(self):
        """Ensure database connection is active."""
        if not db_manager.is_connected:
            connected = await db_manager.connect()
            if not connected:
                raise HTTPException(
                    status_code=503, 
                    detail="Database connection unavailable"
                )

    async def create_player(self, player: PlayerIn) -> Optional[PlayerOut]:
        """Create a new player with error handling."""
        try:
            await self._ensure_connection()
            
            player_dict = player.model_dump()
            res = await self.collection.insert_one(player_dict)
            new_player = await self.collection.find_one({"_id": res.inserted_id})
            
            if new_player:
                logger.info(f"Created player with ID: {res.inserted_id}")
                return PlayerOut(**new_player)
            return None
            
        except PyMongoError as e:
            logger.error(f"Database error creating player: {e}")
            raise HTTPException(status_code=503, detail="Database operation failed")
        except Exception as e:
            logger.error(f"Unexpected error creating player: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_players(self) -> List[PlayerOut]:
        """Get all players with error handling."""
        try:
            await self._ensure_connection()
            
            players = self.collection.find()
            player_list = await players.to_list(length=None)
            
            logger.info(f"Retrieved {len(player_list)} players")
            return [PlayerOut(**player) for player in player_list]
            
        except PyMongoError as e:
            logger.error(f"Database error retrieving players: {e}")
            raise HTTPException(status_code=503, detail="Database operation failed")
        except Exception as e:
            logger.error(f"Unexpected error retrieving players: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_player(self, player_id: str) -> Optional[PlayerOut]:
        """Get a specific player with error handling."""
        try:
            await self._ensure_connection()
            
            # Validate ObjectId format
            try:
                object_id = ObjectId(player_id)
            except InvalidId:
                logger.warning(f"Invalid player ID format: {player_id}")
                raise HTTPException(status_code=400, detail="Invalid player ID format")
            
            player = await self.collection.find_one({"_id": object_id})
            
            if player:
                logger.info(f"Retrieved player: {player_id}")
                return PlayerOut(**player)
            else:
                logger.info(f"Player not found: {player_id}")
                return None
                
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except PyMongoError as e:
            logger.error(f"Database error retrieving player {player_id}: {e}")
            raise HTTPException(status_code=503, detail="Database operation failed")
        except Exception as e:
            logger.error(f"Unexpected error retrieving player {player_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def update_player(self, player_id: str, new_player: PlayerIn) -> Optional[PlayerOut]:
        """Update a player with error handling."""
        try:
            await self._ensure_connection()
            
            # Validate ObjectId format
            try:
                object_id = ObjectId(player_id)
            except InvalidId:
                logger.warning(f"Invalid player ID format: {player_id}")
                raise HTTPException(status_code=400, detail="Invalid player ID format")
            
            player_dict = new_player.model_dump()
            res = await self.collection.update_one(
                {"_id": object_id}, 
                {"$set": player_dict}
            )
            
            if res.matched_count == 0:
                logger.info(f"Player not found for update: {player_id}")
                return None
            
            updated_player = await self.collection.find_one({"_id": object_id})
            
            if updated_player:
                logger.info(f"Updated player: {player_id}")
                return PlayerOut(**updated_player)
            return None
            
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except PyMongoError as e:
            logger.error(f"Database error updating player {player_id}: {e}")
            raise HTTPException(status_code=503, detail="Database operation failed")
        except Exception as e:
            logger.error(f"Unexpected error updating player {player_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    async def delete_player(self, player_id: str) -> bool:
        """Delete a player with error handling."""
        try:
            await self._ensure_connection()
            
            # Validate ObjectId format
            try:
                object_id = ObjectId(player_id)
            except InvalidId:
                logger.warning(f"Invalid player ID format: {player_id}")
                raise HTTPException(status_code=400, detail="Invalid player ID format")
            
            res = await self.collection.delete_one({"_id": object_id})
            
            if res.deleted_count > 0:
                logger.info(f"Deleted player: {player_id}")
                return True
            else:
                logger.info(f"Player not found for deletion: {player_id}")
                return False
                
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except PyMongoError as e:
            logger.error(f"Database error deleting player {player_id}: {e}")
            raise HTTPException(status_code=503, detail="Database operation failed")
        except Exception as e:
            logger.error(f"Unexpected error deleting player {player_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    async def add_coins(self, player_id: str, increment: int) -> Optional[PlayerOut]:
        """Add coins to a player with error handling."""
        try:
            await self._ensure_connection()
            
            # Validate ObjectId format
            try:
                object_id = ObjectId(player_id)
            except InvalidId:
                logger.warning(f"Invalid player ID format: {player_id}")
                raise HTTPException(status_code=400, detail="Invalid player ID format")
            
            # Validate increment value
            if not isinstance(increment, int):
                raise HTTPException(status_code=400, detail="Increment must be an integer")
            
            res = await self.collection.update_one(
                {"_id": object_id}, 
                {"$inc": {"coins": increment}}
            )
            
            if res.matched_count == 0:
                logger.info(f"Player not found for coin update: {player_id}")
                return None
            
            updated_player = await self.collection.find_one({"_id": object_id})
            
            if updated_player:
                logger.info(f"Added {increment} coins to player: {player_id}")
                return PlayerOut(**updated_player)
            return None
            
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except PyMongoError as e:
            logger.error(f"Database error adding coins to player {player_id}: {e}")
            raise HTTPException(status_code=503, detail="Database operation failed")
        except Exception as e:
            logger.error(f"Unexpected error adding coins to player {player_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

