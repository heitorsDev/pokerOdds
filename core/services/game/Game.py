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
    
    def drawCard(self, cardTuple):
        string = cardTuple[0]+cardTuple[1]
        self.array.pop(self.array.index(string))

class Game:
    

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


    def handScore(self, hand):
        hand_type = hand[0]
        BASE = 13  
        
        type_rank = {
            "royal_flush":    8,
            "straight_flush": 7,
            "four_of_a_kind": 6,
            "full_house":     5,
            "flush":          4,
            "straight":       3,
            "three_of_a_kind":2,
            "two_pair":       1,
            "pair":           0,
            "high_card":     -1,
        }[hand_type]

        def r(card):
            return getCardRankAsInt(card[0])

        T = type_rank

        if hand_type == "royal_flush":
            return T * BASE**5

        elif hand_type == "straight_flush":
            high = max(r(c) for c in hand[1])
            return T * BASE**5 + high * BASE**4

        elif hand_type == "four_of_a_kind":
            quad = r(hand[1][0])
            kicker = r(hand[2])
            return T * BASE**5 + quad * BASE**4 + kicker * BASE**3

        elif hand_type == "full_house":
            trio = r(hand[1][0][0])
            pair = r(hand[1][1][0])
            return T * BASE**5 + trio * BASE**4 + pair * BASE**3

        elif hand_type == "flush":
            ranks = sorted([r(c) for c in hand[1]], reverse=True)[:5]
            score = T * BASE**5
            for i, rank in enumerate(ranks):
                score += rank * BASE**(4 - i)
            return score

        elif hand_type == "straight":
            high = max(r(c) for c in hand[1])
            return T * BASE**5 + high * BASE**4

        elif hand_type == "three_of_a_kind":
            trio = r(hand[1][0])
            kickers = sorted([r(c) for c in hand[2]], reverse=True)
            return T * BASE**5 + trio * BASE**4 + kickers[0] * BASE**3 + kickers[1] * BASE**2

        elif hand_type == "two_pair":
            hi_pair = r(hand[1][0][0])
            lo_pair = r(hand[1][1][0])
            kicker = r(hand[2])
            return T * BASE**5 + hi_pair * BASE**4 + lo_pair * BASE**3 + kicker * BASE**2

        elif hand_type == "pair":
            pair = r(hand[1][0])
            kickers = sorted([r(c) for c in hand[2]], reverse=True)
            return T * BASE**5 + pair * BASE**4 + kickers[0] * BASE**3 + kickers[1] * BASE**2 + kickers[2] * BASE**1

        elif hand_type == "high_card":
            
            return T * BASE**5 + r(hand[1]) * BASE**4 + r(hand[2]) * BASE**3


    def __init__(self, holeHands, communityCards):
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
        self.holeHands = holeHands
        self.communityCards = communityCards
        self.playerHands = []
        # hand type, cards, kicker, player index
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
                        handResult = ["flush", suitList, None, holeHands.index(hand)]
                        straightList = self.getStraight(suitList)
                        if straightList != []:
                            ranks = sorted([getCardRankAsInt(c[0]) for c in straightList])
                            if ranks == [8,9,10,11,12]:  # T J Q K A
                                handResult = ["royal_flush", straightList, None, holeHands.index(hand)]
                            else:
                                handResult = ["straight_flush", straightList, None, holeHands.index(hand)]

            straightList = self.getStraight(combination)
            if straightList != [] and handResult[0] not in ["straight_flush", "royal_flush", "flush"]:
                handResult = ["straight", straightList, None, holeHands.index(hand)]

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
                    handResult = ["four_of_a_kind", quads[-1], filtered[-1], holeHands.index(hand)]

                elif len(trios) >= 1 and len(pairs) >= 1:
                    handResult = ["full_house", (trios[-1], pairs[-1]), None, holeHands.index(hand)]

                elif handResult[0] not in ["flush", "straight"]:
                    if len(trios) >= 1:
                        trio_rank = trios[-1][0][0]
                        filtered = [c for c in combination if c[0] != trio_rank]
                        handResult = ["three_of_a_kind", trios[-1], filtered[-2:], holeHands.index(hand)]

                    elif len(pairs) > 1:
                        high_pair = pairs[-1][0][0]
                        low_pair = pairs[-2][0][0]
                        filtered = [c for c in combination if c[0] != high_pair and c[0] != low_pair]
                        handResult = ["two_pair", (pairs[-1], pairs[-2]), filtered[-1], holeHands.index(hand)]

                    elif len(pairs) == 1:
                        pair_rank = pairs[-1][0][0]
                        filtered = [c for c in combination if c[0] != pair_rank]
                        handResult = ["pair", pairs[-1], filtered[-3:], holeHands.index(hand)]

            self.playerHands.append(handResult)
        self.playersResult = []
        for playerHand in self.playerHands:
            self.playersResult.append(self.handScore(playerHand))

    def getIndexResult(self, index):

        higher = self.playersResult[index]==max(self.playersResult)
        if not higher:
            return 0
        
        indexes = []
        start_pos = 0
        while True:
            try:
                idx = self.playersResult.index(self.playersResult[index], start_pos)
                indexes.append(idx)
                start_pos = idx + 1
            except ValueError:
                break
        
        return 2 if len(indexes)==1 else 1
    
