import fastapi
import pydantic
from models.gameState import GameState, Hand, Card, CommunityCards
from services.game.MonteCarlo import Simulation
def decodeCard(card: Card):
    if card is None:
        return None

    return (card.rank, card.suit)

def decodeQueryHand(hand: Hand | None):
    if hand is None:
        return None

    return [
        decodeCard(hand.cards[0]),
        decodeCard(hand.cards[1])
    ]
    
def decodeQueryCommunityCards(communityCards: CommunityCards):
    array = communityCards.cards
    decodedCommunityCards = []
    for card in array:
        decodedCommunityCards.append(decodeCard(card))
    return decodedCommunityCards



router  = fastapi.APIRouter()
##communityCards=CommunityCards(cards=[Card(rank='A', suit='d'), None]) hands=[Hand(cards=(Card(rank='A', suit='s'), Card(rank='A', suit='c')))]
@router.post("/simulate/")
async def simulateGame(gameState: GameState):

    queryHands = gameState.hands
    queryCommunityCards = gameState.communityCards
    simulationHands = []
    for hand in queryHands:
        simulationHands.append(decodeQueryHand(hand))
    simulationCommunityCards= decodeQueryCommunityCards(queryCommunityCards)

    simulation = Simulation(simulationHands, simulationCommunityCards)
    result = simulation.getOdds()
    print(result)
