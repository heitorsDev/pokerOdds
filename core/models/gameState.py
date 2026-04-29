from pydantic import BaseModel, Field
from typing import Literal, Tuple
from enum import Enum

class Card(BaseModel):
    rank: Literal['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suit: Literal['d','s','c','h']

class Hand(BaseModel):
    cards: Tuple[Card, Card] | None
    
class CommunityCards(BaseModel):
    cards: list[Card] = Field(min_length=0, max_length=5)

class GameState(BaseModel):
    communityCards: CommunityCards
    hands: list[Hand]