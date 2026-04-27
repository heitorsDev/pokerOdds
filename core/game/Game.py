import random 
def getCardRankAsInt(rank):
    return ['2','3','4','5','6','7','8','9','T','J','Q','K','A'].index(rank)
def getCardAsTuple(string):
        return (
            string[0],string[1]
        )
class Deck:
    array = []
    def __init__(self):
        self.restore()
        pass

    #Remove a random item in the array and return it
    def drawRandomCard(self):
        random.shuffle(self.array)
        card = self.array[0]
        self.array.pop(0)
        return card
    
    # Restore all deck array
    def restore(self):
        suits = ['d','s','c','h']
        ranks = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
        self.array = []
        for suit in suits:
            for rank in ranks:
                self.array.append(rank+suit)

    


class Game:
    hands = []
    communityCards = []
    
    handTypes = [
        "royal_flush",
        "straight_flush",
        "four_of_a_kind",
        "full_house",
        "flush",
        "straight",
        "three_of_a_kind",
        "two_pair",
        "pair",
        "high_card"
    ]
    # result: (hand type, combinations, kicker)
    def __init__(self, holeHands, communityCards):
        self.holeHands = holeHands
        self.playerHands = []
        self.communityCards = communityCards

        for hand in holeHands:
            combination = communityCards+hand
            combination.sort(key=lambda x: getCardRankAsInt(x[0]))
            handResult = ["high_card", combination[-1], combination[-2]]

            counts = []
            for card in combination:
                if len(list(filter(lambda x: x[0][0] == card[0], counts))) == 0:
                    counts.append((card, len(list(filter(lambda x: x[0] == card[0], combination)))))

            pairs = list(filter(lambda x: x[1] == 2, counts))
            pairs.sort(key=lambda x: getCardRankAsInt(x[0][0]))

            trios = list(filter(lambda x: x[1] == 3, counts))
            trios.sort(key=lambda x: getCardRankAsInt(x[0][0]))

            quads = list(filter(lambda x: x[1] == 4, counts))
            quads.sort(key=lambda x: getCardRankAsInt(x[0][0]))

            if len(quads) != 0:
                quad_rank = quads[-1][0][0]
                filtered = [c for c in combination if c[0] != quad_rank]
                handResult = ["four_of_a_kind", quads[-1], filtered[-1]]

            elif len(trios) >= 1 and len(pairs) >= 1:
                handResult = ["full_house", (trios[-1], pairs[-1])]

            elif len(trios) >= 1:
                trio_rank = trios[-1][0][0]
                filtered = [c for c in combination if c[0] != trio_rank]
                handResult = ["three_of_a_kind", trios[-1], filtered[-2:]]

            elif len(pairs) > 1:
                high_pair = pairs[-1][0][0]
                low_pair = pairs[-2][0][0]
                filtered = [c for c in combination if c[0] != high_pair and c[0] != low_pair]
                handResult = ["two_pair", (pairs[-1], pairs[-2]), filtered[-1]]

            elif len(pairs) == 1:
                pair_rank = pairs[-1][0][0]
                filtered = [c for c in combination if c[0] != pair_rank]
                handResult = ["pair", pairs[-1], filtered[-3:]]


    def getIndexResult(self):
        #0 Win
        #1 Loss
        #2 Tie
        pass

deck = Deck()
game = Game([
    [getCardAsTuple(deck.drawRandomCard()),getCardAsTuple(deck.drawRandomCard())], [getCardAsTuple(deck.drawRandomCard()),getCardAsTuple(deck.drawRandomCard())]]
, [
    getCardAsTuple(deck.drawRandomCard()), getCardAsTuple(deck.drawRandomCard()), getCardAsTuple(deck.drawRandomCard())
])