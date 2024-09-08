import pygame
from conditions import text  
import sys

class Button:
    def __init__(self, x, y, width, height, image_path, hover_image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.button_image = pygame.image.load(image_path)
        self.button_image = pygame.transform.scale(self.button_image, (width, height))
        self.hover_button_image = pygame.image.load(hover_image_path)
        self.hover_button_image = pygame.transform.scale(self.hover_button_image, (width, height))
        self.click_sound = pygame.mixer.Sound("images/click.wav")
        
    def is_clicked(self):                                                #sprawdza czy myszka jest nad przyciskiem
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.click_sound.play()
                return True
        return False

            
    def draw(self, window):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hover_button_image, self.rect.topleft)
        else:
            window.blit(self.button_image, self.rect.topleft)


class Scrollbar:
    def __init__(self, x, y, width, height, content_height, window_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.content_height = content_height
        self.window_height = window_height
        self.scroll_y = 0
        self.dragging = False
        self.scrollbar_height = max(height * (window_height / content_height), 20)
        self.scrollbar_rect = pygame.Rect(x, y, width, self.scrollbar_height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.scrollbar_rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_y_offset = event.pos[1] - self.scrollbar_rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_y = event.pos[1] - self.mouse_y_offset
                self.scrollbar_rect.y = max(self.rect.y, min(new_y, self.rect.y + self.rect.height - self.scrollbar_height))
                self.scroll_y = (self.scrollbar_rect.y - self.rect.y) * (self.content_height - self.window_height) / (self.rect.height - self.scrollbar_height)

    def draw(self, window):
        pygame.draw.rect(window, (200, 200, 200), self.rect)
        pygame.draw.rect(window, (100, 100, 100), self.scrollbar_rect)

    def get_scroll_offset(self):
        return self.scroll_y

class Condition_button:          
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
        wrapped_text_lines = Condition_button.wrap_text(text, font, max_width)
        
        total_text_height = len(wrapped_text_lines) * (font.get_height() + 15) 
                
        scrollbar = Scrollbar(modal_x + modal_width - 20, modal_y + close_button_size, 20, modal_height - close_button_size, total_text_height, modal_height)   
        target_scroll_y = 0         
        scrolling_factor = 0.05
          
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
                    if event.button == 4:  # Przewijanie w górę
                        target_scroll_y = min(target_scroll_y, 0)
                    elif event.button == 5:  # Przewijanie w dół
                        target_scroll_y = max(target_scroll_y, scrollbar.content_height - scrollbar.window_height )
                    elif event.button == 1:  # Kliknięcia myszki
                        mouse_pos = pygame.mouse.get_pos()
                        if close_button_rect.collidepoint(mouse_pos):
                            running = False

                    scrollbar.scroll_y += (target_scroll_y - scrollbar.scroll_y) * scrolling_factor
                    scrollbar.scrollbar_rect.y = scrollbar.rect.y + (scrollbar.scroll_y * (scrollbar.rect.height - scrollbar.scrollbar_height) / (scrollbar.content_height - scrollbar.window_height))
                    
                scrollbar.handle_event(event)        
                        
            main_window.fill((0, 0, 0))        
            pygame.draw.rect(main_window, (255, 255, 255), modal_rect)
            main_window.blit(background, modal_rect.topleft)
            
            scroll_y_with_scrollbar = scrollbar.get_scroll_offset()
            y_offset = modal_y + margin_y - scroll_y_with_scrollbar
            for line in wrapped_text_lines:
                text_surface = font.render(line, True, (0, 0, 0))
                if y_offset > modal_y + text_surface.get_height() and y_offset < modal_height + margin_y:
                    main_window.blit(text_surface, (modal_x + margin_x, y_offset))
                y_offset += text_surface.get_height() + 10 
                    
            
            #krzyżyk do zamykania modalnego okna
            pygame.draw.rect(main_window, (255, 0, 0), close_button_rect)  
            close_text = font.render("X", True, (255, 255, 255))
            main_window.blit(close_text, (close_button_rect.x + 8, close_button_rect.y + 4)) 
            scrollbar.draw(main_window)
            pygame.display.update()

