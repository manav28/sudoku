import pygame
import time
from sudoku_solver import is_valid, solve
from math import sqrt

class SolveButton:
    """Button to solve the puzzle

    Attributes:
        clicked: A boolean indicating whether the button was clicked
    """
    def __init__(self):
        self.clicked = False

    def draw(self, window, board):
        """Draws the button

        Args:
            window: The main window instance
            board: A 2D array containing the current contents of the board

        Returns:
            A 2D array containing the solved board if the button is clicked
            Else it returns None
        """
        if self.clicked:
            pygame.draw.rect(window, (218, 132, 245), ((540/2)-40, 560, 80, 30))
            solve(board)
            return board
        else:
            pygame.draw.rect(window, (143, 220, 249), ((540/2)-40, 560, 80, 30))

        font = pygame.font.SysFont("verdana", 20)
        text = font.render("Solve", 1, (0, 0, 0))
        window.blit(text, ((540/2)-40+13, 565))
        return None

class Cell:
    """An instance of a cell inside the grid

    Attributes:
        value: An integer denoting the value inside the cell
        row: An integer denoting the row in the 2D grid
        col: An integer denoting the column in the 2D grid
        temp: An integer denoting the temporary value inside the cell
        spacing: A float denoting the size of the cell
        selected: A boolean indicating whether the cell is selected
    """
    def __init__(self, value, row, col, spacing):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.spacing = spacing
        self.selected = False

    def draw(self, window):
        """Draws a cell

        Args:
            window: The main window instance

        Returns:
            None
        """
        font = pygame.font.SysFont("comicsans", 40)

        spacing = self.spacing
        x = self.col * spacing
        y = self.row * spacing

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            window.blit(text, (x+5, y+5))
        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (spacing / 2 - text.get_width() / 2),
                               y + (spacing / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(window, (251, 207, 207), (x, y, spacing, spacing), 3)

    def set_value(self, val):
        """Sets the value in the cell"""
        self.value = val

    def set_temp(self, val):
        """Sets a temporary value that is colored gray in the cell"""
        self.temp = val

class Grid:
    """An instance of the puzzle grid
    
    Attributes:
        board: A 2D array representing the current state of the puzzle
        rows: An integer denoting the number of rows in the puzzle
        cols: An integer denoting the number of columns in the puzzle
        width: An integer denoting the width of the grid instance
        height: An integer denoting the height of the grid instance
        subgrid_size: An integer denoting the size of the sub grid
        spacing: A float denoting the spacing of the cells
        cells: A 2D array of cell instances
        solve_button: An instance of the solve button
        model: A copy of the 2D array with the instances of the cells
        selected_cell: A tuple containing the row and column of the selected cell
    """

    def __init__(self, board, width, height):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.width = width
        self.height = height
        self.subgrid_size = sqrt(self.rows)
        self.spacing = self.width / self.rows
        self.cells = [[Cell(self.board[i][j], i, j, self.spacing)
                       for j in range(self.cols)] for i in range(self.rows)]
        self.solve_button = SolveButton()
        self.model = None
        self.selected_cell = None

    def update_model(self):
        """Updates the model"""

        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place_value(self, val):
        """Places the value inside the cell

        Args:
            val: An integer representing the value to be placed

        Returns:
            A boolean indicating whether the placement was valid and successful
        """

        row, col = self.selected_cell
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_value(val)
            self.update_model()
            print(is_valid(self.model, val, (row, col)))
            if is_valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp(0)
                self.update_model()
                return False

    def place_temp_value(self, val):
        """Sets a temporary value displayed in gray at the selected cell
        """
        row, col = self.selected_cell
        self.cells[row][col].set_temp(val)

    def draw(self, window):
        """Draws the gridlines and cells of the puzzle with initial values

        Args:
            window: An instance of the main window of the puzzle

        Returns:
            None
        """
        spacing = self.spacing
        for i in range(self.rows+1):
            if i % self.subgrid_size == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(window, (0, 0, 0), (0, i*spacing), (self.width, i*spacing), thickness)
            pygame.draw.line(window, (0, 0, 0), (i*spacing, 0), (i*spacing, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(window)

        solved_board = self.solve_button.draw(window, self.board)
        if solved_board:
            self.board = solved_board
            for i in range(self.rows):
                for j in range(self.cols):
                    self.cells[i][j].value = self.board[i][j]

    def select_cell(self, row, col):
        """Sets the position of the selected cell

        Args:
            row: An integer denoting the row
            col: An integer denoting the column

        Returns:
            None
        """

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def clear_temp_val(self):
        """Clears the entered temporary text
        """

        row, col = self.selected_cell
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def click(self, pos):
        """Detects the object that got clicked

        Args:
            pos: A tuple containing the x and y coordinates of the click event

        Returns:
            A tuple contatining the position of the cell in the entity was cell
            None otherwise
        """
        if (540/2)-40 < pos[0] < (540/2)+40 and 560 < pos[1] < 560 + 30:
            self.solve_button.clicked = True
        elif pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        """Checks whether the puzzle is solved
        """

        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True

def format_time(current_time):
    """Formats the time for display

    Args:
        time: An integer denoting the number of seconds since the start of the game

    Returns:
        A string that has the formatted time
    """
    seconds = current_time % 60
    minutes = seconds // 60

    return " " + str(minutes) + ":" + str(seconds)

def redraw_window(window, board, current_time, strikes):
    """Refreshes the window

    Args:
        window: The main window instance
        board: A 2D representing the current state of the board
        curent_time: An integer denoting the time elapsed
        strikes: An integer denoting the number of wrong attempts

    Returns:
        None
    """
    window.fill((63, 63, 191))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time: " + format_time(current_time), 1, (0, 0, 0))
    window.blit(text, (540-160, 560))
    text = font.render("X " * strikes, 1, (250, 0, 0))
    window.blit(text, (20, 560))
    board.draw(window)

def main():
    """The main game loop"""

    pygame.font.init()
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")

    board_init = [
        [3, 0, 0, 0, 0, 0, 7, 0, 5],
        [7, 0, 0, 0, 4, 0, 2, 8, 0],
        [2, 0, 8, 9, 0, 7, 0, 0, 0],
        [1, 3, 0, 0, 9, 4, 0, 2, 0],
        [6, 0, 0, 2, 0, 1, 0, 0, 7],
        [0, 5, 0, 7, 3, 0, 0, 4, 1],
        [0, 0, 0, 8, 0, 9, 3, 0, 4],
        [0, 8, 6, 0, 7, 0, 0, 0, 9],
        [9, 0, 3, 0, 0, 0, 0, 0, 2]
    ]

    board = Grid(board_init, 540, 540)
    key = None
    key_bindings = {pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4, pygame.K_5:5,
                    pygame.K_6:6, pygame.K_7:7, pygame.K_8:8, pygame.K_9:9}
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key in key_bindings:
                    key = key_bindings[event.key]

                if event.key == pygame.K_DELETE:
                    board.clear_temp_val()
                    key = None

                if event.key == pygame.K_RETURN:
                    i, j = board.selected_cell

                    if board.cells[i][j].temp != 0:
                        if board.place_value(board.cells[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game Over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select_cell(clicked[0], clicked[1])
                    key = None

            if event.type == pygame.MOUSEBUTTONUP:
                board.solve_button.clicked = False

        if strikes == 3:
            print("Game Over")
            run = False

        if board.selected_cell and key is not None:
            board.place_temp_value(key)

        redraw_window(window, board, play_time, strikes)
        pygame.display.update()

GAME_EXIT = False
while not GAME_EXIT:
    GAME_EXIT = main()
pygame.quit()
            