import tkinter as tk
import pandas as pd


class MicrobesGrid:
    def __init__(self, data_source):
        self.df = pd.read_excel(data_source)
        self.width = 1280
        self.height = 760
        self.running = True
        self.row_props = ["Rod", "Coccus", "Spiral"]
        self.col_props = ["Gram Positive", "Gram Negative", "Acid Fast"]

        self.create_root_and_frame()
        self.get_labels_and_cells()

    def create_root_and_frame(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=40)

    def get_labels_and_cells(self):
        label_font = ("Arial", 16)
        entry_font = ("Arial", 14)

        # Add column property labels
        for col_index, col_prop in enumerate(self.col_props):
            label = tk.Label(
                self.frame,
                text=col_prop,
                width=20,
                height=3,
                bg="lightblue",
                font=label_font,
            )
            label.grid(row=0, column=col_index + 1, padx=10, pady=10)

        # Add row property labels and the clickable grid
        for row_index, row_prop in enumerate(self.row_props):
            # Row property label
            label = tk.Label(
                self.frame,
                text=row_prop,
                width=20,
                height=3,
                bg="lightgreen",
                font=label_font,
            )
            label.grid(row=row_index + 1, column=0, padx=10, pady=10)

            # Grid cells
            for col_index in range(len(self.col_props)):
                entry = tk.Entry(
                    self.frame, width=20, justify="center", font=entry_font
                )
                entry.grid(row=row_index + 1, column=col_index + 1, padx=10, pady=10)

    def main_loop(self):
        if self.running:
            self.root.mainloop()


game = MicrobesGrid("microbes.xlsx")
game.main_loop()
