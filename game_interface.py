import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox

UNKNOWN = "???"


class GameInterface:
    def __init__(
        self,
        width,
        height,
        cols,
        rows,
        game_fields,
        intersections,
        all_species,
        restart_callback,
    ):
        self.width = width
        self.height = height
        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.intersections = intersections
        self.all_species = all_species
        self.restart_callback = restart_callback
        self.label_font = ("Arial", 18)
        self.button_font = ("Arial", 14, "italic")

        self.create_root_and_frame()
        self.get_labels_cells_and_game_cells()

    def create_root_and_frame(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=40)

    def on_button_click(self, button):
        button_text = button.cget("text")

        if button_text == UNKNOWN:
            self.show_combobox(button)
        else:
            self.open_info_panel(self)

    def open_info_panel(self):
        pass

    def show_combobox(self, button):
        # Create a new top-level window for the Combobox
        combobox_window = tk.Toplevel(self.root)
        combobox_window.geometry(
            "300x100+%d+%d"
            % (
                self.root.winfo_x() + self.root.winfo_width() // 2 - 150,
                self.root.winfo_y() + self.root.winfo_height() // 2 - 50,
            )
        )  # Center on the screen
        combobox_window.title("Select Species")
        combobox_window.grab_set()

        # Create the Combobox
        combobox = AutocompleteCombobox(
            combobox_window, completevalues=self.all_species
        )
        combobox.pack(padx=10, pady=10, fill=tk.X)

        def on_select(event):
            selected_value = combobox.get()
            self.check_user_input(selected_value, button)  # Update the button text
            combobox_window.destroy()  # Close the Toplevel window

        def on_enter(event):
            selected_value = combobox.get()
            if selected_value:
                self.check_user_input(selected_value, button)
                combobox_window.destroy()

        combobox.bind("<<ComboboxSelected>>", on_select)
        combobox.bind("<Return>", on_enter)

        combobox.focus()

    def check_user_input(self, selected_value, button):
        # Calculate the button's row and column index
        button_index = self.game_fields.index(button)
        row_index = button_index // len(self.col_props)
        col_index = button_index % len(self.col_props)

        # Get the intersection related to this row and column combination
        intersection = self.intersections[row_index][col_index]

        # Check if the selected value exists in the intersection for this position
        if selected_value in intersection:
            button.config(text=selected_value)
        else:
            button.config(text=UNKNOWN)
            button.config(bg="red")
            self.reset_button_bg_delayed(button)

    def reset_button_bg_delayed(self, button):
        button.after(1000, lambda: button.config(bg="lightgray"))

    def reset_ui(self, cols, rows, game_fields):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.get_labels_cells_and_game_cells()

    def get_labels_cells_and_game_cells(self):
        # Set up gamefield

        # Add restart button
        restart_button = tk.Button(
            self.frame,
            text="Restart",
            width=10,
            justify="center",
            font=self.label_font,
            bg="red",
            fg="white",
            relief="groove",
            bd=2,
            command=self.restart_callback,
        )
        restart_button.grid(row=0, column=0, padx=10, pady=10)

        # Add column property labels
        for col_index, col_prop in enumerate(self.col_props):
            label = tk.Label(
                self.frame,
                text=col_prop[0],
                width=16,
                height=4,
                bg="lightblue",
                font=self.label_font,
                relief="ridge",
                bd=3,
            )
            label.grid(row=0, column=col_index + 1, padx=10, pady=10)

        # Add row property labels and the clickable grid
        for row_index, row_prop in enumerate(self.row_props):
            label = tk.Label(
                self.frame,
                text=row_prop[0],
                width=16,
                height=4,
                bg="lightgreen",
                font=self.label_font,
                relief="ridge",
                bd=3,
            )
            label.grid(row=row_index + 1, column=0, padx=10, pady=10)

            # Grid cells
            for col_index in range(len(self.col_props)):
                button = tk.Button(
                    self.frame,
                    text=UNKNOWN,
                    width=20,
                    height=2,
                    justify="center",
                    font=self.button_font,
                    bg="lightgray",
                    relief="groove",
                    bd=2,
                    pady=20,
                    command=lambda b=col_index + (row_index * 3): self.show_combobox(
                        self.game_fields[b]
                    ),
                )
                button.grid(row=row_index + 1, column=col_index + 1, padx=10, pady=10)
                self.game_fields.append(button)
