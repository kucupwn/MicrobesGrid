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
                    prop_result = (f"{col}: \n{prop[0]}", prop_list)
                    self.properties.append(prop_result)

    def get_properties(self):
        gram_positive_df = self.df[self.df["Gram Stain"] == "Positive"]
        gram_positive_list = self.get_species_name_list(gram_positive_df)
        gram_positive = ("Gram positive \nspecies", gram_positive_list)
        self.properties.append(gram_positive)

        gram_negative_df = self.df[self.df["Gram Stain"] == "Negative"]
        gram_negative_list = self.get_species_name_list(gram_negative_df)
        gram_negative = ("Gram negative \nspecies", gram_negative_list)
        self.properties.append(gram_negative)

        rod_shape_df = self.df[self.df["Shape"] == "Rod"]
        rod_shape_list = self.get_species_name_list(rod_shape_df)
        rod_shape = ("Rod shape \nspecies", rod_shape_list)
        self.properties.append(rod_shape)

        sphere_shape_df = self.df[self.df["Shape"].isin(SPHERE_SHAPE)]
        sphere_shape_list = self.get_species_name_list(sphere_shape_df)
        sphere_shape = ("Sphere shape \nspecies", sphere_shape_list)
        self.properties.append(sphere_shape)

        other_shape_df = self.df[self.df["Shape"].isin(OTHER_SHAPE)]
        other_shape_list = self.get_species_name_list(other_shape_df)
        other_shape = ("Other shape \nspecies", other_shape_list)
        self.properties.append(other_shape)

        aerobe_df = self.df[self.df["Metabolism"] == "Aerobe"]
        aerobe_list = self.get_species_name_list(aerobe_df)
        aerobe = ("Metabolism: \naerobe", aerobe_list)
        self.properties.append(aerobe)

        anaerobe_df = self.df[self.df["Metabolism"] == "Anaerobe"]
        anaerobe_list = self.get_species_name_list(anaerobe_df)
        anaerobe = ("Metabolism: \nanaerobe", anaerobe_list)
        self.properties.append(anaerobe)

        fac_anaerobe_df = self.df[self.df["Metabolism"] == "Facultative Anaerobe"]
        fac_anaerobe_list = self.get_species_name_list(fac_anaerobe_df)
        fac_anaerobe = ("Metabolism: \nfacultative anaerobe", fac_anaerobe_list)
        self.properties.append(fac_anaerobe)

        microaerophilic_df = self.df[self.df["Metabolism"] == "Microaerophilic"]
        microaerophilic_list = self.get_species_name_list(microaerophilic_df)
        microaerophilic = ("Metabolism: \nmicroaerophilic", microaerophilic_list)
        self.properties.append(microaerophilic)

        less_than_40_gc_content_df = self.df[self.df["GC Content"] < 40]
        less_than_40_gc_content_list = self.get_species_name_list(
            less_than_40_gc_content_df
        )
        less_than_40_gc_content = ("GC content \n< 40%", less_than_40_gc_content_list)
        self.properties.append(less_than_40_gc_content)

        between_40_60_gc_content_df = self.df[
            (self.df["GC Content"] >= 40) & (self.df["GC Content"] <= 60)
        ]
        between_40_60_gc_content_list = self.get_species_name_list(
            between_40_60_gc_content_df
        )
        between_40_60_gc_content = (
            "GC content: \n40-60%",
            between_40_60_gc_content_list,
        )
        self.properties.append(between_40_60_gc_content)

        more_than_60_gc_content_df = self.df[self.df["GC Content"] > 60]
        more_than_60_gc_content_list = self.get_species_name_list(
            more_than_60_gc_content_df
        )
        more_than_60_gc_content = ("GC content \n> 60%", more_than_60_gc_content_list)
        self.properties.append(more_than_60_gc_content)
