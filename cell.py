import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        width = self.screen.get_width() // 9
        height = self.screen.get_height() // 9

        x = self.col * width
        y = self.row * height

        font = pygame.font.Font(None, 40)
        sketch_font = pygame.font.Font(None, 25)

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
            self.screen.blit(text, text_rect)

        elif self.sketched_value != 0:
            text = sketch_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height), 3)