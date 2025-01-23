import pandas as pd


class GameDataset:
    def __init__(self, dataset):
        self.df = pd.read_excel(dataset)
