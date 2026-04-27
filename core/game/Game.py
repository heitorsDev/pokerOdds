import random 
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

