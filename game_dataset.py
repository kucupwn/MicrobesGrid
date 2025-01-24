import pandas as pd

SPHERE_SHAPE = [
    "Coccobacillus",
    "Diplococcus",
    "Staphylococcus",
    "Streptococcus",
    "Tetrad",
]
SPIRAL_SHAPE = ["Spiral", "Spirillum"]
OTHER_SHAPE = ["Filamentous", "Pleomorphic", "Vibrio"]


class GameDataset:
    def __init__(self, dataset):
        self.df = pd.read_excel(dataset)
        self.columns = list(self.df.columns)
        self.all_species = []
        self.properties = []

    def get_all_species(self):
        # Get all species for search list
        all_sp = self.df.apply(
            lambda row: f"{row['Genus']} {row['Species']}", axis=1
        ).tolist()
        self.all_species = all_sp

    def get_species_name_list(self, df):
        # Automate name extract to list
        return df.apply(lambda row: f"{row['Genus']} {row['Species']}", axis=1).tolist()

    def get_properties_exp(self):
        for col in self.columns:
            col_values = self.df.groupby(col, as_index=False).size()
            for _, prop in col_values.iterrows():
                if prop["size"] > 2:
                    prop_df = self.df[self.df[col] == prop[0]]
                    prop_list = self.get_species_name_list(prop_df)
                    prop_result = (f"{col}:\n{prop[0]}", prop_list)
                    self.properties.append(prop_result)
