import sys
import time
from game_panel import *
import pygame.font



def addName():
    window = pygame.display.set_mode((1200, 800))
    textInput = TextInput(700, 150, 300, 50, max_length=10)
    textInput2 = TextInput(700, 300, 300, 50, max_length=10)
    next_button = Button(550, 500, 600, 125, "images/next.png", "images/next2.png")
    background = pygame.image.load("images/player_background.jpg")
    background = pygame.transform.scale(background, (1200, 800))
    

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

        content_player1 = textInput.click(events, textInput, textInput2)
        content_player2 = textInput2.click(events, textInput, textInput2)

    
        if next_button.is_clicked():
            game = Game()
            game.start(content_player1, content_player2)
            run = False

        
        window.blit(background, (0, 0))
        next_button.draw(window)      
        textInput.draw(window)
        textInput2.draw(window)
        pygame.display.flip()


if __name__ == "__main__":
    addName()


class TextInput:
    def __init__(self, x, y, width, height, max_length=-1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("red")
        self.font = pygame.font.Font(None, 32)
        self.text = ""
        self.placeholder = "Wprowadź imię"
        self.max_length = max_length
        self.active = False        
        self.cursor = pygame.rect.Rect(self.rect.x + 5, self.rect.y + 5, 1, self.rect.height - 10)
        self.cursor_active = False
        self.last_cursor_toggle = time.time()
        self.cursor_visible = True
    
    def click(self,events, textInput, textInput2):
        for event in events:
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_TAB:
                # Jeśli textInput jest aktywny, przełącz na textInput2
                    if textInput.active:
                        textInput.active = False
                        textInput2.active = True
                elif len(self.text) < self.max_length or self.max_length == -1:
                        self.text += event.unicode
                        

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True                    
                else:
                    self.active = False

        return self.text
                 

       
                
    def draw(self, window):
        # Rysowanie tła pola tekstowego
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        # Rysowanie czerwonej ramki wokół pola tekstowego
        pygame.draw.rect(window, (101, 67, 33), self.rect, 3)
        if self.text:
            font_image = pygame.font.Font(None, 32).render(self.text, True, self.color)
            window.blit(font_image, (self.rect.x + 10, self.rect.y + 15))
            # Aktualizacja pozycji kursora
            text_width, _ = font_image.get_size()
            self.cursor.topleft = (self.rect.x + 10 + text_width, self.rect.y + 10)
        else:
            font_image = pygame.font.Font(None, 28).render(self.placeholder, True, "grey")
            window.blit(font_image, (self.rect.x + 10, self.rect.y + 15))

        # Logika migania kursora
        if self.active and self.cursor_visible:
            pygame.draw.rect(window, "black", self.cursor)
        
        # Aktualizacja widoczności kursora
        if time.time() - self.last_cursor_toggle > 0.5:  # Co 0.5 sekundy
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = time.time()