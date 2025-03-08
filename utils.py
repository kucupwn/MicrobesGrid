import os
import sys
import pandas as pd


def get_xlsx_file():
    if getattr(sys, "frozen", False):
        # Running as a bundled .exe
        return os.path.join(sys._MEIPASS, "microbes.xlsx")
    else:
        # Running as a normal Python script
        return os.path.join(os.path.dirname(__file__), "microbes.xlsx")


def load_dataset():
    xlsx_file = get_xlsx_file()

    return pd.read_excel(xlsx_file)


DATASET = load_dataset()
