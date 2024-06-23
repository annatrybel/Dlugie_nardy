# Board.py
import pygame

class Checker:
    pionek1_img = pygame.image.load("images/white.png")
    pionek2_img = pygame.image.load("images/black.png")
    pionek1_img = pygame.transform.scale(pionek1_img, (75, 75))
    pionek2_img = pygame.transform.scale(pionek2_img, (75, 75))

    def __init__(self, color, x, y):
        self.image = self.pionek1_img if color == 'white' else self.pionek2_img
        self.rect = pygame.Rect(x, y, 75, 75)

    @staticmethod
    def draw_checkers(window, pionki1, pionki2):
        for pionek in pionki1:
            window.blit(Checker.pionek1_img, pionek.rect.topleft)
        for pionek in pionki2:
            window.blit(Checker.pionek2_img, pionek.rect.topleft)

class Board:
    def __init__(self, window, offset=60):
        self.window = window
        self.offset = offset
        self.pionki1 = [Checker('white', 1055, offset + i * 40) for i in range(15)]
        self.pionki2 = [Checker('black', offset, 680 - i * 40) for i in range(15)]
        self.pionki_wyprowadzone1 = []
        self.pionki_wyprowadzone2 = []

    def draw(self):
        for i in range(6):
            pygame.draw.rect(self.window, (200, 200, 200), (self.offset + i * 80, 60, 75, 100), 1)
            pygame.draw.rect(self.window, (200, 200, 200), (650 + i * 80, 60, 75, 100), 1)
            pygame.draw.rect(self.window, (200, 200, 200), (self.offset + i * 80, 700 - self.offset, 75, 100), 1)
            pygame.draw.rect(self.window, (200, 200, 200), (650 + i * 80, 700 - self.offset, 75, 100), 1)
        Checker.draw_checkers(self.window, self.pionki1, self.pionki2)
        Checker.draw_checkers(self.window, self.pionki_wyprowadzone1, self.pionki_wyprowadzone2)
    
    def remove_from_stack(self, color, pionek):
        if color == 'white':
            self.pionki_wyprowadzone1.append(pionek)
            self.pionki1.remove(pionek)
        else:
            self.pionki_wyprowadzone2.append(pionek)
            self.pionki2.remove(pionek)
            