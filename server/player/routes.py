from fastapi import APIRouter, HTTPException, status
from player.service import PlayerService
from player.schemas import PlayerIn, PlayerOut
from typing import List
import logging

logger = logging.getLogger(__name__)

player_router = APIRouter(
    prefix="/players",
    tags=["players"]
)

@player_router.post("/", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
async def create_player(player: PlayerIn):
    """Create a new player."""
    result = await PlayerService().create_player(player)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create player"
        )
    return result

@player_router.get("/", response_model=List[PlayerOut])
async def get_players():
    """Get all players."""
    return await PlayerService().get_players()

@player_router.get("/{player_id}", response_model=PlayerOut)
async def get_player(player_id: str):
    """Get a specific player by ID."""
    result = await PlayerService().get_player(player_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return result

@player_router.put("/{player_id}", response_model=PlayerOut)
async def update_player(player_id: str, player: PlayerIn):
    """Update a player."""
    result = await PlayerService().update_player(player_id, player)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return result

@player_router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: str):
    """Delete a player."""
    success = await PlayerService().delete_player(player_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

@player_router.patch("/{player_id}/coins", response_model=PlayerOut)
async def add_coins(player_id: str, increment: int):
    """Add coins to a player."""
    result = await PlayerService().add_coins(player_id, increment)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return result
