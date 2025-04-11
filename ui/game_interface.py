import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from typing import Callable
from .ui_utils import get_restart_button, get_label, get_gamefield_button, get_info_button


class GameInterface:
    def __init__(self, game) -> None:
        self.game = game
        self.text_unknown = '???'
        self.text_info_centre = 'Info Centre'
        self.label_font = ("Arial", 18)
        self.button_font = ("Arial", 14, "italic")

        self.create_root_and_frame()
        self.get_labels_cells_game_cells()
        
    def main_loop(self) -> None:
        self.root.mainloop()

    # UI Setup

    def create_root_and_frame(self) -> None:
        """
        Creates tkinter root and frame
        """

        self.root = tk.Tk()
        self.root.geometry(f"{self.game.width}x{self.game.height}")
        self.root.title("Microbes Grid")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=40, pady=40)

    def get_labels_cells_game_cells(self) -> None:
        """
        Creates full game field in grid form: restart button, col-row labels, 9 guess button, info centre button
        """

        # Add restart button
        restart_button = get_restart_button(self.frame, self.label_font, self.reset_ui)
        restart_button.grid(row=0, column=0, padx=10, pady=10)

        # Add column property labels
        for col_index, col_prop in enumerate(self.game.cols):
            label = get_label(self.frame, self.label_font, col_prop)
            label.grid(row=0, column=col_index + 1, padx=10, pady=10)
            
        cols_count = len(self.game.cols)
        
        # Add row property labels and the clickable grid
        for row_index, row_prop in enumerate(self.game.rows):
            label = get_label(self.frame, self.label_font, row_prop)
            label.grid(row=row_index + 1, column=0, padx=10, pady=10)

            # Grid cells
            for col_index in range(cols_count):
                button = get_gamefield_button(self, self.frame, self.button_font, self.text_unknown, cols_count, col_index, row_index)
                button.grid(row=row_index + 1, column=col_index + 1, padx=10, pady=10)
            
        info_button = get_info_button(self.frame, self.button_font, self.input_combobox_events, self.text_info_centre)
        info_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.attempt_label = tk.Label(self.frame, text=f'Attempts: {self.game.attempts}', font=self.button_font)
        self.attempt_label.grid(row=4, column=3, padx=10, pady=10)

    def reset_ui(self) -> None:
        """
        Resets ui and variables
        Generates a new game
        """

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Generate new random game in main file
        self.game.restart_game()
        self.get_labels_cells_game_cells()

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
            combobox_window, completevalues=self.game.dataset.all_species
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
            combobox["window"].destroy()

        # Bind function to combobox
        self.bind_enter_event_function(combobox["combobox"], on_enter)

    
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
            text=f"... from {self.game.attempts} attempts.",
            font=("Arial", 24),
            justify="center",
            padx=10,
            pady=5,
        ).pack()

    
    def user_input_feedback(
        self, selected_value: str, button: tk.Button
    ) -> None:
        """
        Gets buttons position in game_fields
        Checks if answer is correct
        If correct, change button text to answer
        If not correct, change button's background color to red, then back to default
        Checks win
        """

        # Count attempts
        self.game.attempts += 1
        self.attempt_label.config(text=f'Attempts: {self.game.attempts}')

        # Calculate the button's row and column index
        button_index = self.game.game_fields.index(button)
        row_index = button_index // len(self.game.cols)
        col_index = button_index % len(self.game.cols)

        # Get the intersection related to this row and column combination
        intersection = self.game.intersections[row_index][col_index]

        # Check if the selected value exists in the intersection for this position
        if selected_value not in intersection or self.game.is_existing_value(selected_value):
            # Change background to red
            button.config(bg="red")
            # 1 sec later background change to default
            self.reset_button_bg_delayed(button)
        else:
            # Add linebreak for better display
            line_break_name = selected_value.replace(" ", "\n")
            # Change button text to input
            button.config(text=line_break_name)

            if self.game.check_win(self.text_unknown):
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
        name_row = self.game.dataset.df[
            (self.game.dataset.df["Genus"] == name_cols[0]) & (self.game.dataset.df["Species"] == name_cols[1])
        ]

        # Create a new top-level window for info view
        info_window = self.create_toplevel_window(400, 680, f"Details for {name}")

        # Create a frame inside the window to organize labels
        frame = tk.Frame(info_window)
        frame.pack(padx=10, pady=10, anchor="w")

        # Loop through the dataframe columns and display key-value pairs in a table format
        for i, col in enumerate(self.game.dataset.df.columns):
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

    @staticmethod
    def window_placement_middle(window: tk.Toplevel, width: int, height: int):
        """
        Function for positioning top level windows to middle on x and y
        """

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        return (position_left, position_top)