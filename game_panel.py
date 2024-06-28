# main.py
import math
from board import Checker, Board
import pygame
import random
from main_panel import Button


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1200, 900))
        self.board = Board(self.window)
        self.font = pygame.font.Font(None, 60)
        self.ustawianie_pierwszenstwa = True
        self.dragging = False
        self.selected_pionek = None
        self.offset_x = 0
        self.offset_y = 0
        self.dice_result = 0
        self.current_color = "black" 
        self.pionek_usuniety = False  # Flaga do śledzenia, czy pionek został usunięty podczas bieżącego rzutu
        self.double_dice_white = False
        self.double_dice_black = False
        self.double_roll_white = None
        self.double_roll_black = None

        self.dice1_used = False  
        self.dice2_used = False  
        
        self.random_dice1 = None
        self.random_dice2 = None


        self.expected_move = None
    
        self.ustawianie_button = Button(50, 800, 400, 100, "images/ustawienie.png", "images/ustawienie2.png")
        self.rzut_button = Button(50, 800, 400, 100, "images/rzut.png", "images/rzut2.png")
        self.powrot_button = Button(700, 800, 400, 100, "images/powrot.png", "images/powrot2.png")

    def catch_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def reset_game(self):
        self.board = Board(self.window)
        self.ustawianie_pierwszenstwa = True
        self.current_color = "black" 
        self.pionek_usuniety = False
        self.double_dice_white = False
        self.double_dice_black = False
        self.double_roll_white = None
        self.double_roll_black = None
        self.dice1_used = False
        self.dice2_used = False
        
       

    def draw_buttons(self):
        if self.ustawianie_pierwszenstwa:
            self.ustawianie_button.draw(self.window)
        else:
            self.rzut_button.draw(self.window)
        self.powrot_button.draw(self.window)

    def resize_window(self, width, height):
        self.window = pygame.display.set_mode((width, height))

    def display_dice_results(self, result1, result2):
        text1 = self.font.render(f"Pierwsza kostka: {result1}", True, (255, 255, 255))
        text2 = self.font.render(f"Druga kostka: {result2}", True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 20))
        text2_rect = text2.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 + 20))
        self.window.blit(text1, text1_rect)
        self.window.blit(text2, text2_rect)
        pygame.display.update()
        pygame.time.delay(3000)

    def first_projection(self):
        # Sprawdzanie, czy to pierwszy rzut dla danego gracza
        if self.current_color == "white":
            if not self.double_dice_white:  # Sprawdzenie, czy to pierwszy rzut białego gracza
                if self.random_dice1 == self.random_dice2:  # Sprawdzenie, czy wyrzucono dublet
                    self.double_roll_white = self.random_dice1
            self.double_dice_white = True  # Ustawienie flagi po pierwszym rzucie białego gracza

        elif self.current_color == "black":
            if not self.double_dice_black:  # Sprawdzenie, czy to pierwszy rzut czarnego gracza
                if self.random_dice1 == self.random_dice2:  # Sprawdzenie, czy wyrzucono dublet
                    self.double_roll_black = self.random_dice1
            self.double_dice_black = True  # Ustawienie flagi po pierwszym rzucie czarnego gracza

    def obsługa_przycisków(self):
        if self.ustawianie_button.is_clicked() and self.ustawianie_pierwszenstwa:
            first_dice1, first_dice2 = self.catch_dice()
            if first_dice1 > first_dice2:
                text = self.font.render("Gracz 1 zaczyna!", True, (255, 255, 255))
            elif first_dice2 > first_dice1:
                text = self.font.render("Gracz 2 zaczyna!", True, (255, 255, 255))
            else:
                text = self.font.render("Równa liczba oczek, losowanie jeszcze raz...", True, (255, 255, 255))
                self.window.blit(text, (self.window.get_width() // 2 - text.get_width() // 2, self.window.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(2000)
                return
            text_rect = text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 20))
            self.window.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            self.ustawianie_pierwszenstwa = False
        elif self.rzut_button.is_clicked() and not self.ustawianie_pierwszenstwa:
            self.random_dice1, self.random_dice2 = self.catch_dice()
            self.display_dice_results(self.random_dice1, self.random_dice2)
            self.dice_result = self.random_dice1 + self.random_dice2

            self.dice1_used = False  # Resetowanie zmiennej
            self.dice2_used = False  # Resetowanie zmiennej
            
            self.pionek_usuniety = False  # Resetowanie flagi przy nowym rzucie, 1 usunięty pionek na rzut
                                        
            self.current_color = "white" if self.current_color == "black" else "black"  # Zmiana aktualnego koloru gracza

        elif self.powrot_button.is_clicked():
            self.reset_game()
            self.resize_window(1200, 800)
            from main import main  # Import tutaj, zamiast na górze pliku
            main()
            return

    
    def start(self):
        background = pygame.image.load("images/background.jpg")
        background = pygame.transform.scale(background, (1200, 800))
        run = True

        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:                            
                    self.obsługa_przycisków()
                            
                    if not self.ustawianie_pierwszenstwa and self.dice_result != 0:
                        self.first_projection()
                        mouse_x, mouse_y = event.pos
                        if self.current_color == "white":
                            if self.board.pionki1 and not self.pionek_usuniety:
                                self.board.remove_from_stack(self.current_color, self.board.pionki1[-1])
                                if self.double_roll_white is not None:
                                    self.board.remove_from_stack(self.current_color, self.board.pionki1[-1])
                                self.pionek_usuniety = True
                            pionki_wyprowadzone = self.board.pionki_wyprowadzone1
                        else:
                            if self.board.pionki2 and not self.pionek_usuniety:
                                self.board.remove_from_stack(self.current_color, self.board.pionki2[-1])
                                if self.double_roll_black is not None:
                                    self.board.remove_from_stack(self.current_color, self.board.pionki2[-1])
                                self.pionek_usuniety = True
                            pionki_wyprowadzone = self.board.pionki_wyprowadzone2

                        for pionek in pionki_wyprowadzone:
                            if pionek.rect.collidepoint(mouse_x, mouse_y):
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

                        for rect in self.board.top_left + self.board.top_right + self.board.down_left + self.board.down_right:
                            if self.selected_pionek.rect.colliderect(rect):
                                if not self.dice1_used:
                                    print("not self.dice1_used:")
                                    if self.is_move_clockwise(self.selected_pionek.previous_position, (rect.x, rect.y), self.random_dice1):
                                        if not self.board.is_opponent_checker_on_position(self.current_color, rect.x, rect.y):
                                            self.selected_pionek.rect.centerx = rect.centerx
                                            self.selected_pionek.rect.centery = rect.centery
                                            self.dice1_used = True
                                            valid_position = True
                                            break  # Przerwij pętlę po znalezieniu pierwszego prawidłowego ruchu
                                elif not self.dice2_used:
                                    print("not self.dice2_used:")
                                    if self.is_move_clockwise(self.selected_pionek.previous_position, (rect.x, rect.y), self.random_dice2):
                                        if not self.board.is_opponent_checker_on_position(self.current_color, rect.x, rect.y):
                                            self.selected_pionek.rect.centerx = rect.centerx
                                            self.selected_pionek.rect.centery = rect.centery
                                            self.dice2_used = True
                                            valid_position = True
                                            break  # Przerwij pętlę po znalezieniu pierwszego prawidłowego ruchu

                        if not valid_position:
                            self.selected_pionek.rect.x, self.selected_pionek.rect.y = self.selected_pionek.previous_position
                        else:
                            self.selected_pionek.update_previous_position()
                            self.expected_move = None
                            self.selected_pionek = None
                    
                     # Po każdym ruchu sprawdź, czy oba rzuty zostały wykorzystane
                    if self.dice1_used and self.dice2_used:     
                        self.dice_result = 0  # Resetowanie wyniku kości, aby wskazać, że gracz zakończył ruchy
                    
                                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging and self.selected_pionek:
                        mouse_x, mouse_y = event.pos
                        self.selected_pionek.rect.x = mouse_x + self.offset_x
                        self.selected_pionek.rect.y = mouse_y + self.offset_y
                
                       
            self.window.blit(background, (0, 0))
            self.board.draw()
            self.draw_buttons()
            pygame.display.update()




    def is_move_clockwise(self, original_pos, new_pos, dice_result):
        current_x, current_y = original_pos
        new_x, new_y = new_pos
        
        # Definiowanie prostokątów wokół pozycji
        target_rect_original = pygame.Rect(current_x, current_y, 75, 75)
        target_rect_new = pygame.Rect(new_x, new_y, 75, 75)

        target_down_right = pygame.Rect(1165,590,75,75)
        target_top_right = pygame.Rect(1165,110,75,75)
        target_top_left = pygame.Rect(97,110,75,75)
        target_down_left = pygame.Rect(97,590,75,75)

         # Obliczanie odległości Manhattan między prostokątami
       
        
        num_end = None
        num_end2 = None


        top_left_quadrant = (current_x < 650 and current_y < 160)
        top_right_quadrant = (current_x >= 650 and current_y < 600)
        down_left_quadrant = (current_x < 650 and current_y >= 160)
        down_right_quadrant = (current_x >= 650 and current_y >= 600)
        
        if down_left_quadrant:
            if (new_x >= 650 and new_y >= 500):
                self.expected_move = (abs(target_rect_new.centerx - target_rect_original.centerx) - 100)//80 
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
            elif (new_x < 650 and new_y >= 160):
                self.expected_move = abs(target_rect_new.centerx - target_rect_original.centerx)//80
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
            else:
                return False
        

        if down_right_quadrant:
            if (new_x >= 650 and new_y < 200):
                if(target_down_right.centerx -  target_rect_original.centerx)//80 != 0:
                    num_end = abs(target_down_right.centerx -  target_rect_original.centerx)//80     # Obliczanie liczby pól, o które przesunięto pionek w swoim kwadracie
                else:
                    num_end = 1
                num_end2 = abs(target_top_right.centerx -  target_rect_new.centerx)//80          # Obliczanie liczby pól, o które przesunięto pionek w nowym kwadracie 
                self.expected_move = (num_end + num_end2 - 1)
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
                else:
                    return False                  
            elif (new_x >= 650 and new_y >= 500):
                self.expected_move = abs(target_rect_new.centerx - target_rect_original.centerx)//80
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
            else:
                return False

        if top_right_quadrant:
            if (new_x < 650 and new_y < 600):
                self.expected_move = (abs(target_rect_new.centerx - target_rect_original.centerx) - 100)//80
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
                else:
                    return False
            elif (new_x >= 650 and new_y < 600):
                self.expected_move = abs(target_rect_new.centerx - target_rect_original.centerx)//80
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
                else:
                    return False
                

        if top_left_quadrant:
            if (new_x < 650 and new_y >= 400):
                if(target_rect_original.centerx - target_top_left.centerx)//80 != 0:
                    num_end = abs(target_rect_original.centerx - target_top_left.centerx + 50)//80     # Obliczanie liczby pól, o które przesunięto pionek w swoim kwadracie
                    print(target_top_left.centerx, target_rect_original.centerx, num_end)
                else:
                    num_end = 1
                num_end2 = abs(target_rect_new.centerx - target_down_left.centerx + 50) // 80         # Obliczanie liczby pól, o które przesunięto pionek w nowym kwadracie 
                print(target_rect_new.centerx, target_down_left.centerx, num_end2)
                self.expected_move = (num_end + num_end2 + 1)
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True             
                else:
                    return False     
            elif (new_x < 650 and new_y < 200):
                self.expected_move = abs(target_rect_original.centerx - target_rect_new.centerx)//80
                print(self.expected_move)
                if self.expected_move == dice_result:
                    return True
            else:
                return False





if __name__ == "__main__":
    game = Game()
    game.start()

    


