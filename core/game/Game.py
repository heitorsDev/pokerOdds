import random 

def getCardRankAsInt(rank):
    return ['2','3','4','5','6','7','8','9','T','J','Q','K','A'].index(rank)

def getCardAsTuple(string):
    return (string[0], string[1])


class Deck:
    def __init__(self):
        self.restore()

    def drawRandomCard(self):
        
        card = self.array.pop(0)
        return card
    
    def restore(self):
        suits = ['d','s','c','h']
        ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        self.array = []
        for suit in suits:
            for rank in ranks:
                self.array.append(rank+suit)
        random.shuffle(self.array)

class Game:
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

    def getStraight(self, array):
        unique_ranks = sorted(set([getCardRankAsInt(c[0]) for c in array]))

        if 12 in unique_ranks:
            unique_ranks.insert(0, -1)

        straight_high = None

        for i in range(len(unique_ranks) - 4):
            window = unique_ranks[i:i+5]
            if window[4] - window[0] == 4:
                straight_high = window[-1]

        if straight_high is not None:
            return [c for c in array if getCardRankAsInt(c[0]) in [
                straight_high - i for i in range(5)
            ]]
        return []


    def __init__(self, holeHands, communityCards):
        self.holeHands = holeHands
        self.communityCards = communityCards
        self.playerHands = []

        for hand in holeHands:
            combination = communityCards + hand
            combination.sort(key=lambda x: getCardRankAsInt(x[0]))

            handResult = ["high_card", combination[-1], combination[-2]]

            rankCounts = []
            suitCounts = []

            for card in combination:
            
                if len(list(filter(lambda x: x[0] == card[0], [r[0][0] for r in rankCounts]))) == 0:
                    count = len(list(filter(lambda x: x[0] == card[0], combination)))
                    rankCounts.append((card, count))

                
                if len(list(filter(lambda x: x == card[1], [s[0][1] for s in suitCounts]))) == 0:
                    suitList = list(filter(lambda x: x[1] == card[1], combination))
                    suitCounts.append((card, len(suitList)))

                    if len(suitList) >= 5:
                        handResult = ["flush", suitList, [c for c in combination if c not in suitList][-1]]

                        straightList = self.getStraight(suitList)
                        if straightList != []:
                            ranks = sorted([getCardRankAsInt(c[0]) for c in straightList])
                            if ranks == [8,9,10,11,12]:  # T J Q K A
                                handResult = ["royal_flush", straightList, None]
                            else:
                                handResult = ["straight_flush", straightList, None]

            straightList = self.getStraight(combination)
            if straightList != [] and handResult[0] not in ["straight_flush", "royal_flush", "flush"]:
                handResult = ["straight", straightList, None]

            pairs = list(filter(lambda x: x[1] == 2, rankCounts))
            pairs.sort(key=lambda x: getCardRankAsInt(x[0][0]))

            trios = list(filter(lambda x: x[1] == 3, rankCounts))
            trios.sort(key=lambda x: getCardRankAsInt(x[0][0]))

            quads = list(filter(lambda x: x[1] == 4, rankCounts))
            quads.sort(key=lambda x: getCardRankAsInt(x[0][0]))

            if handResult[0] not in ["straight_flush", "royal_flush"]:
                if len(quads) != 0:
                    quad_rank = quads[-1][0][0]
                    filtered = [c for c in combination if c[0] != quad_rank]
                    handResult = ["four_of_a_kind", quads[-1], filtered[-1]]

                elif len(trios) >= 1 and len(pairs) >= 1:
                    handResult = ["full_house", (trios[-1], pairs[-1]), None]

                elif handResult[0] not in ["flush", "straight"]:
                    if len(trios) >= 1:
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

            self.playerHands.append(handResult)
            print(handResult)


    def getIndexResult(self):
        pass