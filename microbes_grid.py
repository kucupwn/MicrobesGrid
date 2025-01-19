import pygame
import pandas as pd

WHITE = (255, 255, 255)


class MicrobesGrid:
    def __init__(self, data_source):
        self.df = pd.read_excel(data_source)
        self.width = 1280
        self.height = 760
        self.running = True

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Microbes Grid")

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.clock.tick(60)
        self.screen.fill(WHITE)

    def main_loop(self):
        while self.running:
            self.update()
            self.event_handler()


game = MicrobesGrid("microbes.xlsx")
game.main_loop()
