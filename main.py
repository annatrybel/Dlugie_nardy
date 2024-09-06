import pygame
import sys
from main_panel import Button
from players_panel import addName
from conditions import text

pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Dłudie nardy")

def wrap_text(text, font, max_width):
    lines = []
    current_line = ''
    
    for word in text.split():
        text_line = f"{current_line} {word}".strip()
        text_surface = font.render(text_line, True, (0, 0, 0))
        
        if text_surface.get_width() <= max_width:
            current_line = text_line
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def show_conditions_window(main_window):
    modal_width, modal_height = 900, 600
    modal_x = (main_window.get_width() - modal_width) // 2
    modal_y = (main_window.get_height() - modal_height) // 2
    modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
    
    close_button_size = 30
    close_button_rect = pygame.Rect(modal_x + modal_width - close_button_size, modal_y, close_button_size, close_button_size)

    background = pygame.image.load("images/conditions_background.png")
    background = pygame.transform.scale(background, (modal_width, modal_height))
    
    font = pygame.font.Font(None, 28)
    margin_x = 60
    margin_y = 30
    max_width = modal_width - 2 * margin_x 
    wrapped_text_lines = wrap_text(text, font, max_width)
    
    total_text_height = len(wrapped_text_lines) * (font.get_height() + 15) 
    max_scroll_y = modal_height - total_text_height - 2 * margin_y 
    
    scroll_y = 0
    scroll_speed = 15   
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Przewijanie w górę
                    scroll_y = min(scroll_y + scroll_speed, 0)
                elif event.button == 5: # Przewijanie w dół
                    scroll_y = max(scroll_y - scroll_speed, max_scroll_y)
                elif event.button == 1: # Kliknięcia myszki
                    mouse_pos = pygame.mouse.get_pos()
                    if close_button_rect.collidepoint(mouse_pos):
                        running = False
                    
        main_window.fill((0, 0, 0))        
        pygame.draw.rect(main_window, (255, 255, 255), modal_rect)
        main_window.blit(background, modal_rect.topleft)
        
        
        y_offset = modal_y + margin_y + scroll_y
        for line in wrapped_text_lines:
            text_surface = font.render(line, True, (0, 0, 0))
            if y_offset > modal_y + text_surface.get_height() and y_offset < modal_height + margin_y:
                main_window.blit(text_surface, (modal_x + margin_x, y_offset))
            y_offset += text_surface.get_height() + 10 
                
        
        #krzyżyk do zamykania modalnego okna
        pygame.draw.rect(main_window, (255, 0, 0), close_button_rect)  
        close_text = font.render("X", True, (255, 255, 255))
        main_window.blit(close_text, (close_button_rect.x + 8, close_button_rect.y + 4)) 
        
        pygame.display.update()

def main():
    run = True
    background = pygame.image.load("images/start_background.jpg")
    background = pygame.transform.scale(background, (1200, 800))
    play_button = Button(0, 50, 600, 125, "images/start.png", "images/start2.png")
    conditions_button = Button(0, 200, 600, 125, "images/conditions.png", "images/conditions2.png")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okno
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked():  # rozpoczęcie gry               
                    addName()  
                    run = False
                elif conditions_button.is_clicked():  
                    show_conditions_window(window)
                   
        window.blit(background, (0, 0))
        play_button.draw(window)
        conditions_button.draw(window)
        pygame.display.update()

if __name__ == "__main__":
    main()
