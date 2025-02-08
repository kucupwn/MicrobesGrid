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
        df,
    ):
        self.width = width
        self.height = height
        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.intersections = intersections
        self.all_species = all_species
        self.restart_callback = restart_callback
        self.df = df
        self.label_font = ("Arial", 18)
        self.button_font = ("Arial", 14, "italic")
        self.attempts = 0

        self.create_root_and_frame()
        self.get_labels_cells_and_game_cells()

    # UI Setup

    def create_root_and_frame(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=40)

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
                bg="lightblue",
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
                    command=lambda b=col_index + (
                        row_index * 3
                    ): self.input_combobox_events(self.game_fields[b]),
                )
                button.grid(row=row_index + 1, column=col_index + 1, padx=10, pady=10)
                self.game_fields.append(button)

        info_button = tk.Button(
            self.frame,
            text="Info Centre",
            width=10,
            justify="center",
            font=self.button_font,
            bg="lightgray",
            relief="groove",
            bd=2,
            command=self.info_centre_combobox_events,
        )
        info_button.grid(row=4, column=0, padx=10, pady=10)

    def reset_ui(self, cols, rows, game_fields, intersections):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Generate new random game in main file
        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.intersections = intersections
        self.get_labels_cells_and_game_cells()

    def create_toplevel_window(self, width, height, title):
        toplevel_window = tk.Toplevel(self.root)
        toplevel_window.title(title)

        position_left, position_top = self.window_placement_middle(
            toplevel_window, width, height
        )

        toplevel_window.geometry(f"{width}x{height}+{position_left}+{position_top}")

        return toplevel_window

    def create_combobox(self):
        # Create a new top-level window for the Combobox
        combobox_window = self.create_toplevel_window(300, 60, "Select Species")

        # Create the Combobox
        combobox = AutocompleteCombobox(
            combobox_window, completevalues=self.all_species
        )
        combobox.pack(padx=10, pady=10, fill=tk.X)

        return {"window": combobox_window, "combobox": combobox}

    # Event handling

    def bind_enter_event_function(self, combobox, func):
        combobox.bind("<<ComboboxSelected>>", func)
        combobox.bind("<Return>", func)

        combobox.focus()

    def input_combobox_events(self, button):
        # Disable clicking after successful guess
        if button.cget("text") != UNKNOWN:
            return

        combobox = self.create_combobox()

        # Enter event
        def on_enter(event):
            selected_value = combobox["combobox"].get()
            if selected_value:
                self.user_input_feedback(selected_value, button)
                combobox["window"].destroy()

        self.bind_enter_event_function(combobox["combobox"], on_enter)

    def check_win(self):
        for button in self.game_fields:
            if button.cget("text") == UNKNOWN:
                return False

        return True

    def display_win(self):
        # Create a new top-level window for info view
        info_window = self.create_toplevel_window(460, 160, "Game Over")

        tk.Label(
            info_window,
            text="You Won!",
            font=("Arial", 72),
            justify="center",
            padx=10,
            pady=5,
        ).pack()

        tk.Label(
            info_window,
            text=f"... from {self.attempts} attempts.",
            font=("Arial", 24),
            justify="center",
            padx=10,
            pady=5,
        ).pack()

    def is_existing_value(self, value):
        for button in self.game_fields:
            button_text = button.cget("text").replace("\n", " ")
            if button_text == value:
                return True

        return False

    def user_input_feedback(self, selected_value, button):
        self.attempts += 1

        # Calculate the button's row and column index
        button_index = self.game_fields.index(button)
        row_index = button_index // len(self.col_props)
        col_index = button_index % len(self.col_props)

        # Get the intersection related to this row and column combination
        intersection = self.intersections[row_index][col_index]

        # Check if the selected value exists in the intersection for this position
        if selected_value not in intersection or self.is_existing_value(selected_value):
            # Change background to red
            button.config(bg="red")
            # 1 sec later background change to default
            self.reset_button_bg_delayed(button)
        else:
            # Add linebreak for better display
            line_break_name = selected_value.replace(" ", "\n")
            # Change button text to input
            button.config(text=line_break_name)

            if self.check_win():
                self.display_win()

    def reset_button_bg_delayed(self, button):
        button.after(1000, lambda: button.config(bg="lightgray"))

    def info_centre_combobox_events(self):
        combobox = self.create_combobox()

        # Enter event
        def on_enter(event):
            selected_value = combobox["combobox"].get()
            if selected_value:
                self.display_species_info(selected_value)
                combobox["window"].grab_release()
                combobox["window"].destroy()

        self.bind_enter_event_function(combobox["combobox"], on_enter)

    def display_species_info(self, name):
        # Split name into Genus and Species
        name_cols = name.split(" ")

        # Filter the DataFrame based on Genus and Species
        name_row = self.df[
            (self.df["Genus"] == name_cols[0]) & (self.df["Species"] == name_cols[1])
        ]

        # Create a new top-level window for info view
        info_window = self.create_toplevel_window(350, 680, f"Details for {name}")

        # Add key-value pairs in the format "Column Name: Value"
        for col in self.df.columns:
            value = name_row.iloc[0][col]  # Get the value for the current column
            tk.Label(
                info_window,
                text=f"{col}: {value}",
                font=("Arial", 12),
                anchor="w",
                justify="left",
                padx=10,
                pady=5,
            ).pack(anchor="w")

    # Util

    def window_placement_middle(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        return (position_left, position_top)
