import os
import sys
import pandas as pd


def get_xlsx_file():
    base_path = (
        sys._MEIPASS
        if getattr(sys, "frozen", False)
        else os.path.dirname(os.path.abspath(__file__))
    )
    return os.path.join(base_path, "data", "microbes.xlsx")


def load_dataset():
    xlsx_file = get_xlsx_file()

    return pd.read_excel(xlsx_file)


DATASET = load_dataset()
