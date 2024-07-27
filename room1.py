import pygame
import subprocess
import sys
import os

class Room1:
    def __init__(self, window):
        self.window = window
        self.window_width, self.window_height = window.get_size()
        self.background_image1 = pygame.image.load('matrixpill.png')
        self.background_image = pygame.transform.scale(self.background_image1, (self.window_width, self.window_height))
        self.font_path = 'ZenDots-Regular.ttf'
        self.font_size = 14
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.input_text = ''
        self.input_active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.clock = pygame.time.Clock()
        self.input_box = pygame.Rect(370, self.window_height - 150, 150, 40)
        self.prompt_text = "Choose a path (red pill or blue pill)"
        self.prompt_position = (300, self.window_height - 180)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
        elif event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.input_text.lower() == "red pill":
                        self.run_script('riddle.py')
                    elif self.input_text.lower() == "blue pill":
                        self.run_script('shuffle.py')
                    self.input_text = ''
                else:
                    self.input_text += event.unicode

    def run_script(self, script_name):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), script_name))
        try:
            result = subprocess.run(
                ["python3", script_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Output:", result.stdout)
            print("Error:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_name}: {e}")
            print("Output:", e.output)
            print("Error:", e.stderr)

    def render(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background_image, (0, 0))
        prompt_surface = self.font.render(self.prompt_text, True, (255, 255, 255))
        self.window.blit(prompt_surface, self.prompt_position)
        pygame.draw.rect(self.window, (255, 255, 255), self.input_box, 2)
        text_surface = self.font.render(self.input_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.input_box.centerx, self.input_box.centery))
        self.window.blit(text_surface, text_rect)
        self.cursor_timer += self.clock.tick(30) / 1000
        if self.cursor_timer >= 0.5:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
        if self.input_active and self.cursor_visible:
            cursor_rect = pygame.Rect(text_rect.right + 2, text_rect.top, 2, text_rect.height)
            pygame.draw.rect(self.window, (255, 255, 255), cursor_rect)

# Code to test Room1 if run directly
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((894, 700))
    pygame.display.set_caption("Room 1 - The Matrix")
    room1 = Room1(window)

    running = True
    while running:
        for event in pygame.event.get():
            room1.handle_event(event)
        room1.render()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
