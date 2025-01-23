import random
from game_interface import GameInterface
from game_dataset import GameDataset


class MicrobesGrid:
    def __init__(self, dataset):
        self.width = 1280
        self.height = 760
        self.running = True
        self.cols = ["Gram Positive", "Gram Negative", "Acid Fast"]
        self.rows = ["Rod", "Coccus", "Spiral"]
        self.game_fields = []

        self.init_dataset()

        self.interface = GameInterface(
            self.width, self.height, self.cols, self.rows, self.game_fields
        )

    def init_dataset(self):
        self.dataset = GameDataset("microbes.xlsx")
        self.dataset.get_species_name_list()
        self.dataset.get_properties()

    def get_random_rows_and_cols(self):
        while True:
            cols = random.sample(self.dataset.properties, 3)
            cols_keys = [list(cols.keys())[0] for col in cols]
            rows = []

            shuffled_properties = self.dataset.properties[:]
            random.shuffle(shuffled_properties)

            for prop in self.dataset.properties:
                key, value_list = list(prop.items())[0]

                if len(rows) == 3:
                    self.rows = rows
                    self.cols = cols
                    return

                if key in cols_keys:
                    continue

                common_1 = list(set(value_list) & set(cols[0].values())[0])
                common_2 = list(set(value_list) & set(cols[1].values())[0])
                common_3 = list(set(value_list) & set(cols[2].values())[0])

                if len(common_1) > 4 and len(common_2) > 4 and len(common_3) > 4:
                    rows.append({key: value_list})

    def main_loop(self):
        if self.running:
            self.interface.root.mainloop()


game = MicrobesGrid()
game.main_loop()
