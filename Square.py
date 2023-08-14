from Card import Card

class Square:
    def __init__(self, x, y):
        self.x = x  # The x coordinate of the square
        self.y = y  # The y coordinate of the square
        self.card = 'empty'  # The Card that is placed on the square

    def isFilled(self):
        return self.card != 'empty'

    def __str__(self):
        if self.card == 'empty':
            return ''.ljust(5)
        else:
            return str(self.card)
