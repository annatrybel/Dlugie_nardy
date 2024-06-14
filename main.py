import pygame
import sys
from game import *

pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Dłudie nardy")

# Ładowanie tła
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (1200, 800))

# Pętla gry
def start():
    run = True
    dragging = False
    selected_pionek = None
    offset_x = 0
    offset_y = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okno
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:    # jeśli gracz kliknie myszką
                mouse_x, mouse_y = event.pos
                for pionek in pionki1 + pionki2:
                    if pionek.collidepoint(mouse_x, mouse_y):
                        dragging = True
                        selected_pionek = pionek
                        offset_x = pionek.x - mouse_x
                        offset_y = pionek.y - mouse_y
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                selected_pionek = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and selected_pionek:
                    mouse_x, mouse_y = event.pos
                    selected_pionek.x = mouse_x + offset_x
                    selected_pionek.y = mouse_y + offset_y
        window.blit(background, (0, 0))  # Rysowanie tła
        rysuj_plansze()
        rysuj_pionki()
        pygame.display.update()


def main():
    run = True
    background = pygame.image.load("start_background.jpg")
    background = pygame.transform.scale(background, (1200, 800))
    play_button = Button(0, 50)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okno
                run = False

        if play_button.tick():                                                  #rozpoczęcie gry
            start()


        window.blit(background, (0, 0))
        play_button.draw(window)
        pygame.display.update()
    

if __name__ == "__main__":
    main()

pygame.quit()
sys.exit()