import random
import time

def welcome_screen():
    """
    Welcomes the user.
    Displays ASCII art and lets user start the game.
    """
    art = r"""
        __        __   _
        \ \      / /__| | ___ ___  _ __ ___   ___
         \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \
          \ V  V /  __/ | (_| (_) | | | | | |  __/
           \_/\_/ \___|_|\___\___/|_| |_| |_|\___

        Instructions:
            - Instruction 1. Start by entering a letter between A-E and press enter. 
            - Instruction 2. Then enter a number between 1-5 and press enter.
            - Instruction 3. A message will let you know if you hit/miss your enemys ship.
            - Instruction 4. Keep firing missiles until you sink your enemys fleet or run out of missiles.

            (ALL SHIPS ARE MADE OUT OF A SINGLE 'X') 
            """
    print(art)
    time.sleep(5)


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
            print("%d|%s|" % (row_num, "|".join(row)))
            row_num += 1


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
        Intergers translated into co-ordinates and a ship is
        places on the board.
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
            while y_col not in ['A', 'B', 'C', 'D', 'E']:
                print('Co-Ordinate Error. Enter a letter A-E.')
                y_col = input('Enter Co-Ordinate (A-E): ').upper()

            x_row = input('Enter Co-Ordinate (1-5): ')
            while x_row not in ['1', '2', '3', '4', '5']:
                print('Co-Ordinate Error. Enter a number 1-5.')
                x_row = input('Enter Co-ordinate (1-5)')

            return int(x_row) - 1, GameBoard.co_ordinates()[y_col]

        except ValueError or KeyError:
            print('Not a valid input. Enter a number or letter.')
            return Ship.user_launch_mission()

    def enemy_launch_mission():
        """
        Takes co-ordinates from a random choice of letters and integers
        to generate a computer launch
        """
        letter_choices = ['A', 'B', 'C', 'D', 'E']
        y_col = random.choice(letter_choices).upper()
        x_row = random.randint(0, 4)
        return int(x_row), GameBoard.co_ordinates()[y_col]

    @staticmethod
    def count_damaged_ships(board):
        damaged_ships = 0
        for row in board:
            for column in row:
                if column == 'X':
                    damaged_ships += 1
        return damaged_ships


def run_battleship_game():
    """
    This is the main function.
    It generates the gameboard and the ships.
    Incorporates a turn limit.
    prompts user for input and provides feedback on turn results.
    """
    enemy_board = [[' '] * 5 for _ in range(5)]
    enemy_target_board = GameBoard([[' '] * 5 for _ in range(5)])
    user_board = [[' '] * 5 for _ in range(5)]
    user_target_board = GameBoard([[' '] * 5 for _ in range(5)])

    Ship.generate_fleet(enemy_board)
    Ship.generate_fleet(user_board)

    missiles = 15
    enemy_missiles = 15
    while missiles > 0:
        enemy_target_board.generate_board('Enemy Target')
        user_target_board.generate_board('User Target')

        user_x_row, user_y_col = Ship.user_launch_mission()
        while (
            user_target_board.board[user_x_row][user_y_col] == '-'
            or user_target_board.board[user_x_row][user_y_col] == 'X'
        ):
            print('That location has already been fired at.')
            print('Choose a new location.')
            user_x_row, user_y_col = Ship.user_launch_mission()

        if enemy_board[user_x_row][user_y_col] == 'X':
            print('Thats a hit! Enemy ship down!')
            user_target_board.board[user_x_row][user_y_col] = 'X'
        else:
            print('Thats a miss. No ship at given location.')
            user_target_board.board[user_x_row][user_y_col] = '-'

        if Ship.count_damaged_ships(user_target_board.board) == 4:
            print('Well done! You sank the enemy fleet!')
            break
        else:
            missiles -= 1
            print(f'Missiles remaining: {missiles}.')
            if missiles == 0:
                print('Out of missiles! The enemy got away.')

                user_target_board.generate_board('User Target')

        enemy_x_row, enemy_y_col = Ship.enemy_launch_mission()
        while (
            enemy_target_board.board[enemy_x_row][enemy_y_col] == '-'
            or enemy_target_board.board[enemy_x_row][enemy_y_col] == 'X'
        ):
            enemy_x_row, enemy_y_col = Ship.enemy_launch_mission()

        if user_board[enemy_x_row][enemy_y_col] == 'X':
            print('Thats a hit! Enemy sunk one of our ships!')
            enemy_target_board.board[enemy_x_row][enemy_y_col] = 'X'
        else:
            print('Enemy missed their shot!')
            enemy_target_board.board[enemy_x_row][enemy_y_col] = '-'

        if Ship.count_damaged_ships(enemy_target_board.board) == 4:
            print('Retreat! All of our ships has been sunk!')
            break
        else:
            enemy_missiles -= 1
            if enemy_missiles == 0:
                print('The enemy has used all their missiles.')

                enemy_target_board.generate_board('Enemy Target')

    game_over()


def game_over():
    """
    This function runs when all ships has been sunk.
    Prompts the user to start new game or exit game.
    """
    print('Game Over!')
    restart = input('Do you want to try again? Y/N: \n').lower()

    if restart == 'y':
        run_battleship_game()
    elif restart == 'n':
        print('Thank you for your service! You are relieved of duty!')
        quit()
    else:
        print('Input Error. Type Y/N.')
        game_over()


def main():

    welcome_screen()
    run_battleship_game()


if __name__ == '__main__':
    main()                                                                                                       