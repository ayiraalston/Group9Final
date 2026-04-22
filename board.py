# board.py
import pygame

from sudoku import draw_button


# ---------- START SCREEN ----------

# The start_screen(win) function MUST be called in sudoku [dot] py.
# See the following implementation:

# In sudoku.py ...
# from board import Board
# difficulty = start_screen(win)
 ####################### Call start_screen(win) function.
# board_data = generate_sudoku(9, removed_cells)
# board = Board(540, 540, win, difficulty, board_data) 
# Call Board class from board [dot] py
# while True:
#   board.draw()
#   pygame.display.update()

def start_screen(win):
    import sys
    pygame.font.init()

    font=pygame.font.SysFont("comicsans", 60)
    button_font=pygame.font.SysFont("comicsans", 30)

    # Buttons for the difficulty levels on the start screen

    easy_rect=pygame.Rect(170,220,200,60)
    medium_rect=pygame.Rect(170,300,200,60)
    hard_rect=pygame.Rect(170,380,200,60)

    while True:
        win.fill((255,255,255)) #Background color

        # The title

        title=font.render("Sudoku Game", True, (0,0,0))
        win.blit(title, (180, 100))

        # Button design

        draw_button(win, "Easy", easy_rect, button_font)
        draw_button(win, "Medium", medium_rect, button_font)
        draw_button(win, "Hard", hard_rect, button_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=event.pos
                if easy_rect.collidepoint(mouse_pos):
                    return "easy"
                if medium_rect.collidepoint(mouse_pos):
                    return "medium"
                if hard_rect.collidepoint(mouse_pos):
                    return "hard"

# ---------- THE BOARD ----------

# The Cell class helps with interaction:
# value storage and placement, sketch, and position.

class Cell:
    def __init__(self, value, row, col, screen):
        self.value=value
        self.row=row
        self.col=col
        self.screen=screen
        self.sketched_value=0
        self.selected=False

    def set_cell_value(self, value):
        self.value=value

    def set_sketched_value(self, value):
        self.sketched_value=value

    def draw(self):
        gap=540//9
        x=self.col*gap
        y=self.row*gap

        font=pygame.font.SysFont("comicsans", 40)
        small_font=pygame.font.SysFont("comicsans", 20)

        if self.value!=0:
            text=font.render(str(self.value), True, (0,0,0))
            self.screen.blit(text, (x+20, y+15))
        elif self.sketched_value!=0:
            text = small_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(self.screen, (255,0,0), (x, y, gap, gap), 3)

# The Board class:
# Contains 81 cell objects and handles user interaction.

class Board:
    def __init__(self, width, height, screen, difficulty, board):
        self.width=width
        self.height=height
        self.screen=screen
        self.difficulty=difficulty
        self.cells=[[Cell(board[i][j],i,j,screen) for j in range(9)] for i in range(9)]
        self.selected=None
        self.original=[[board[i][j] for j in range(9)] for i in range(9)]

    # Added function reset_to_original for sudoku[dot]py button 'Reset.'

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].value=self.original[i][j]
                self.cells[i][j].sketched_value=0

    def draw(self):
        gap=self.width//9

        for i in range(10):
            thickness=4 if i%3==0 else 1
            pygame.draw.line(self.screen, (0,0,0), (0, i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(self.screen, (0,0,0), (i*gap, 0), (i*gap, self.height), thickness)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected:
            self.cells[self.selected[0]][self.selected[1]].selected=False
        self.selected=(row,col)
        self.cells[row][col].selected=True

    def click(self, x, y):
        gap=self.width//9
        if x<self.width and y<self.height:
            return (y//gap, x//gap)
        return None

    def clear(self):
        if self.selected is None:
            return
        row, col=self.selected
        self.cells[row][col].set_cell_value(0)
        self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected is None:
            return
        row, col=self.selected
        self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected is None:
            return
        row, col=self.selected
        self.cells[row][col].set_cell_value(value)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value==0:
                    return False
        return True
