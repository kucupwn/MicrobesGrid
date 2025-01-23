import tkinter as tk
import pandas as pd
from game_interface import GameInterface
from game_dataset import GameDataset


class MicrobesGrid:
    def __init__(self, dataset):
        self.width = 1280
        self.height = 760
        self.running = True
        self.col_props = ["Gram Positive", "Gram Negative", "Acid Fast"]
        self.row_props = ["Rod", "Coccus", "Spiral"]
        self.game_fields = []
        self.dataset = GameDataset(dataset)
        self.interface = GameInterface(
            self.width, self.height, self.col_props, self.row_props, self.game_fields
        )

    def main_loop(self):
        if self.running:
            self.interface.root.mainloop()


game = MicrobesGrid("microbes.xlsx")
game.main_loop()
