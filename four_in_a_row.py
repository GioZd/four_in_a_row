'''
FILE NAME: four_in_a_row.py
LATEST VERSION: 1.0
LAST EDIT: 22/12/2022
AUTHOR: Giovanni Zedda
DESCRIPTION: Play 4-in-row!
CHANGELOG:
'''
# useful charset
# "○●◌◆◇■◻◎◍◉Ｏ◯⭕"
# for colored text, write '\u001b[' followed by ANSI escape code 
# and finally the string you want to be colored
# https://en.wikipedia.org/wiki/ANSI_escape_code


import os
import keyboard
from time import sleep

# values for a standard game
WIDTH = 7
HEIGHT = 6
N_IN_A_ROW = 4
CHARSET =   ('○', #void char
            '\u001b[32m◉ \u001b[0m', #green ◉ player
            '\u001b[31m◉ \u001b[0m'  #red ◉ player
            )

class Board():
    """
    Board object represents a board with all necessary 
    attributes and methods to play the n-in-a-row game

    Attributes
    ----------
    height : int
    width : int
    many : int
        Number of consecutive equal tokens
        which are needed for a player to win
    board : list[list[str]]
        Matrix which contains the board
        and some explanatory rows 
    
    Methods
    -------
    is_winner(player: str) -> bool
        returns whether {player} wins or not
    print() -> None
        displays the matrix on separate rows
    __set_up_board() -> None
        clears up the board all with '○'s
    """
    def __init__(self, 
                 height: int = HEIGHT, width: int = WIDTH,
                 many: int = N_IN_A_ROW) -> None:

        self.height = height
        self.width = width
        self.many = many
        self.voidchr = CHARSET[0]
        self.board = self.__set_up_board()

    def __set_up_board(self) -> list[list[str]]:
        """This private method clears up the board"""
        board = [
            [self.voidchr for _ in range(self.width)] for 
            _ in range(self.height)
        ]
        # board.append([i for i in range(self.width)])
        return board

    def is_winner(self, player: str) -> bool:
        """
        This method returns True if 
        {self.many} in a row are found 
        else False

        Inputs
        ------
        player: str
            a short string or char that represents a player's token
        """
        # checks all horizontal lines
        for row in self.board[:self.height]:     
            if player*self.many in ''.join(row):
                return True

        #checks all vertical lines
        for col in range(self.width):
            column = [
                self.board[height][col] for 
                height in range(self.height)
            ] #genera un vettore colonna ad ogni iterazione
            if player*self.many in ''.join(column):
                return True  

        #checks all discending diagonals
        for top in range(self.height):
            discending_diagonal = [
                self.board[top+i][i] for
                i in range(self.height-top)
            ]
            if player*self.many in ''.join(discending_diagonal):
                return True
          
        for top in range(self.width):
            discending_diagonal = [
                self.board[i][top+i] for
                i in range(min(self.height, self.width-top))
            ]
            if player*self.many in ''.join(discending_diagonal):
                return True

        #checks all ascending diagonals
        for bottom in range(self.height):
            ascending_diagonal = [
                self.board[bottom-i][i] for
                i in range(bottom+1)
            ]
            if player*self.many in ''.join(ascending_diagonal):
                return True
        
        for bottom in range(self.width):
            ascending_diagonal = [
                self.board[self.height-i-1][bottom+i] for
                i in range(min(self.height, self.width-bottom))
            ]
            if player*self.many in ''.join(ascending_diagonal):
                return True

        return False

    def insert(self, player: str, column: int = 0) -> bool: 
        """
        This method pulls down a token in a given column

        Inputs
        ------
        player: str
            a short string or char that represents a player's token
        column: int
            number of the column in which the token is inserted  
        """
        top = 0
        while top < self.height:
            if self.board[top][column] == self.voidchr:
                top += 1
            else:
                break
        top -= 1
        if top >= 0:
            self.board[top][column] = player
            return True
        return False

    def print(self) -> None:
        """
        This method displays the board
        arranged in rows and columns
        """
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print(f"{self.board[row][col]:<2}", end = ' ')
            print()

    def __repr__(self) -> str:
        return str(self.board)

#--------------------------------------------------------------------------
def main():
    name_player_1 = input("Nome giocatore 1: ")
    name_player_2 = input("Nome giocatore 2: ")
    board = Board()

    current_player = CHARSET[1]
    for i in range(board.width*board.height):
        current_player = CHARSET[i%2 +1]
        choice = choose_column(current_player, board)
        while(not board.insert(current_player, choice)):
            choice = choose_column(current_player, board)

        if board.is_winner(current_player):
            os.system('cls' if os.name == 'nt' else 'clear')
            board.print()
            print(
                f"{name_player_1} ha vinto!" if current_player == CHARSET[1] else
                f"{name_player_2} ha vinto!"
            )
            return        

    print("Pareggio!")

def choose_column(player: str, board: Board) -> int:
    """
    Graphic input function.
    Returns a column index

    Inputs
    ------
    player: str
        player's token
    board: Board    
        the board where the game is played
    """
    column = int(board.width/2)
    os.system('cls' if os.name == 'nt' else 'clear')
    heading = make_heading(player, column)
    print(heading)
    board.print()
    while not ( keyboard.is_pressed('space') 
                or keyboard.is_pressed('enter')
                or keyboard.is_pressed('down')  ):
        if keyboard.is_pressed('left') or keyboard.is_pressed('right'):
            if keyboard.is_pressed('left'):
                column = (column - 1) % board.width
            if keyboard.is_pressed('right'):
                column = (column + 1) % board.width 
            os.system('cls' if os.name == 'nt' else 'clear')
            heading = make_heading(player, column)
            print(heading)
            board.print()
            sleep(0.2)

    while ( keyboard.is_pressed('space') 
            or keyboard.is_pressed('enter')
            or keyboard.is_pressed('down')  ):
        continue

    return column

def make_heading(player: str, column: int = 0, width: Board = WIDTH) -> str:
    """
    makes a string that shows where a token is going to fall

    Inputs
    ------
    player: str
        a short string or char that represents a player's token
    column: int
        the column-th space of the string that will be filled with player
    width: int
        maximum number of columns
    """
    return (
        '   ' * column
        + f"{player:<2}"
        + '   ' * (width - column - 1)
    )

if __name__ == "__main__":
    main()