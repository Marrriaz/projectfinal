import pygame
import sys
import os
from random import shuffle
import time

class SlidePuzzle:
    def __init__(self, gs, ts, ms):
        self.gs, self.ts, self.ms = gs, ts, ms
        self.tiles_len = (gs[0] * gs[1]) - 1
        self.tiles = [(x, y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilesOG = [(x, y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilespos = {(x, y): (x * (ts + ms) + ms, y * (ts + ms) + ms) for y in range(gs[1]) for x in range(gs[0])}
        self.font = pygame.font.Font(None, 120)
        w, h = gs[0] * (ts + ms) + ms, gs[1] * (ts + ms) + ms

        image_path = "hand.png"  
        pic = self.load_image_from_file(image_path)
        pic = pygame.transform.scale(pic, (w, h))

        self.images = []
        for i in range(self.tiles_len):
            x, y = self.tilespos[self.tiles[i]]
            image = pic.subsurface(x, y, ts, ts)
            self.images.append(image)

        self.shuffle_tiles()

    def load_image_from_file(self, path):
        img = pygame.image.load(path)
        return img

    def shuffle_tiles(self):
        self.temp = self.tiles[:-1]
        shuffle(self.temp)
        self.temp.append(self.tiles[-1])
        self.tiles = self.temp

    def getBlank(self):
        return self.tiles[-1]

    def setBlank(self, pos):
        self.tiles[-1] = pos

    opentile = property(getBlank, setBlank)

    def switch(self, tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        if self.tiles == self.tilesOG:
            print("COMPLETE")

    def is_grid(self, tile):
        return 0 <= tile[0] < self.gs[0] and 0 <= tile[1] < self.gs[1]

    def adjacent(self):
        x, y = self.opentile
        return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)

    def update(self, dt):
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()

        if mouse[0]:
            tile = mpos[0] // self.ts, mpos[1] // self.ts

            if self.is_grid(tile):
                if tile in self.adjacent():
                    self.switch(tile)

    def draw(self, screen):
        for i in range(self.tiles_len):
            x, y = self.tilespos[self.tiles[i]]
            screen.blit(self.images[i], (x, y))


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Slide Puzzle")
    screen = pygame.display.set_mode((600, 600))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((3, 3), 200, 5)
    start_time = time.time()  # Start timer

    while True:
        dt = fpsclock.tick() / 1000
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        screen.fill((1, 0, 0))

        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        program.update(dt)

        if elapsed_time > 60:  # Check if more than 60 seconds have passed
            print("You lose! Restarting the game.")
            program.shuffle_tiles()  # Shuffle tiles to restart the game
            start_time = time.time()  # Reset timer

if __name__ == '__main__':
    main()
