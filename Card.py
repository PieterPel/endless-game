class Card:
    def __init__(self, value, suit):
        self.value = value  # The value of the card (2 - 14)
        self.suit = suit  # The suit of the card (1 - 4)

    def __str__(self):
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'S', 'C']
        return f"[{values[self.value - 2]}{suits[self.suit - 1]}]".ljust(5)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value and self.suit == other.suit
