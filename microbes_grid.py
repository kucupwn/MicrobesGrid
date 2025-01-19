import tkinter as tk
import pandas as pd

WHITE = (255, 255, 255)


class MicrobesGrid:
    def __init__(self, data_source):
        self.df = pd.read_excel(data_source)
        self.width = 1280
        self.height = 760
        self.running = True
        self.row_props = ["Rod", "Coccus", "Spiral"]
        self.col_props = ["Gram Positive", "Gram Negative", "Acid Fast"]

        self.create_root()
        self.get_labels_and_cells()

    def create_root(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

    def get_labels_and_cells(self):
        # Add column property labels
        for col_index, col_prop in enumerate(self.col_props):
            label = tk.Label(
                self.frame, text=col_prop, width=15, height=2, bg="lightblue"
            )
            label.grid(row=0, column=col_index + 1, padx=5, pady=5)

        # Add row property labels and the clickable grid
        for row_index, row_prop in enumerate(self.row_props):
            # Row property label
            label = tk.Label(
                self.frame, text=row_prop, width=15, height=2, bg="lightgreen"
            )
            label.grid(row=row_index + 1, column=0, padx=5, pady=5)

            # Grid cells
            for col_index in range(len(self.col_props)):
                entry = tk.Entry(self.frame, width=15, justify="center")
                entry.grid(row=row_index + 1, column=col_index + 1, padx=5, pady=5)

    def main_loop(self):
        if self.running:
            self.root.mainloop()


game = MicrobesGrid("microbes.xlsx")
game.main_loop()
