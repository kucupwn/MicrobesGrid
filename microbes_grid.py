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
        self.intersections = []

        self.init_dataset()
        self.get_random_rows_and_cols()

        self.interface = GameInterface(
            self.width,
            self.height,
            self.cols,
            self.rows,
            self.game_fields,
            self.intersections,
            self.dataset.all_species,
            self.restart_game,
        )
        self.game_fields = self.interface.game_fields

    def init_dataset(self):
        self.dataset = GameDataset("microbes.xlsx")
        self.dataset.get_all_species()
        self.dataset.get_properties()

    def get_random_rows_and_cols(self):
        while True:
            # Initiate 3 random columns
            cols = random.sample(self.dataset.properties, 3)
            cols_desc = [prop[0] for prop in cols]
            rows = []

            # Shuffle properties order
            shuffled_properties = self.dataset.properties[:]
            random.shuffle(shuffled_properties)

            for prop in self.dataset.properties:
                # Return when all cols and rows got matched
                if len(rows) == 3:
                    self.rows = rows
                    self.cols = cols
                    return

                # Unpack tuple
                desc = prop[0]
                name_list = prop[1]
                name_list_set = set(name_list)

                if desc in cols_desc:
                    continue

                # Check common values between cols and current row
                common_1 = list(name_list_set & set(cols[0][1]))
                common_2 = list(name_list_set & set(cols[1][1]))
                common_3 = list(name_list_set & set(cols[2][1]))

                # Check if there are at least 3 match in all 3 intersection
                if len(common_1) > 2 and len(common_2) > 2 and len(common_3) > 2:
                    rows.append(prop)
                    self.intersections.append([common_1, common_2, common_3])

    def restart_game(self):
        self.cols = []
        self.rows = []
        self.game_fields = []
        self.get_random_rows_and_cols()
        self.interface.reset_ui(self.cols, self.rows, self.game_fields)

    def open_search(self):
        pass

    def main_loop(self):
        if self.running:
            self.interface.root.mainloop()


game = MicrobesGrid()
game.main_loop()
