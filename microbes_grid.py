import random
from game_interface import GameInterface
from game_dataset import GameDataset


class MicrobesGrid:
    def __init__(self):
        self.width = 1280
        self.height = 760
        self.running = True
        self.cols = []
        self.rows = []
        self.game_fields = []

        self.init_dataset()
        self.get_random_rows_and_cols()

        self.interface = GameInterface(
            self.width, self.height, self.cols, self.rows, self.game_fields
        )

    def init_dataset(self):
        self.dataset = GameDataset("microbes.xlsx")
        self.dataset.get_all_species()
        self.dataset.get_properties()

    def get_random_rows_and_cols(self):
        while True:
            cols = random.sample(self.dataset.properties, 3)
            cols_desc = [prop[0] for prop in cols]
            rows = []

            shuffled_properties = self.dataset.properties[:]
            random.shuffle(shuffled_properties)

            for prop in self.dataset.properties:
                if len(rows) == 3:
                    self.rows = rows
                    self.cols = cols
                    return

                desc = prop[0]
                name_list = prop[1]

                if desc in cols_desc:
                    continue

                common_1 = list(set(name_list) & set(cols[0][1]))
                common_2 = list(set(name_list) & set(cols[1][1]))
                common_3 = list(set(name_list) & set(cols[2][1]))

                if len(common_1) > 2 and len(common_2) > 2 and len(common_3) > 2:
                    rows.append(prop)

    def main_loop(self):
        if self.running:
            self.interface.root.mainloop()


game = MicrobesGrid()
game.main_loop()
