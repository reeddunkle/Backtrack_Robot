"""
backtrack_OOP.py
-------------
Converting backtrack to OOP:
"""


from random import randint
import os
import time




DOWN = "Down"
RIGHT = "Right"
DESTINATION = "Destination!"
EMPTY_CHAR = "[ ]"
OBSTACLE_CHAR = "[X]"
FAILED = "[$]"
HOME_CHAR = "[+]"
DESTINATION_CHAR = "[*]"
DOWN_CHAR = "[|]"   # From up going down
RIGHT_CHAR = "[-]"  # From left going right
DOWN_RIGHT_CHAR = "[{}]".format(chr(8735))  # From up going right
RIGHT_DOWN_CHAR = "[{}]".format(chr(119317))  # From left going down




# class UserInputValidator(object):






def possible_directions(row, col, obstacles):
    """Returns the moves that are legal from the given coordinates."""

    dirs = []

    obs_coordinates = [(square.row, square.col) for square in obstacles]

    # In case the user sets the robot's destination as (0,0),
    # this adds their destination to the path.
    if row == 0 and col == 0:
        dirs.append((0, 0))

    if col > 0 and (row, col-1) not in obs_coordinates:
        dirs.append((row, col-1))

    if row > 0 and (row-1, col) not in obs_coordinates:
        dirs.append((row-1, col))

    return dirs





class Board(object):

    def __init__(self):
        """Calls _get_user_input()."""

        self.squares = []
        self.rows = -1
        self.cols = -1
        self.dest_r = -1
        self.dest_c = -1
        self.max_obstacles = -1
        self.num_obstacles = -1



    def setup_from_user(self):
        """Gets destination and obstacles from the user."""

        self.dest_r, self.dest_c  = self._get_destination()

        self.rows = self.dest_r + 1     # add 1 to calculate grid size from coordinates
        self.cols = self.dest_c + 1

        self.squares = [[Square(r, c) for c in range(self.cols)] for r in range(self.rows)]

        # We subtract 2 because src and trg are not allowed to have obstacles.
        self.max_obstacles = self.rows * self.cols - 2

        self.num_obstacles = self._get_num_obstacles(self.max_obstacles)
        self._place_obstacles()


    def _get_destination(self):
        """Gets coordinates from the user for the robot's destination."""

        prompt_r = "Which row number is your robot's destination?\n(Starting from 0)\n> "
        prompt_c = "Which column number is your robot's destination?\n(Starting from 0)\n> "
        error_msg = "Sorry. You must enter a number which is less than 32."
        test = lambda s: s.isdigit() and int(s) <= 32

        destination_r = validate_user_input(prompt_r, error_msg, test)
        destination_c = validate_user_input(prompt_c, error_msg, test)
        r_chars = [char for char in destination_r if char.isdigit()]
        c_chars = [char for char in destination_c if char.isdigit()]

        r = int(''.join(r_chars))
        c = int(''.join(c_chars))

        return (r, c)


    def _get_num_obstacles(self, max_obstacles):
        """Get number of obstacles from the user."""

        prompt = "Please enter a number of random obstacles:\n> "
        error_msg = "Sorry, for a board of this size\nyou can only have {} obstacles.".format(max_obstacles)
        test = lambda s: s.isdigit() and int(s) <= max_obstacles

        num_obstacles = validate_user_input(prompt, error_msg, test)
        num_obstacles = int(num_obstacles)

        return num_obstacles


    def _place_obstacles(self):
        """Places obstacles randomly."""

        self.obstacles = []
        current_obstacles = 0
        while (current_obstacles < self.num_obstacles):
            r = randint(0, self.dest_r)
            c = randint(0, self.dest_c)

            # Avoid placing obstacles in src and trg
            if (r == 0 and c == 0) or (r == self.dest_r and c == self.dest_c):
                continue

            elif self.squares[r][c].obstacle:
                continue

            else:

                self.squares[r][c].obstacle = True
                self.obstacles.append(self.squares[r][c])
                current_obstacles += 1


    def memoize(self, cur_row, cur_col):
        """Caches squares that prove to not lead anywhere to avoid re-visiting them."""

        self.squares[cur_row][cur_col].failed = True
        self.squares[cur_row][cur_col].face = FAILED  # Shouldn't have set face here
        self.obstacles.append(self.squares[cur_row][cur_col])


    def find_path(self):
        """Finds path from (0,0) to (self.dest_r, self.dest_c)"""
        return self._find_path(self.dest_r, self.dest_c)


    def _find_path(self, cur_row, cur_col):
        """The backtrack algorithm -- returns the robot's path."""

        # This ensures that the function returns the complete path even in this base case
        if (self.dest_r == 0 and self.dest_c == 1) or (self.dest_r == 1 and self.dest_c == 0):
            return [(0, 0), (self.dest_r, self.dest_c)]

        else:
            possible_dirs = possible_directions(cur_row, cur_col, self.obstacles)

            # Memoization to cache previously failed coordinates
            if len(possible_dirs) == 0:
                self.memoize(cur_row, cur_col)

            for coordinance in possible_dirs:
                r, c = coordinance

                if r == 0 and c == 0:
                    return [(0, 0)]

                solution = self._find_path(r, c)
                if solution:
                    final = solution + [(r, c)]
                    if cur_row == self.dest_r and cur_col == self.dest_c:
                        final += [(cur_row, cur_col)]

                    return final

                else:
                    possible_dirs = possible_directions(r, c, self.obstacles)

                    if len(possible_dirs) == 0:
                        # self.memoize(r, c)
                        self.squares[cur_row][cur_col].failed = True
                        self.squares[cur_row][cur_col].face = "[^]"
                        self.obstacles.append(self.squares[cur_row][cur_col])


    def _coords_to_english(self, path):
        """Writes the English directions of the robot's path."""

        path_english = []
        for i in range(0, -1 + len(path)):
            r, c = path[i]
            next_r, next_c = path[i+1]
            if c < next_c:
                path_english.append(RIGHT)
            elif r < next_r:
                path_english.append(DOWN)

        path_english.append(DESTINATION)

        return path_english


    def assign_path(self, path):
        """
        Tells the Squares with coordinates in <path> that there's a path going
        through them.
        """

        # Edge case where destination is the same as starting pos
        if self.dest_r == 0 and self.dest_c == 0:
            self.squares[0][0].face = HOME_CHAR

        if path:

            if path[1] == (0, 1):
                self.squares[0][0].face = RIGHT_CHAR
            else:
                self.squares[0][0].face = DOWN_CHAR


            path_english = self._coords_to_english(path)


            for i in range(1, len(path) - 1):
                prev_move = path_english[i-1]
                next_move = path_english[i+1]
                cur_move = path_english[i]
                r, c = path[i]

                if prev_move == RIGHT and cur_move == DOWN:
                    move = RIGHT_DOWN_CHAR
                elif prev_move == DOWN and cur_move == RIGHT:
                    move = DOWN_RIGHT_CHAR
                elif cur_move == RIGHT:
                    move = RIGHT_CHAR
                elif cur_move == DOWN:
                    move = DOWN_CHAR

                self.squares[r][c].face = move

            self.squares[self.dest_r][self.dest_c] = DESTINATION_CHAR


    def display(self):
        """Prints self.__str__()."""
        print(self.__str__())


    def __str__(self):
        """Returns a string representation of the board."""

        board_string = ""
        for square_row in self.squares:
            row_string = "".join([s.__str__() for s in square_row])
            board_string += row_string + "\n"

        return board_string



class Square(object):

    def __init__(self, row, col):
        self.obstacle = False
        self.failed = False
        self.row = row
        self.col = col
        self._face = ""

    def __str__(self):
        """String representation of a Square."""

        return self.face

    @property
    def face(self):
        """A property to compute the face value based on self.obstacle."""

        if self._face == "":

            if self.obstacle:
                self._face = OBSTACLE_CHAR
            elif self.failed:
                self._face = FAILED
            else:
                self._face = EMPTY_CHAR

        return self._face

    @face.setter
    def face(self, new_face):

        if not self.obstacle:
            self._face = new_face

        else:
            raise ValueError("A path may not go through an obstacle.")


def print_introduction():
    """Prints the game's introduction messages."""

    print("-" * 15)
    print("Welcome to the Robot Game!")
    print("Your robot starts in the upper left corner")
    print("of the game board, at coordinates (0,0)\n")
    print("She can only move to the RIGHT and DOWN.\n")


def validate_user_input(prompt, error_msg, test):
    """
    Keeps prompting the user for a valid input. <test> is a function that returns
    a Boolean value, depending on whether or not the input is valid.
    """

    user_input = input(prompt)

    while not test(user_input):
        if not test(user_input):
            print(error_msg)

        user_input = input(prompt)

    return user_input


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_final_message(path):

    if path:

        print("Looking for a path...Success!")
        print("Check it out.")
    else:

        print("Looking for a path...Darn!")
        print("Such ill placed obstacles.")


if __name__ == '__main__':

    clear_screen()
    print_introduction()
    board = Board()
    board.setup_from_user()

    clear_screen()
    board.display()

    print("Looking for a path...")
    path = board.find_path()

    board.assign_path(path)

    time.sleep(1.5)
    clear_screen()
    board.display()
    print_final_message(path)

