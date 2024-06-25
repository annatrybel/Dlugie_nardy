# Board.py
import pygame

class Checker:
    pionek1_img = pygame.image.load("images/white.png")
    pionek2_img = pygame.image.load("images/black.png")
    pionek1_img = pygame.transform.scale(pionek1_img, (75, 75))
    pionek2_img = pygame.transform.scale(pionek2_img, (75, 75))

    def __init__(self, color, x, y):
        self.color = color
        self.image = self.pionek1_img if color == 'white' else self.pionek2_img
        self.rect = pygame.Rect(x, y, 75, 75)
        self.previous_position = None

    def update_previous_position(self):
        self.previous_position = (self.rect.x, self.rect.y)


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
        self.pionki1 = [Checker('white', 1055, offset + i * 37) for i in range(15)]
        self.pionki2 = [Checker('black', offset, 680 - i * 37) for i in range(15)]
        self.pionki_wyprowadzone1 = []
        self.pionki_wyprowadzone2 = []
        # Listy do przechowywania prostokątów
        self.top_left = [pygame.Rect(self.offset + i * 80, 60, 75, 100) for i in range(6)]
        self.top_right = [pygame.Rect(650 + i * 80, 60, 75, 100) for i in range(6)]
        self.down_left = [pygame.Rect(self.offset + i * 80, 700 - self.offset, 75, 100) for i in range(6)]
        self.down_right = [pygame.Rect(650 + i * 80, 700 - self.offset, 75, 100) for i in range(6)]

    def draw(self):
        for rect in self.top_left + self.top_right + self.down_left + self.down_right:
            pygame.draw.rect(self.window, (200, 200, 200), rect, 1)

        Checker.draw_checkers(self.window, self.pionki1, self.pionki2)
        Checker.draw_checkers(self.window, self.pionki_wyprowadzone1, self.pionki_wyprowadzone2)

        self.draw_checkers_with_spacing(self.pionki_wyprowadzone1)
        self.draw_checkers_with_spacing(self.pionki_wyprowadzone2)

    def draw_checkers_with_spacing(self, pionki_list):  # Dodanie odstępu między pionkami jeśli pozycja jest już narysowana
        drawn_positions = set()                     # Zbiór do przechowywania już narysowanych pozycji

        for pionek in pionki_list:
            if pionek.rect.topleft in drawn_positions:
                if any(pionek.rect.colliderect(rect) for rect in self.top_left + self.top_right):
                    pionek.rect.y += 20           # Przesunięcie pionka w dół
                elif any(pionek.rect.colliderect(rect) for rect in self.down_left + self.down_right):
                    pionek.rect.y -= 20            # Przesunięcie pionka w górę

            self.window.blit(pionek.image, pionek.rect)
            drawn_positions.add(pionek.rect.topleft)
    
    def remove_from_stack(self, color, pionek):   
        if color == 'white':
            self.pionki_wyprowadzone1.append(pionek)
            self.pionki1.remove(pionek)
        else:
            self.pionki_wyprowadzone2.append(pionek)
            self.pionki2.remove(pionek)


    def is_opponent_checker_on_position(self, current_color, x, y):    # Sprawdza czy na pozycji jest pionek przeciwnika
        target_rect = pygame.Rect(x, y, 75, 75)
        if current_color == "white":
            for pionek in self.pionki_wyprowadzone2:
                if pionek.rect.colliderect(target_rect):
                    return True
        else:
            for pionek in self.pionki_wyprowadzone1:
                if pionek.rect.colliderect(target_rect):
                    return True
        return False  