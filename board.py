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
        self.previous_position = (x, y)

    def update_previous_position(self):
        self.previous_position = (self.rect.x, self.rect.y)


    @staticmethod
    def draw_checkers(window, pionki1, pionki2):
        for pionek in pionki1:
            window.blit(Checker.pionek1_img, pionek.rect.topleft)
        for pionek in pionki2:
            window.blit(Checker.pionek2_img, pionek.rect.topleft)


class NumberedRect(pygame.Rect):
    def __init__(self, left, top, width, height, position_number):
        super().__init__(left, top, width, height)
        self.position_number = position_number

class Board:
    def __init__(self, window, offset=35):
        self.window = window
        self.offset = offset
        self.pionki1 = [Checker('white', 1055, self.offset + i * 36) for i in range(15)]
        self.pionki2 = [Checker('black', 120, 700 - i * 36) for i in range(15)]
        self.pionki_wyprowadzone1 = []
        self.pionki_wyprowadzone2 = []
        
        
         # Listy do przechowywania prostokątów z numerami pozycji
        self.top_right = [NumberedRect(655 + i * 80, self.offset, 75, 150, 7 - 1) for i in range(6)]
        self.top_left = [NumberedRect(120 + i * 80, self.offset, 75, 150, 13 - 1) for i in range(6)]        
        self.down_left = [NumberedRect(120 + i * 80, 620, 75, 150, i + 13) for i in range(6)]
        self.down_right = [NumberedRect(655 + i * 80, 620, 75, 150, i + 19) for i in range(6)]

        self.box_white =pygame.Rect(1160,self.offset, 75, 400)
        self.box_black =pygame.Rect(15,self.offset, 75, 400)

        

    def draw(self):
        for rect in self.top_left + self.top_right + self.down_left + self.down_right:
            pygame.draw.rect(self.window, (200, 200, 200), rect, 1)

        pygame.draw.rect(self.window, (200, 200, 200), self.box_white, 1)
        pygame.draw.rect(self.window, (200, 200, 200), self.box_black, 1)

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
        opponent_checkers = self.pionki_wyprowadzone2 if current_color == "white" else self.pionki_wyprowadzone1
        for checker in opponent_checkers:
            if checker.rect.colliderect(target_rect):
                return True        
        return False  
    

    def end_on_position(self, x, y, pionki_wyprowadzone):   # Zwraca pionek, który jest ostatni na danej pozycji
        target_rect = pygame.Rect(x, y, 75, 75)
        last_checker = None

        for checker in pionki_wyprowadzone:
            if checker.rect.colliderect(target_rect):
                if last_checker is None:
                    last_checker = checker
                else:
                    if ((any(target_rect.colliderect(rect) for rect in self.top_left + self.top_right) and checker.rect.centery > last_checker.rect.centery)
                        or (any(target_rect.colliderect(rect) for rect in self.down_left + self.down_right) and checker.rect.centery < last_checker.rect.centery)):
                        last_checker = checker

        return last_checker


        
