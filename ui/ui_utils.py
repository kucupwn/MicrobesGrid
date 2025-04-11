import tkinter as tk
from typing import Callable

def get_restart_button(self, frame: tk.Frame, font: tuple, command: callable):
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

def get_label(self, frame, font, prop):
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