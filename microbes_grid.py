import random
from game_interface import GameInterface
from game_dataset import GameDataset
from utils import DATASET


class MicrobesGrid:
    def __init__(self) -> None:
        self.width = 1280
        self.height = 760
        self.cols = []
        self.rows = []
        self.game_fields = []
        self.intersections = []
        self.attempts = 0

        self.init_dataset()
        self.generate_game()


    def init_dataset(self) -> None:
        """
        Initiate dataset to work from
        All species is a list of strings (eg. 'Staphylococcus aureus')
        Properties is a list of tuples: [0] is the property definition, [1] is the list of names
        """

        self.dataset = GameDataset(DATASET)
        self.dataset.get_all_species()
        self.dataset.get_properties()

    def generate_game(self) -> None:
        """
        Sets up the game's main logic
        Randomly get 3 properties (y values)
        Get 3 more and check if there are enough intersection values
        """

        while True:
            # Initiate 3 random columns
            cols = random.sample(self.dataset.properties, 3)
            cols_desc = [prop[0] for prop in cols]
            rows = []

            # Shuffle properties order
            shuffled_properties = self.dataset.properties[:]
            random.shuffle(shuffled_properties)

            for prop in shuffled_properties:
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
                if len(common_1) >= 3 and len(common_2) >= 3 and len(common_3) >= 3:
                    rows.append(prop)
                    self.intersections.append([common_1, common_2, common_3])
                    
    
    def is_existing_value(self, value: str) -> bool:
        """
        Checks if a name is already used
        Returns bool
        """

        for button in self.game_fields:
            # Transform previous answers line break back to space for comparison
            button_text = button.cget("text").replace("\n", " ")
            # True if answer is already used
            if button_text == value:
                return True

        return False
    
    
    def check_win(self, text_unknown) -> bool:
        """
        Checks if all cells are answered correctly
        Returns bool
        """

        for button in self.game_fields:
            # Not win if there's still unknown
            if button.cget("text") == text_unknown:
                return False

        return True
    
    def restart_game(self) -> None:
        """
        Empty all lists for new generation
        Resets UI
        """

        self.cols = []
        self.rows = []
        self.game_fields = []
        self.intersections = []
        self.attempts = 0
        self.generate_game()
    
    


game = MicrobesGrid()
ui = GameInterface(game)
ui.main_loop()
