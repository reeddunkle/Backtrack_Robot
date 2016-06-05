import os
import time
from random import randint
os.system('cls' if os.name == 'nt' else 'clear')

def possible_directions(row, col):
    '''Returns the moves that are legal from the given coordinates.'''

    dirs = []
    if row == 0 and col == 0:
        dirs.append((0, 0))
    if col > 0 and (row, col-1) not in obstacles:
        dirs.append((row, col-1))
    if row > 0 and (row-1, col) not in obstacles:
        dirs.append((row-1, col))
    return dirs


def find_path(row, col):
    '''The backtrack algorithm -- returns the robots path.'''

    if (DEST_R == 0 and DEST_C == 1) or (DEST_R == 1 and DEST_C == 0):
        return [(0, 0), (row, col)]
    else:
        for coordinance in possible_directions(row, col):
            r, c = coordinance
            if r == 0 and c == 0:
                return [(0, 0)]

            solution = find_path(r, c)
            if solution:
                final = solution + [(r, c)]
                if row == DEST_R and col == DEST_C:
                    final += [(row, col)]
                return final


def create_board(row, col):
    '''Returns an array representation of the board.'''

    board = []
    for r in range(row + 1):
        board.append([])
        for c in range(col + 1):
            if (r, c) in obstacles:
                board[r].append("[X]")
            else:
                board[r].append("[ ]")
    return board


def convert_coords_english(path):
    """Writes the English directions of the robot's path"""

    path_english = []
    for i in range(0, -1 + len(path)):
        r, c = path[i]
        next_r, next_c = path[i+1]
        if c < next_c:
            path_english.append("Right")
        elif r < next_r:
            path_english.append("Down")

    path_english.append("Destination!")
    return path_english


def draw_path_to_board(board, path):
    """Draws the robot's path to the board"""

    if DEST_R == 0 and DEST_C == 0:
        return ["[+]"]

    if path:
        path_english = convert_coords_english(path)

        board[0][0] = "[|]" if path_english[0] == "Down" else "[-]"

        for i in range(1, -1 + len(path)):
            prev_move = path_english[i-1]
            next_move = path_english[i+1]
            cur_move = path_english[i]
            r, c = path[i]

            if prev_move == "Right" and cur_move == "Down":
                board[r][c] = "[{}]".format(chr(119317))
            elif prev_move == "Down" and cur_move == "Right":
                board[r][c] = "[{}]".format(chr(8735))
            elif cur_move == "Right":
                board[r][c] = "[-]"
            elif cur_move == "Down":
                board[r][c] = "[|]"

        board[DEST_R][DEST_C] = "[*]"
    return board


def convert_board_string(board):
    """Returns a string representation of the board."""
    board_string = ""
    for row in board:
        row_string = ""
        for element in row:
            row_string += element
        board_string += row_string + "\n"
    return board_string

def print_introduction():
    print("-" * 15)
    print("Welcome to the Robot Game!")
    print("Your robot starts in the upper left corner")
    print("of the game board, at coordinates (0,0)\n")
    print("She can only move to the RIGHT and DOWN.\n")

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_destination():
    print("\nWhat are the coordinates of your robot's destination?")
    print("Example: 2,2")
    coord = input("> ")
    int_coord = []
    for c in coord:
        if is_int(c) and len(int_coord) < 2:  # Grabs the first two integers
            int_coord.append(c)
    try:
        r, c = int_coord
    except (ValueError, UnboundLocalError):
        print("Sorry. You must enter the destination in the form Row,Column")
        get_destination()

    return (int(r), int(c))


def message():
    print("\nOkay. Right now there are some obstacles...")
    print("Those squares are marked with an X.\n")
    print(BOARD_STRING)
    for x in range(2):
        if x == 0:
            m = "Looking for a path..."
            print(m, end="\r")
            time.sleep(2.5)
        elif PATH:
            m = "Looking for a path...Success!!!"
            m += "\nCheck it out:\n"
            print(m, end="\r")
            print(BOARD_PATH_STRING)
        else:
            m = "Looking for a path...Darn!"
            m += "\nThere doesn't seem to be a path through the obstacles!\n"
            print(m, end="\r")

    if PATH:
        print("\nPress ENTER to see the path's coordinates:")
        display = input()
        print(PATH)
    else:
        print("Such ill-placed obstacles.")

def get_obstacles():
    obstacles = []
    max_obs = (DEST_R + 1) * (DEST_C + 1) - 2
    print("Would you like to add in random obstacles?")
    num_obs = input("Enter a number: ")
    n = 0
    while (n < int(num_obs)):
        r = randint(0, DEST_R)
        c = randint(0, DEST_C)
        if (r == 0 and c == 0) or (r == DEST_R and c == DEST_C):
            n -= 1
            continue
        elif (r, c) not in obstacles:
            obstacles.append((r, c))
        else:
            n -= 1
        n += 1
        if len(obstacles) >= max_obs:
            return obstacles
    return obstacles


print_introduction()
DEST_R, DEST_C = get_destination()
obstacles = get_obstacles()

GAME_BOARD = create_board(DEST_R, DEST_C)
PATH = find_path(DEST_R, DEST_C)
BOARD_STRING = convert_board_string(GAME_BOARD)
BOARD_WITH_PATH = draw_path_to_board(GAME_BOARD, PATH)
BOARD_PATH_STRING = convert_board_string(BOARD_WITH_PATH)
message()
