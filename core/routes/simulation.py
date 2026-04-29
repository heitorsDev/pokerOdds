import fastapi
import pydantic
from models.gameState import GameState



router  = fastapi.APIRouter()

@router.post("/simulate/")
async def simulateGame(gameState: GameState):
    print(gameState)