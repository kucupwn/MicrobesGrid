import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import ttk

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

    def reset_ui(self, cols, rows, game_fields):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Generate new random game in main file
        self.col_props = cols
        self.row_props = rows
        self.game_fields = game_fields
        self.get_labels_cells_and_game_cells()

    # Event handling

    def create_combobox(self):
        # Create a new top-level window for the Combobox
        combobox_window = tk.Toplevel(self.root)
        combobox_window.title("Select Species")

        # Toplevel properies
        combobox_width = 300
        combobox_height = 60
        position_left, position_top = self.window_placement_middle(
            combobox_window, combobox_width, combobox_height
        )
        # Set window size and position
        combobox_window.geometry(
            f"{combobox_width}x{combobox_height}+{position_left}+{position_top}"
        )

        # Create the Combobox
        combobox = AutocompleteCombobox(
            combobox_window, completevalues=self.all_species
        )
        combobox.pack(padx=10, pady=10, fill=tk.X)

        return {"window": combobox_window, "combobox": combobox}

    def input_combobox_events(self, button):
        # Disable clicking after successful guess
        if button.cget("text") != UNKNOWN:
            return

        combobox = self.create_combobox()

        # Click event
        def on_select(event):
            selected_value = combobox["combobox"].get()
            self.user_input_feedback(selected_value, button)  # Update the button text
            combobox["window"].destroy()  # Close the Toplevel window

        # Enter event
        def on_enter(event):
            selected_value = combobox["combobox"].get()
            if selected_value:
                self.user_input_feedback(selected_value, button)
                combobox["window"].destroy()

        combobox["combobox"].bind("<<ComboboxSelected>>", on_select)
        combobox["combobox"].bind("<Return>", on_enter)

        combobox["combobox"].focus()

    def user_input_feedback(self, selected_value, button):
        # Calculate the button's row and column index
        button_index = self.game_fields.index(button)
        row_index = button_index // len(self.col_props)
        col_index = button_index % len(self.col_props)

        # Get the intersection related to this row and column combination
        intersection = self.intersections[row_index][col_index]

        # Check if the selected value exists in the intersection for this position
        if selected_value in intersection:
            # Add linebreak for better display
            line_break_name = selected_value.replace(" ", "\n")
            # Change button text to input
            button.config(text=line_break_name)
        else:
            # Change background to red
            button.config(bg="red")
            # 1 sec later background change to default
            self.reset_button_bg_delayed(button)

    def reset_button_bg_delayed(self, button):
        button.after(1000, lambda: button.config(bg="lightgray"))

    def info_centre_combobox_events(self):
        combobox = self.create_combobox()

        # Click event
        def on_select(event):
            selected_value = combobox["combobox"].get()
            self.display_species_info(selected_value)
            combobox["window"].grab_release()  # Release the lock
            combobox["window"].destroy()  # Close the Toplevel window

        # Enter event
        def on_enter(event):
            selected_value = combobox["combobox"].get()
            if selected_value:
                self.display_species_info(selected_value)
                combobox["window"].grab_release()
                combobox["window"].destroy()

        combobox["combobox"].bind("<<ComboboxSelected>>", on_select)
        combobox["combobox"].bind("<Return>", on_enter)

        combobox["combobox"].focus()

    def display_species_info(self, name):
        # Split name into Genus and Species
        name_cols = name.split(" ")

        # Filter the DataFrame based on Genus and Species
        name_row = self.df[
            (self.df["Genus"] == name_cols[0]) & (self.df["Species"] == name_cols[1])
        ]

        # Create a new top-level window for info view
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Details for {name}")

        # Toplevel properties
        window_width = 350
        window_height = 680
        position_left, position_top = self.window_placement_middle(
            info_window, window_width, window_height
        )
        info_window.geometry(
            f"{window_width}x{window_height}+{position_left}+{position_top}"
        )

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
