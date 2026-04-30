import services.game.Game as g

class Simulation:
    def __init__(self, holeCards, communityCards):
        # holeCards: list of [card, card] or None per player
        # communityCards: list of card tuples or None (up to 5)
        self.holeCards = holeCards
        self.communityCards = communityCards
        self.wins = 0
        self.ties = 0
        self.loss = 0

    def iterate(self):
        deck = g.Deck()

        randomizedHoleCards = [hand[:] if hand is not None else None for hand in self.holeCards]
        randomizedCommunityCards = self.communityCards[:]

        for hand in randomizedHoleCards:
            if hand is not None:
                for card in hand:
                    if card is not None:
                        deck.drawCard(card)

        for card in randomizedCommunityCards:
            if card is not None:
                deck.drawCard(card)

        for i in range(len(randomizedHoleCards)):
            hand = randomizedHoleCards[i]
            if hand is None:
                c1 = g.getCardAsTuple(deck.drawRandomCard())
                c2 = g.getCardAsTuple(deck.drawRandomCard())
                randomizedHoleCards[i] = [c1, c2]
            else:
                if hand[0] is None:
                    randomizedHoleCards[i][0] = g.getCardAsTuple(deck.drawRandomCard())
                if hand[1] is None:
                    randomizedHoleCards[i][1] = g.getCardAsTuple(deck.drawRandomCard())

        for i in range(len(randomizedCommunityCards)):
            if randomizedCommunityCards[i] is None:
                randomizedCommunityCards[i] = g.getCardAsTuple(deck.drawRandomCard())

        game = g.Game(randomizedHoleCards, randomizedCommunityCards)
        result = game.getIndexResult(0)

        if result == 0:
            self.loss += 1
        elif result == 1:
            self.ties += 1
        elif result == 2:
            self.wins += 1

    def getOdds(self, iterations=1000):
        for _ in range(iterations):
            self.iterate()
        total = self.wins + self.ties + self.loss
        return {
            "win":  self.wins / total,
            "tie":  self.ties / total,
            "loss": self.loss / total
        }
   ## def getAverageEvaluation():

