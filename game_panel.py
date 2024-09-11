import time
from board import Board
import pygame
import random
from main_panel import Button
from memory_profiler import profile
import gc


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1250, 900))
        self.board = Board(self.window)
        background = pygame.image.load("images/board.png")
        self.background = pygame.transform.scale(background, (1250, 800))
        self.font = pygame.font.Font(None, 60)
        self.ustawianie_pierwszenstwa = True
        self.dragging = False
        self.selected_pionek = None
        self.offset_x = 0
        self.offset_y = 0
        self.current_color = "black" 
        self.pionek_usuniety = False  # czy pionek został usunięty podczas bieżącego rzutu
        self.expected_move = None

        self.dice_result = 0
        self.random_dice1 = None
        self.random_dice2 = None
        self.first_double_dice1_white = False
        self.first_double_dice1_black = False
        self.double_roll_white = None
        self.double_roll_black = None
        self.double_dice = 0
        self.dice1_used = False  
        self.dice2_used = False       

        pygame.mixer.init()   
        self.dice_roll_sound = pygame.mixer.Sound("images/dice_roll.wav")
    
        self.ustawianie_button = Button(110, 800, 400, 100, "images/ustawienie.png", "images/ustawienie2.png")
        self.rzut_button = Button(110, 800, 400, 100, "images/rzut.png", "images/rzut2.png")
        self.powrot_button = Button(720, 800, 400, 100, "images/powrot.png", "images/powrot2.png")
        self.sound_on = True  
        self.update_sound_button_image()
        

    def update_sound_button_image(self):
        pygame.draw.rect(self.window, (0, 0, 0), (1150, 820, 50, 50))
        if self.sound_on:
            self.sound_button = Button(1150, 820, 50, 50, "images/sound.png", "images/sound.png")           
            pygame.mixer.set_num_channels(8)  #włączenie dźwięku
        else:
            self.sound_button = Button(1150, 820, 50, 50, "images/not_sound.png", "images/not_sound.png")            
            pygame.mixer.set_num_channels(0) 
        self.sound_button.draw(self.window)
        

    def reset_game(self):
        self.board = Board(self.window)
        self.ustawianie_pierwszenstwa = True
        self.current_color = "black" 
        self.pionek_usuniety = False
        self.first_double_dice1_white = False
        self.first_double_dice1_black = False
        self.double_roll_white = None
        self.double_roll_black = None
        self.dice_result = 0
        self.dice1_used = False
        self.dice2_used = False
        self.random_dice1 = None
        self.random_dice2 = None
        self.expected_move = None
        self.double_dice = 0
        self.sound_on = True
        self.dragging = False
        self.selected_pionek = None     
        self.offset_x = 0
        self.offset_y = 0
        
         
    def draw_buttons(self):
        if self.ustawianie_pierwszenstwa:
            self.ustawianie_button.draw(self.window)
        else:
            self.rzut_button.draw(self.window)
        self.powrot_button.draw(self.window)
        

    def resize_window(self, width, height):
        self.window = pygame.display.set_mode((width, height))


    def catch_dice(self):
        return random.randint(1, 6), random.randint(1, 6)
    

    def display_dice_results(self, result1, result2):
        results_area = pygame.Rect(525, 800, 200, 100)  
        font = pygame.font.SysFont("arial", 70)  
        self.window.fill((0, 0, 0), results_area) 

        # Trzykrotna symulacja rzutu kośćmi
        for _ in range(3):  
            temp_result1, temp_result2 = self.catch_dice()     
            text = font.render(f"{temp_result1}  :  {temp_result2}", True, (255, 255, 255))  

            self.window.fill((0, 0, 0), results_area)  
            self.window.blit(text, (results_area.x + 25, results_area.y)) 
            pygame.display.update(results_area)  
            self.dice_roll_sound.play()  
            time.sleep(0.3)  

        self.window.fill((0, 0, 0), results_area) 
        final_result = font.render(f"{result1}  :  {result2}", True, (255, 255, 255))  
        self.window.blit(final_result, (results_area.x + 25, results_area.y))  
        pygame.display.update(results_area)  

            
            
    def first_projection(self):
        # Sprawdzanie, czy to pierwszy rzut dla danego gracza
        if self.current_color == "white":
            if not self.first_double_dice1_white: 
                if self.random_dice1 == self.random_dice2:
                    self.double_roll_white = self.random_dice1
            self.first_double_dice1_white = True  

        elif self.current_color == "black":
            if not self.first_double_dice1_black:  
                if self.random_dice1 == self.random_dice2:     
                    self.double_roll_black = self.random_dice1
            self.first_double_dice1_black = True  


    def obsługa_przycisków(self, name_player1, name_player2):
        def display_text(message, delay=2000):
            text = self.font.render(message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 20))
            self.window.blit(text, text_rect)
            pygame.display.update(text_rect)
            pygame.time.delay(delay)

        if self.ustawianie_button.is_clicked() and self.ustawianie_pierwszenstwa:
            first_dice1, first_dice2 = self.catch_dice()

            if first_dice1 > first_dice2:
                display_text(f"Gracz {name_player1} zaczyna!")
            elif first_dice2 > first_dice1:
                display_text(f"Gracz {name_player2} zaczyna!")
            else:
                display_text("Równa liczba oczek, losowanie jeszcze raz...")
                return
            
            self.ustawianie_pierwszenstwa = False
            
        elif self.rzut_button.is_clicked() and not self.ustawianie_pierwszenstwa:
            self.double_dice = 0                
            
            self.random_dice1, self.random_dice2 = self.catch_dice()
            self.display_dice_results(self.random_dice1, self.random_dice2)
            self.dice_result = self.random_dice1 + self.random_dice2
            if self.random_dice1 == self.random_dice2:
                self.double_dice = 2
                           
            self.dice1_used = False  # Resetowanie zmiennej, odpowiedzialnej za wykorzystanie pierwszego rzutu
            self.dice2_used = False  # Resetowanie zmiennej, odpowiedzialnej za wykorzystanie drugiego rzutu
            
            self.pionek_usuniety = False  # Resetowanie flagi przy nowym rzucie, 1 usunięty pionek na rzut
                                        
            self.current_color = "white" if self.current_color == "black" else "black"  # Zmiana aktualnego koloru gracza

        elif self.powrot_button.is_clicked():
            self.reset_game()
            self.resize_window(1200, 800)
            from main import main  
            main()
            return
        
        elif self.sound_button.is_clicked():
            self.sound_on = not self.sound_on
            self.update_sound_button_image()
                

    def handle_move(self, rect, dice_value):
        if not self.checkers_in_final_position():
            if self.is_move_clockwise(self.selected_pionek.previous_position, (rect.x, rect.y), dice_value):
                if not self.board.is_opponent_checker_on_position(self.current_color, rect.x, rect.y):
                    self.selected_pionek.rect.centerx = rect.centerx
                    if any(self.selected_pionek.rect.colliderect(p) for p in self.board.top_left + self.board.top_right):
                        self.selected_pionek.rect.top = rect.top
                    else:
                        self.selected_pionek.rect.bottom = rect.bottom                                       
                    return True
        else:
            print("remove")
            if self.remove_from_deck(self.current_color, self.selected_pionek.previous_position, (rect.x, rect.y), dice_value):
                self.selected_pionek.rect.centerx = rect.centerx
                self.selected_pionek.rect.top = rect.top
                return True
        return False

    

    def is_move_clockwise(self, original_pos, new_pos, dice_result):
        current_x, current_y = original_pos
        new_x, new_y = new_pos
        
        num_end = None
        num_end2 = None
        
        # Definiowanie prostokątów wokół pozycji
        target_rect_original = pygame.Rect(current_x, current_y, 75, 75)
        target_rect_new = pygame.Rect(new_x, new_y, 75, 75)
      
        def calculate_move(rect1, rect2):
            return abs(rect2.centerx - rect1.centerx) // 80

        top_left_quadrant = (current_x < 600 and current_y < 190)
        top_right_quadrant = (current_x >= 655 and current_y < 550)
        down_left_quadrant = (current_x < 600 and current_y >= 190)
        down_right_quadrant = (current_x >= 655 and current_y >= 550)
        
        if down_left_quadrant:
            if (new_x >= 655 and new_y >= 500):
                self.expected_move = (abs(target_rect_new.centerx - target_rect_original.centerx) - 50)//80 
            elif (new_x < 600 and new_y >= 190):
                if new_x > current_x:
                    self.expected_move = calculate_move(target_rect_original, target_rect_new)
            else:
                return False
            print(self.expected_move)
            return self.expected_move == dice_result
        

        if down_right_quadrant:
            if (new_x >= 655 and new_y < 200):

                if self.current_color == "white":     # Ograniczenie przejście po drugiemu kołu dla białych pionków
                    return False
                num_end = calculate_move(target_rect_original, self.board.down_right[-1])      # Obliczanie liczby pól, o które przesunięto pionek w swoim kwadracie
                num_end2 = calculate_move(target_rect_new, self.board.top_right[-1])       
                self.expected_move = (num_end + num_end2 + 1) 
                
                print(num_end,num_end2,self.expected_move)                
            elif (new_x >= 655 and new_y >= 500):
                if new_x > current_x:
                    self.expected_move = calculate_move(target_rect_original, target_rect_new)
            else:
                return False
            print(self.expected_move)
            return self.expected_move == dice_result

        if top_right_quadrant:
            if (new_x < 600 and new_y < 600):
                self.expected_move = (abs(target_rect_new.centerx - target_rect_original.centerx) - 50)//80
            elif (new_x >= 655 and new_y < 620):
                if new_x < current_x:
                    self.expected_move = calculate_move(target_rect_original, target_rect_new)
                else:
                    return False
            print(self.expected_move)
            return self.expected_move == dice_result
                

        if top_left_quadrant:
            if (new_x < 600 and new_y >= 500):

                if self.current_color == "black":      # Ograniczenie przejście po drugiemu kołu dla czarnych pionków
                    return False                
                
                num_end = calculate_move(target_rect_original, self.board.top_left[0])      # Obliczanie liczby pól, o które przesunięto pionek w swoim kwadracie
                num_end2 = calculate_move(target_rect_new, self.board.down_left[0]) 
                
                self.expected_move = (num_end + num_end2 + 1) 
                print(num_end,num_end2,self.expected_move)
            elif (new_x < 600 and new_y < 190):
                if new_x < current_x:
                    self.expected_move = calculate_move(target_rect_original, target_rect_new)
            else:
                return False
            print(self.expected_move)
            return self.expected_move == dice_result
        
        return False


    def checkers_in_final_position(self):
        if self.current_color == "white":
            wyprowadzone = self.board.pionki_wyprowadzone1 
            for checker in wyprowadzone:
                if not (checker in self.board.down_right):
                    return False
        elif self.current_color == "black":
            wyprowadzone= self.board.pionki_wyprowadzone2
            for checker in wyprowadzone:
                if not (checker in self.board.top_left):
                    return False
        else:
            print("checkers_in_final_position(self)==true")        
            return True


    def remove_from_deck(self, color, original_pos, new_pos, dice_result):
        if color == "white":
            box_position = self.board.box_white
            pionki_wyprowadzone = self.board.pionki_wyprowadzone1
            positions = [
                self.board.down_right[5],
                self.board.down_right[4],
                self.board.down_right[3],
                self.board.down_right[2],
                self.board.down_right[1],
                self.board.down_right[0]
            ]
            print("remove-color-white")
        else:
            box_position = self.board.box_black
            pionki_wyprowadzone = self.board.pionki_wyprowadzone2
            positions = [
                self.board.top_left[5],
                self.board.top_left[4],
                self.board.top_left[3],
                self.board.top_left[2],
                self.board.top_left[1],
                self.board.top_left[0]
            ]
            print("remove-color-black")
        # indeks oryginalnej pozycji pionka
        original_position_index = None
        for idx, position in enumerate(positions):
            if position.centerx == original_pos[0]:
                original_position_index = idx + 1  
                break

        if original_position_index is not None:
            print("original_position_index is not None")
            if (dice_result == original_position_index and new_pos == box_position):
                print("dice_result == original_position_index and new_pos == box_position")
                for checker in pionki_wyprowadzone:
                    if checker.rect.centerx == original_pos[0] and checker.rect.centery == original_pos[1]:
                        pionki_wyprowadzone.remove(checker)
                        break
                return True
            elif self.is_move_clockwise(original_pos, new_pos, dice_result):
                print("self.is_move_clockwise(original_pos, new_pos, dice_result):")
                return True

        return False
    

    @profile
    def start(self, name_player1, name_player2):        
        run = True   
        clock = pygame.time.Clock()
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:                            
                    self.obsługa_przycisków(name_player1, name_player2)
                            
                    if not self.ustawianie_pierwszenstwa and self.dice_result != 0:
                        self.first_projection()
                        mouse_x, mouse_y = event.pos
                        if self.current_color == "white":
                            if self.board.pionki1 and not self.pionek_usuniety:
                                 if self.board.pionki1[-1].rect.collidepoint(mouse_x, mouse_y):
                                    self.board.remove_from_stack(self.current_color, self.board.pionki1[-1])
                                    if self.double_roll_white is not None:
                                        self.board.remove_from_stack(self.current_color, self.board.pionki1[-1])
                                    self.pionek_usuniety = True
                            pionki_wyprowadzone = self.board.pionki_wyprowadzone1
                        else:
                            if self.board.pionki2 and not self.pionek_usuniety:
                                if self.board.pionki2[-1].rect.collidepoint(mouse_x, mouse_y):
                                    self.board.remove_from_stack(self.current_color, self.board.pionki2[-1])
                                    if self.double_roll_black is not None:
                                        self.board.remove_from_stack(self.current_color, self.board.pionki2[-1])
                                    self.pionek_usuniety = True
                            pionki_wyprowadzone = self.board.pionki_wyprowadzone2

                        for pionek in pionki_wyprowadzone:
                            if pionek.rect.collidepoint(mouse_x, mouse_y): 
                                if pionek == self.board.end_on_position(mouse_x, mouse_y, pionki_wyprowadzone):                             
                                    self.dragging = True
                                    self.selected_pionek = pionek
                                    self.offset_x = pionek.rect.x - mouse_x
                                    self.offset_y = pionek.rect.y - mouse_y
                                    self.selected_pionek.update_previous_position()
                                    break
                            
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging and self.selected_pionek:
                        self.dragging = False
                        valid_position = False

                        rects = self.board.top_left + self.board.top_right + self.board.down_left + self.board.down_right

                        def attempt_move(dice, dice_used):
                            if not dice_used:
                                for rect in rects:
                                    if self.selected_pionek.rect.colliderect(rect):
                                        if self.handle_move(rect, dice):
                                            return True
                            return False

                        if not self.dice1_used:
                            if attempt_move(self.random_dice1, self.dice1_used):
                                self.dice1_used = True
                                if self.double_dice > 0:
                                    self.dice1_used = False
                                    self.double_dice -= 1
                                valid_position = True
                        if not valid_position and not self.dice2_used:
                            if attempt_move(self.random_dice2, self.dice2_used):
                                self.dice2_used = True
                                valid_position = True

                        if not valid_position:
                            self.selected_pionek.rect.x, self.selected_pionek.rect.y = self.selected_pionek.previous_position
                        else:
                            self.selected_pionek.update_previous_position()
                            self.expected_move = None
                            self.selected_pionek = None

                        if self.dice1_used and self.dice2_used:
                            self.dice_result = 0 
                                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging and self.selected_pionek:
                        mouse_x, mouse_y = event.pos
                        self.selected_pionek.rect.x = mouse_x + self.offset_x
                        self.selected_pionek.rect.y = mouse_y + self.offset_y
                
                       
            self.window.blit(self.background, (0, 0))
            self.board.draw()
            self.draw_buttons()
            self.update_sound_button_image()
            pygame.display.update()

            clock.tick(60)
            gc.collect()
            


if __name__ == "__main__":
    game = Game()
    game.start()

    

