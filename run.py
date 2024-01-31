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