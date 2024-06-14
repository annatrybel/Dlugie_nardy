import pygame
import sys

window = pygame.display.set_mode((1200, 800))


class Button:
    def __init__(self, x, y):
        self.x_cord = x
        self.y_cord = y
        self.button_image = pygame.image.load("start.png")
        self.hover_button_image = pygame.image.load("start2.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())

    def tick(self):                                                #sprawdza czy myszka jest nad przyciskiem
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):       #współrzędne myszki
            if pygame.mouse.get_pressed()[0]:
                return True
            
    def draw(self,window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hover_button_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image, (self.x_cord, self.y_cord))


# Ładowanie obrazów pionków
pionek1_img = pygame.image.load("biale.png")
pionek2_img = pygame.image.load("czarne.png")
pionek1_img = pygame.transform.scale(pionek1_img, (75, 75))
pionek2_img = pygame.transform.scale(pionek2_img, (75, 75))


# Ustawienia pionków
offset = 60  # Odstęp od krawędzi planszy


# Pionki gracza 1 (umieszczone w prawej części planszy)
pionki1 = [pygame.Rect(1075, offset + i * 75, 75, 75) for i in range(6)]

# Pionki gracza 2 (umieszczone w lewej części planszy)
pionki2 = [pygame.Rect(offset, 700 - i * 75, 75, 75) for i in range(6)]


# Funkcja do rysowania planszy
def rysuj_plansze():
    for i in range(6):
        pygame.draw.rect(window, (200, 200, 200), (offset + i * 80, 60, 75, 100), 1)
        pygame.draw.rect(window, (200, 200, 200), (650 + i * 80, 60, 75, 100), 1)

        pygame.draw.rect(window, (200, 200, 200), (offset + i * 80, 700-offset, 75, 100), 1)
        pygame.draw.rect(window, (200, 200, 200), (650 + i * 80, 700-offset, 75, 100), 1)


# Funkcja do rysowania pionków
def rysuj_pionki():
    for pionek in pionki1:
        window.blit(pionek1_img, pionek.topleft)
    for pionek in pionki2:
        window.blit(pionek2_img, pionek.topleft)