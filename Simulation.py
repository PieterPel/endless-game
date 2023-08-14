import random
from Square import Square
from Card import Card
from Board import Board


class Simulation:
    def __init__(self):
        self.maxRuns = 1000
        self.instance = 1
        self.alpha = 0.0
        self.crossesCleared = 0
        self.numCardsLaid = 0
        self.mostCards = 0
        self.board = Board()
        self.gottenClose = False
        self.printing = True

    def simulate(self):
        self.board.shuffleDeck()
        self.board.setUpBoard()

        while self.board.numberOfCardsOnBoard() < 49 and self.instance <= self.maxRuns:
            # bestSquare = self.board.bestSquareToPlay2(self.alpha)
            bestSquare = self.board.bestSquareToPlay()
            whatToSay = self.board.whatToSay(bestSquare)
            newCard = self.board.pullCard()

            if self.printing:
                print(f'Playing square ({bestSquare.x}, {bestSquare.y}), saying: {self.board.whatToSay(self.board.grid[bestSquare.x][bestSquare.y])}')
                print(f'Probability of success: {self.board.chanceOfSquare(self.board.grid[bestSquare.x][bestSquare.y])}')
                # print(f'Record number of cards: {self.mostCards}')
                print(f'Number of cards on the board: {self.board.numberOfCardsOnBoard()}')

            self.board.replaceCard(bestSquare.x, bestSquare.y, newCard)
            self.numCardsLaid += 1

            if self.printing:
                print(str(self.board))

            if self.board.cardAllowed(newCard, bestSquare, whatToSay):
                continue
            else:
                self.board.clearCross(bestSquare)
                self.crossesCleared += 1

            if self.board.numberOfCardsOnBoard() > self.mostCards:
                self.mostCards = self.board.numberOfCardsOnBoard()

            if self.board.numberOfCardsOnBoard() > 40:
                self.gottenClose = True

            self.instance += 1
