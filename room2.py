import pygame
import sys
import subprocess

pygame.init()

window_width, window_height = 894, 700
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Room 1 - The Matrix")
background_image1 = pygame.image.load('interstellar.png')
background_image = pygame.transform.scale(background_image1, (window_width, window_height))
font_path = 'InknutAntiqua-Regular.ttf'
font_size = 25
font = pygame.font.Font(font_path, font_size)
input_text = ''
input_active = False
cursor_visible = True
cursor_timer = 0
clock = pygame.time.Clock()

input_box = pygame.Rect(370, window_height - 70, 150, 40)

prompt_text = "Wich planet you wish to visit (1 or 2)?"
prompt_position = (220, window_height - 120)


correct_answer = "red pill"  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text.lower() == correct_answer.lower():
                        pygame.quit()
                        subprocess.run(["python3", "room2.py"])
                    else:
                        print("Wrong answer!")
                    input_text = ''
                else:
                    input_text += event.unicode

    window.fill((0, 0, 0))
    window.blit(background_image, (0, 0))
    prompt_surface = font.render(prompt_text, True, (255, 255, 255))
    window.blit(prompt_surface, prompt_position)
    pygame.draw.rect(window, (255, 255, 255), input_box, 2)

    text_surface = font.render(input_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(input_box.centerx, input_box.centery))
    window.blit(text_surface, text_rect)

    cursor_timer += clock.tick(30) / 1000
    if cursor_timer >= 0.5:
        cursor_timer = 0
        cursor_visible = not cursor_visible

    if input_active and cursor_visible:
        cursor_rect = pygame.Rect(text_rect.right + 2, text_rect.top, 2, text_rect.height)
        pygame.draw.rect(window, (255, 255, 255), cursor_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
