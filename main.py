import pygame
import sys
from main_panel import Button
from players_panel import addName

pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Dłudie nardy")



def main():
    run = True
    background = pygame.image.load("images/start_background.jpg")
    background = pygame.transform.scale(background, (1200, 800))
    play_button = Button(0, 50, 600, 125, "images/start.png", "images/start2.png")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okno
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked():  # rozpoczęcie gry               
                    addName()  # Przejście do panelu dodawania nazw graczy
                    run = False

        window.blit(background, (0, 0))
        play_button.draw(window)
        pygame.display.update()

    
if __name__ == "__main__":
    main()

