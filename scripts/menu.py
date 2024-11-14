from scripts.settings import *
from scripts.utils import load_image,load_images,Animation,draw_health_bar,draw_bar_hp,toggle_mute



class Menu:
    def __init__(self, game,game_state):
        self.game = game
        self.game_state = game_state
        self.buttons = {
            "Sound": pygame.Rect(300, 150, 200, 50),
            "Fullscreen": pygame.Rect(300, 220, 200, 50),
            "Resume": pygame.Rect(300, 290, 200, 50),
            "Quit": pygame.Rect(300, 360, 200, 50)
        }
        self.selected = None

    def draw(self, screen):
        if self.game_state.fullscreen:
                    info = pygame.display.Info()
                    self.game.assets['menu'] =load_image('menu.jpg',(info.current_w,info.current_h))
                    self.game.screen.blit(self.game.assets['menu'],(0,0))
                    
        else:
                    self.game.screen.blit(self.game.assets['menu'],(0,0))
        

        current_width = screen.get_width()
        center_x = current_width // 2

        # Vẽ các nút
        for button_text, rect in self.buttons.items():
            # Xác định màu sắc của mỗi nút dựa trên trạng thái trong game_state
            if button_text == "Sound":
                color = GREEN if self.game_state.sound_on else RED
            elif button_text == "Fullscreen":
                color = GREEN if self.game_state.fullscreen else RED
            else:
                color = GREEN

            # Căn chỉnh nút vào giữa màn hình
            rect.x = center_x - rect.width // 2

            # Vẽ hình chữ nhật của nút với màu phù hợp
            pygame.draw.rect(screen, color, rect)

            # Tạo và vẽ văn bản vào giữa nút
            text = font.render(button_text, True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_text, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    self.selected = button_text
                    return self.selected
        return None
