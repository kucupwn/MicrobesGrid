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
        self.game_fields = []

        self.create_root_and_frame()
        self.get_labels_cells_and_game_cells()

    def create_root_and_frame(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=100)

    def change_button_text(self, button):
        button.config(text="Changed")

    def get_labels_cells_and_game_cells(self):
        label_font = ("Arial", 18)
        button_font = ("Arial", 20)

        # Add column property labels
        for col_index, col_prop in enumerate(self.col_props):
            label = tk.Label(
                self.frame,
                text=col_prop,
                width=16,
                height=3,
                bg="lightblue",
                font=label_font,
                relief="ridge",
                bd=3,
            )
            label.grid(row=0, column=col_index + 1, padx=10, pady=10)

        # Add row property labels and the clickable grid
        for row_index, row_prop in enumerate(self.row_props):
            # Row property label
            label = tk.Label(
                self.frame,
                text=row_prop,
                width=16,
                height=3,
                bg="lightgreen",
                font=label_font,
                relief="ridge",
                bd=3,
            )
            label.grid(row=row_index + 1, column=0, padx=10, pady=10)

            # Grid cells
            for col_index in range(len(self.col_props)):
                button = tk.Button(
                    self.frame,
                    text="???",
                    width=14,
                    justify="center",
                    font=button_font,
                    bg="lightgray",
                    relief="groove",
                    bd=2,
                    pady=20,
                    command=lambda b=col_index + (
                        row_index * 3
                    ): self.change_button_text(self.game_fields[b]),
                )
                button.grid(row=row_index + 1, column=col_index + 1, padx=10, pady=10)
                self.game_fields.append(button)

    def main_loop(self):
        if self.running:
            self.root.mainloop()


game = MicrobesGrid("microbes.xlsx")
game.main_loop()
