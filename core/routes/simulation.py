import fastapi
from models.gameState import GameState, Hand, Card, CommunityCards, HandOddsResult
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


def validate_game_state(gameState: GameState):
    if not gameState.hands:
        raise fastapi.HTTPException(status_code=400, detail="At least one hand is required.")

    seen_cards: set[str] = set()

    def add_card(card: Card | None):
        if card is None:
            return
        card_key = f"{card.rank}{card.suit}"
        if card_key in seen_cards:
            raise fastapi.HTTPException(status_code=400, detail=f"Duplicate card in input: {card_key}")
        seen_cards.add(card_key)

    for hand in gameState.hands:
        if hand is not None:
            add_card(hand.cards[0])
            add_card(hand.cards[1])

    for card in gameState.communityCards.cards:
        add_card(card)


router  = fastapi.APIRouter()
##communityCards=CommunityCards(cards=[Card(rank='A', suit='d'), None]) hands=[Hand(cards=(Card(rank='A', suit='s'), Card(rank='A', suit='c')))]
@router.post("/simulate/", response_model=HandOddsResult)
async def simulateGame(gameState: GameState):
    validate_game_state(gameState)

    queryHands = gameState.hands
    queryCommunityCards = gameState.communityCards
    simulationHands = []
    for hand in queryHands:
        simulationHands.append(decodeQueryHand(hand))
    simulationCommunityCards = decodeQueryCommunityCards(queryCommunityCards)

    simulation = Simulation(simulationHands, simulationCommunityCards)
    result = simulation.getOdds()
    return HandOddsResult(win=result["win"], tie=result["tie"], loss=result["loss"])
