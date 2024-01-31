import random
import gspread
from google.oauth2.service_account import Credentials









# Global variables assigned to allow access through Google APIs to gspread.
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleship-game')

class GameBoard:
    """
    Stores the values that are needed to generate gameboard.
    Dictionary stores letter/number values for the co-ordinates.
    Stores values for a board outline for user visuals.
    """

    def __init__(self, board):
        self.board = board

    @staticmethod
    def co_ordinates():
        co_ordinates = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
           
        }
        return co_ordinates

    def generate_board(self, label):
        print(f'\n{label} Board:')
        print('  A B C D E ')
        print('  x-x-x-x-x ')
        row_num = 1
        for row in self.board:
            print("%d|%s|" % (row_number, "|".join(row)))
            row_number += 1

class Ship:
    """
    Stores the values that are needed to generate ships.
    """
    def __init__(self, board):
        self.board = board


    @staticmethod
    def generate_fleet(board):
        """
        The for statement loops through the board co-ordinate lists.
        Generates random integers and asigns the letter 'x' as a ship to each.
        Intergers translated into co-ordinates and a ship is places on the board.
        """

        for i in range(4):
            x_row, y_col = random.randint(0, 4), random.randint(0, 4)
            while board[x_row][y_col] == 'X':
                x_row = random.randint(0, 4)
                y_col = random.randint(0, 4)
            board[x_row][y_col] = 'X'
        return board

    @staticmethod
    def user_launch_mission():
        """
        Takes user input and checks for validation.
        Assigns the launch to a co-ordinate and checks for hit/miss/sink
        Feeds back to user
        """
        try:
            y_col = input('Enter Co-Ordinate (A-E): ').upper()
            while y_col not in 'ABCDE':
                print('Co-Ordinate Error. Enter a letter A-E.')
                y_col = input('Enter Co-Ordinate (A-E): ').upper()

            x_row = input('Enter Co-Ordinate (1-5): ')
            while x_row not in '12345':
                print('Co-Ordinate Error. Enter a number 1-5.')
                x_row = input('Enter Co-ordinate (1-5)')

            return int(x_row) - 1, GameBoard.co_ordinates()[y_col]

        except ValueError or KeyError:
            print('Not a valid input. Enter a number or letter.')
            return ship.user_launch_mission()

    def enemy_launch_mission():
        """
        Takes co-ordinates from a random choice of letters and integers
        to generate a computer launch
        """
        letter_choices = ['A', 'B', 'C', 'D', 'E']
        y_col = random.choice(letter_choices).upper()
        x_row = random.randint(0, 8)
        return int(x_row), GameBoard.co_ordinates()[y_col]

    @staticmethod
    def count_damaged_ships(board):
        damaged_ships = 0
        for row in board:
            for column in row:
                if column == 'X':
                    damaged_ships += 1
        return damaged_ships  