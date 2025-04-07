import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
import pandas as pd
from typing import Callable


class GameInterface:
    def __init__(
        self,
        width: int,
        height: int,
        cols: list,
        rows: list,
        game_fields: list,
        intersections: list,
        all_species: tuple,
        restart_callback: Callable,
        df: pd.DataFrame,
    ) -> None:
        self.width = width
        self.height = height
        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.intersections = intersections
        self.all_species = all_species
        self.restart_callback = restart_callback
        self.df = df
        self.text_unknown = '???'
        self.text_info_centre = 'Info Centre'
        self.label_font = ("Arial", 18)
        self.button_font = ("Arial", 14, "italic")
        self.attempts = 0

        self.create_root_and_frame()
        self.get_labels_cells_and_game_cells()

    # UI Setup

    def create_root_and_frame(self) -> None:
        """
        Creates tkinter root and frame
        """

        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=40)

    def get_labels_cells_and_game_cells(self) -> None:
        """
        Creates full game field in grid form: restart button, col-row labels, 9 guess button, info centre button
        """

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
                    text=self.text_unknown,
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
            text=self.text_info_centre,
            width=10,
            justify="center",
            font=self.button_font,
            bg="lightgray",
            relief="groove",
            bd=2,
            command=self.input_combobox_events,
        )
        info_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.attempt_label = tk.Label(self.frame, text=f'Attempts: {self.attempts}', font=("Arial", 18, "italic"))
        self.attempt_label.grid(row=4, column=3, padx=10, pady=10)

    def reset_ui(
        self, cols: list, rows: list, game_fields: list, intersections: list
    ) -> None:
        """
        Resets ui and variables
        Generates a new game
        """

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Generate new random game in main file
        self.attempts = 0
        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.intersections = intersections
        self.get_labels_cells_and_game_cells()

    def create_toplevel_window(
        self, width: int, height: int, title: str
    ) -> tk.Toplevel:
        """
        Creates top level window to put search box on it
        """

        toplevel_window = tk.Toplevel(self.root)
        toplevel_window.title(title)

        # Calculate position
        position_left, position_top = self.window_placement_middle(
            toplevel_window, width, height
        )

        # Set position
        toplevel_window.geometry(f"{width}x{height}+{position_left}+{position_top}")

        return toplevel_window

    def create_combobox(self) -> dict:
        """
        Creates combobox (search bar + drop-down ) for search
        """

        # Create a new top-level window for the Combobox
        combobox_window = self.create_toplevel_window(300, 60, "Select Species")

        # Create the Combobox
        combobox = AutocompleteCombobox(
            combobox_window, completevalues=self.all_species
        )
        combobox.pack(padx=10, pady=10, fill=tk.X)

        return {"window": combobox_window, "combobox": combobox}

    # Event handling

    def bind_enter_event_function(
        self, combobox: AutocompleteCombobox, func: Callable
    ) -> None:
        """
        Binds functions for input events (click and Enter)
        """

        combobox.bind("<<ComboboxSelected>>", func)
        combobox.bind("<Return>", func)

        combobox.focus()

    def input_combobox_events(self, button: tk.Button = None) -> None:
        """
        Creates combobox only if cell has no answer yet
        Handles input events in combobox
        """

        # For gamefield buttons
        if button is not None:
            button_text = button.cget("text")

            # Disable clicking after successful guess
            if button_text != self.text_unknown:
                return

        combobox = self.create_combobox()

        # Enter event
        def on_enter(event: tk.Event) -> None:
            selected_value = combobox["combobox"].get()
            if selected_value:
                # Only None is Info centre
                if button is None:
                    self.display_species_info(selected_value)
                # Gamefields buttons
                else:
                    self.user_input_feedback(selected_value, button)

            # Close combobox window
            combobox["window"].grab_release()
            combobox["window"].destroy()

        # Bind function to combobox
        self.bind_enter_event_function(combobox["combobox"], on_enter)

    def check_win(self) -> bool:
        """
        Checks if all cells are answered correctly
        Returns bool
        """

        for button in self.game_fields:
            # Not win if there's still unknown
            if button.cget("text") == self.text_unknown:
                return False

        return True

    def display_win(self) -> None:
        """
        Creates top level window with win feedback and attempt counts
        """

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

        # Display attempts too
        tk.Label(
            info_window,
            text=f"... from {self.attempts} attempts.",
            font=("Arial", 24),
            justify="center",
            padx=10,
            pady=5,
        ).pack()

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

    def user_input_feedback(
        self, selected_value: AutocompleteCombobox, button: tk.Button
    ) -> None:
        """
        Gets buttons position in game_fields
        Checks if answer is correct
        If correct, change button text to answer
        If not correct, change button's background color to red, then back to default
        Checks win
        """

        # Count attempts
        self.attempts += 1
        self.attempt_label.config(text=f'Attempts: {self.attempts}')

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

    def reset_button_bg_delayed(self, button: tk.Button) -> None:
        """
        Changes back buttons background to default with delay
        """

        button.after(1000, lambda: button.config(bg="lightgray"))

    def display_species_info(self, name: str) -> None:
        """
        Creates top level window for info centre display
        Displays all information of choosen bacteria
        """

        # Split name into Genus and Species
        name_cols = name.split(" ")

        # Filter the DataFrame based on Genus and Species
        name_row = self.df[
            (self.df["Genus"] == name_cols[0]) & (self.df["Species"] == name_cols[1])
        ]

        # Create a new top-level window for info view
        info_window = self.create_toplevel_window(400, 680, f"Details for {name}")

        # Create a frame inside the window to organize labels
        frame = tk.Frame(info_window)
        frame.pack(padx=10, pady=10, anchor="w")

        # Loop through the dataframe columns and display key-value pairs in a table format
        for i, col in enumerate(self.df.columns):
            # Column name
            tk.Label(
                frame, text=f"{col}:", font=("Arial", 12, "bold"), anchor="w"
            ).grid(row=i, column=0, sticky="w", padx=5, pady=2)

            # Value
            value = name_row.iloc[0][col]
            tk.Label(frame, text=value, font=("Arial", 12), anchor="w").grid(
                row=i, column=1, sticky="w", padx=5, pady=2
            )

    # Util

    def window_placement_middle(self, window: tk.Toplevel, width: int, height: int):
        """
        Function for positioning top level windows to middle on x and y
        """

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        return (position_left, position_top)
