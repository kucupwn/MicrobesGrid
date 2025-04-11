import tkinter as tk
from typing import Callable

def get_restart_button(frame: tk.Frame, font: tuple, command: Callable) -> tk.Button:
    restart_button = tk.Button(
        frame,
        text="Restart",
        width=10,
        justify="center",
        font=font,
        bg="red",
        fg="white",
        relief="groove",
        bd=2,
        command=command,
    )
    
    return restart_button

def get_label(frame: tk.Frame, font: tuple, prop: list) -> tk.Label:
    label = tk.Label(
        frame,
        text=prop[0],
        width=16,
        height=4,
        bg="lightblue",
        font=font,
        relief="ridge",
        bd=3,
    )
    
    return label

def get_gamefield_button(self, frame: tk.Frame, font: tuple, text: str, cols_count: int, col_index: int, row_index: int) -> tk.Button:
    gamefield_button = tk.Button(
        frame,
        text=text,
        width=20,
        height=2,
        justify="center",
        font=font,
        bg="lightgray",
        relief="groove",
        bd=2,
        pady=20,
        command=lambda b=col_index + (
            row_index * cols_count
        ): self.input_combobox_events(self.game.game_fields[b]),
    )
    
    self.game.game_fields.append(gamefield_button)
    
    return gamefield_button

def get_info_button(frame: tk.Frame, font: tuple, command: Callable, text: str) -> tk.Button:
    info_button = tk.Button(
        frame,
        text=text,
        width=10,
        justify="center",
        font=font,
        bg="lightgray",
        relief="groove",
        bd=2,
        command=command,
    )
    
    return info_button

def center_window(window: tk.Toplevel, width: int, height: int) -> tuple:
        """
        Function for positioning top level windows to middle on x and y
        """

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        return (position_left, position_top)