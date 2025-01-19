import pygame
import pandas as pd


class MicrobesGrid:
    def __init__(self, data_source):
        self.df = pd.read_excel(data_source)

    def update(self):
        pass

    def main_loop(self):
        pass
