import pygame

class Button:
    def __init__(self, x, y, width, height, image_path, hover_image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.button_image = pygame.image.load(image_path)
        self.button_image = pygame.transform.scale(self.button_image, (width, height))
        self.hover_button_image = pygame.image.load(hover_image_path)
        self.hover_button_image = pygame.transform.scale(self.hover_button_image, (width, height))
        
    def is_clicked(self):                                                #sprawdza czy myszka jest nad przyciskiem
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

            
    def draw(self, window):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Środek powiększonego przycisku powinien być taki sam jak oryginalnego
            hover_rect = self.hover_button_image.get_rect(center=self.rect.center)
            window.blit(self.hover_button_image, self.rect.topleft)
        else:
            window.blit(self.button_image, self.rect.topleft)

