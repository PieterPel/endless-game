from Board import Board
from Square import Square


class Game:
    def __init__(self):
        self.board = Board()

    def play(self):
        self.board.shuffleDeck()
        self.board.setUpBoard()

        while self.board.numberOfCardsOnBoard() < 49:
            print(self.board)
            validSquare = False

            while not validSquare:
                xvalue = int(input("What is the x-value of the square you choose? (start at 0)"))
                yvalue = int(input("What is the y-value of the square you choose? (start at 0"))
                chosenSquare = self.board.grid[xvalue][yvalue]
                if Square.isFilled(chosenSquare) or len(self.board.filledNeighbours(chosenSquare)) == 0:
                    print("This square isn't valid")
                    continue
                validSquare = True

            options = self.board.options(chosenSquare)
            choice = int(input(f"What is your option? 0: {options[0]} or 1: {options[1]}"))
            option = options[choice]
            newCard = self.board.pullCard()
            self.board.replaceCard(xvalue, yvalue, newCard)

            print(str(self.board))

            if self.board.cardAllowed(newCard, chosenSquare, option):
                print('Correct!')
                continue
            else:
                print('Wrong!')
                self.board.clearCross(chosenSquare)



