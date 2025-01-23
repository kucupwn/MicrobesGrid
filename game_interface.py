import tkinter as tk


class GameInterface:
    def __init__(self, width, height, col, row, game_fields):
        self.width = width
        self.height = height
        self.col_props = col
        self.row_props = row
        self.game_fields = game_fields
        self.create_ui()

    def create_ui(self):
        self.create_root_and_frame()
        self.get_labels_cells_and_game_cells()

    def create_root_and_frame(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=40)

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
                height=4,
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
                height=4,
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
                    height=2,
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
