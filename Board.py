import numpy as np
import random
from Square import Square
from Card import Card


class Board:
    def __init__(self):
        # Initialize
        self.lastCardPlayed = Square(0, 0)
        self.width = 7
        self.height = 7

        # Initialize the empty grid
        self.grid = [[None] * 7 for i in range(0, 7)]
        for x in range(0, 7):
            for y in range(0, 7):
                newSquare = Square(x, y)
                self.grid[x][y] = newSquare

        # Initialize the deck
        self.deck = []
        for value in range(2, 15):
            for suit in range(1, 5):
                newCard = Card(value, suit)
                self.deck.append(newCard)

    # Sets up the board
    def setUpBoard(self):
        for x in range(0, 7):
            newCard = self.deck.pop(0)
            self.replaceCard(x, 3, newCard)
            if x != 3:  # Ensure that the middle isn't done twice
                newCard = self.deck.pop(0)
                self.replaceCard(3, x, newCard)

    # Returns the number of cards on the board
    def numberOfCardsOnBoard(self):
        number = 0
        for x in range(0, 7):
            for y in range(0, 7):
                if Square.isFilled(self.grid[x][y]):
                    number += 1
        return number

    # Shuffles the deck
    def shuffleDeck(self):
        random.shuffle(self.deck)

    # Returns the squares that are filled by a card neighbouring a given square
    def filledNeighbours(self, square):
        # Initialize, start with the square having all four filled neighbours
        ownX = square.x
        ownY = square.y
        listOfSquares = []
        hasLeftNeighbour = True
        hasRightNeighbour = True
        hasBottomNeighbour = True
        hasTopNeighbour = True

        # Removes the neighbours of the squares in the corners
        if ownX == 0 and ownY == 0:
            hasBottomNeighbour = False
            hasLeftNeighbour = False
        elif ownX == 0 and ownY == 6:
            hasTopNeighbour = False
            hasLeftNeighbour = False
        elif ownX == 6 and ownY == 0:
            hasBottomNeighbour = False
            hasRightNeighbour = False
        elif ownX == 6 and ownY == 6:
            hasTopNeighbour = False
            hasRightNeighbour = False

        # Removes the squares from the squares on the edges
        elif ownX == 0:
            hasLeftNeighbour = False
        elif ownX == 6:
            hasRightNeighbour = False
        elif ownY == 0:
            hasBottomNeighbour = False
        elif ownY == 6:
            hasTopNeighbour = False

        # Adds the neighbours to the list
        if hasLeftNeighbour and Square.isFilled(self.grid[ownX - 1][ownY]):
            listOfSquares.append(self.grid[ownX - 1][ownY])
        if hasRightNeighbour and Square.isFilled(self.grid[ownX + 1][ownY]):
            listOfSquares.append(self.grid[ownX + 1][ownY])
        if hasBottomNeighbour and Square.isFilled(self.grid[ownX][ownY - 1]):
            listOfSquares.append(self.grid[ownX][ownY - 1])
        if hasTopNeighbour and Square.isFilled(self.grid[ownX][ownY + 1]):
            listOfSquares.append(self.grid[ownX][ownY + 1])

        return listOfSquares

    # Returns a boolean that indicates if a placed card is correct or wrong
    def cardAllowed(self, newCard, square, whatSaid):
        cardValue = newCard.value
        cardSuit = newCard.suit
        filledNeighbours = self.filledNeighbours(square)

        if len(filledNeighbours) == 0:  # The card has 0 filled neighbours
            return False

        if len(filledNeighbours) == 1:  # The card has 1 filled neighbour
            if filledNeighbours[0].card.value < cardValue and whatSaid == 'Higher':
                return True
            if filledNeighbours[0].card.value > cardValue and whatSaid == 'Lower':
                return True

        if len(filledNeighbours) == 2:  # The card has 2 filled neighbours
            if filledNeighbours[0].card.value >= filledNeighbours[1].card.value:
                highestValue = filledNeighbours[0].card.value
                lowestValue = filledNeighbours[1].card.value
            else:
                highestValue = filledNeighbours[1].card.value
                lowestValue = filledNeighbours[0].card.value
            if lowestValue < cardValue < highestValue and whatSaid == 'Inside':
                return True
            if (lowestValue > cardValue or highestValue < cardValue) and whatSaid == 'Outside':
                return True

        if len(filledNeighbours) >= 3:  # The card has 3 or 4 filled neighbours
            gotIt = False
            for neighbour in filledNeighbours:
                if neighbour.card.suit == cardSuit:
                    gotIt = True

            if gotIt and whatSaid == 'Got it':
                return True

            if not gotIt and whatSaid == 'Do not have it':
                return True

        return False

    # Returns the options to say when placing a card
    def options(self, square):
        numFilledNeighbours = len(self.filledNeighbours(square))
        if numFilledNeighbours == 0:
            return 'Nothing'
        elif numFilledNeighbours == 1:
            return ['Higher', 'Lower']
        elif numFilledNeighbours == 2:
            return ['Inside', 'Outside']
        return ['Got it', 'Do not have it']  # Implied that number of filled neighbours is 3 or 4

    # Returns which option has the greatest chance of being correct
    def whatToSay(self, square):
        bestChance = 0
        bestOption = ''
        for option in self.options(square):
            if self.chanceToGetRight(square, option) > bestChance:
                bestOption = option

        return bestOption

    # Returns what the chance is that the prediction is correct for a given square
    def chanceToGetRight(self, square, whatSaid):
        # Ensure that a card is never placed on a filled square
        if Square.isFilled(square):
            return 0

        # Checks how many of the cards in the deck give a correct outcome
        counter = 0
        for card in self.deck:
            if self.cardAllowed(card, square, whatSaid):
                counter += 1

        # Compute the chance of being correct
        chance = counter / len(self.deck)
        return chance

    # Returns the chance that a square will be good with the best prediction
    def chanceOfSquare(self, square):
        return self.chanceToGetRight(square, self.whatToSay(square))

    def weightedChanceOfSquare(self, square, alpha):
        chance = self.chanceToGetRight(square, self.whatToSay(square))
        hazard = (self.numOfCardsGoneIfWrong(square) - 2) / 12  # -2 since two cards will always be lost
        weightedChance = alpha * hazard + (1 - alpha) * chance
        return weightedChance

    # Returns the square that has the highest chance of being correct
    def bestSquareToPlay(self):
        bestSquare = self.grid[0][0]
        bestChance = 0

        # Compute the chance for every feasible square
        for x in range(0, 7):
            for y in range(0, 7):
                if Square.isFilled(self.grid[x][y]):  # Don't consider squares that are filled
                    continue
                chance = self.chanceOfSquare(self.grid[x][y])
                if chance > bestChance:
                    bestChance = chance
                    bestSquare = self.grid[x][y]

        self.lastCardPlayed = bestSquare
        return bestSquare

    def bestSquareToPlay2(self, alpha):
        bestSquare = self.grid[0][0]
        bestWeightedChance = 0

        # Compute the chance for every feasible square
        for x in range(0, 7):
            for y in range(0, 7):
                if Square.isFilled(self.grid[x][y]):  # Don't consider squares that are filled
                    continue
                weightedChance = self.weightedChanceOfSquare(self.grid[x][y], alpha)
                if weightedChance > bestWeightedChance:
                    bestWeightedChance = weightedChance
                    bestSquare = self.grid[x][y]

        self.lastCardPlayed = bestSquare
        return bestSquare

    # Clears the cross if a prediction is incorrect
    def clearCross(self, originSquare):
        originX = originSquare.x
        originY = originSquare.y

        for i in range(0, 7):
            # Clear the squares and put the cards in the deck
            if Square.isFilled(self.grid[originX][i]):
                self.replaceCard(originX, i, 'empty')
            if Square.isFilled(self.grid[i][originY]):
                self.replaceCard(i, originY, 'empty')

        # Shuffle the deck
        self.shuffleDeck()

        # Place the new cards on the cross
        newCard = self.deck.pop(0)
        self.replaceCard(originX, 3, newCard)
        newCard = self.deck.pop(0)
        self.replaceCard(3, originY, newCard)

    # Replace a card on the board with a new card
    def replaceCard(self, x, y, newCard):
        if self.grid[x][y].isFilled():
            self.deck.append(self.grid[x][y].card)  # Add the replaced card to the bottom of the deck
        self.grid[x][y].card = newCard

    # Returns a drawn a card from the deck
    def pullCard(self):
        return self.deck.pop(0)

    # Returns a list of every square with at least one filled neighbour
    def listOfSquaresWithNeighbours(self):
        lis = []
        for x in range(0, 7):
            for y in range(0, 7):
                square = self.grid[x][y]
                if len(self.filledNeighbours(square)) > 0:
                    lis.append(square)
        return lis

    # Returns a random feasible square
    def randomFeasibleSquare(self):
        return random.choice(self.listOfSquaresWithNeighbours())

    # Returns a list of every card on the board
    def cardsOnBoard(self):
        cards = []
        for x in range(0, 7):
            for y in range(0, 7):
                if Square.isFilled(self.grid[x][y]):
                    cards.append(self.grid[x][y].card)
        return cards

    def numOfCardsGoneIfWrong(self, square):
        number = 0
        originX = square.x
        originY = square.y
        for i in range(0, 7):
            if Square.isFilled(self.grid[originX][i]):
                number += 1
            if Square.isFilled(self.grid[i][originY]) and i != originX:
                number += 1
        return number

    # For debugging: returns a list of every card that is a duplicate in the deck and on the board
    def findDuplicateCards(self):
        cardsOnBoard = self.cardsOnBoard()
        cardsInDeck = self.deck
        duplicates = []
        instances = []
        allCards = cardsOnBoard + cardsInDeck
        for card in allCards:
            if card in instances:
                duplicates.append(card)
            else:
                instances.append(card)
        return duplicates

    # Creates the string representation of the Board
    def __str__(self):
        string = ""
        for y in range(6, -1, -1):
            string = string + "\n"
            for x in range(0, 7):
                if x == self.lastCardPlayed.x and y == self.lastCardPlayed.y:
                    string = string + '\033[1m' + str(self.grid[x][y]) + '\033[0;0m'
                else:
                    string = string + str(self.grid[x][y])
        return string
