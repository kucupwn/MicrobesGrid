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

    def create_property_tuple(self, col, prop):
        prop_df = self.df[self.df[col] == prop[0]]
        prop_list = self.get_species_name_list(prop_df)
        prop_result = (f"{col}:\n{prop[0]}", prop_list)

        return prop_result

    def get_properties(self):
        for col in self.columns:
            if col == "Domain" or col == "Genus" or col == "Species":
                continue

            col_values = self.df.groupby(col, as_index=False).size()

            if col == "Shape":
                self.get_shape_property(col, col_values)

            if col == "GC Content":
                self.get_gc_content_property(col, col_values)

            for _, prop in col_values.iterrows():
                if prop["size"] > 2:
                    prop_result = self.create_property_tuple(col, prop)
                    self.properties.append(prop_result)

    def get_shape_property(self, col, values):
        for _, prop in values.iterrows():
            if prop["size"] > 2:
                if prop[0] == "Rod":
                    prop_result = self.create_property_tuple(col, prop)
                    self.properties.append(prop_result)
                elif prop[0] in SPHERE_SHAPE:
                    prop_df = self.df[self.df[col].isin(SPHERE_SHAPE)]
                    prop_list = self.get_species_name_list(prop_df)
                    prop_result = (f"{col}:\nSphere", prop_list)
                    self.properties.append(prop_result)
                elif prop[0] in OTHER_SHAPE:
                    prop_df = self.df[self.df[col].isin(OTHER_SHAPE)]
                    prop_list = self.get_species_name_list(prop_df)
                    prop_result = (f"{col}:\nNOT Rod or Sphere", prop_list)
                    self.properties.append(prop_result)

    def get_gc_content_property(self):
        pass
