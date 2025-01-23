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
        self.all_species = []
        self.properties = []
        
    def get_all_species(self):
        all_sp = self.df.apply(lambda row: f'{row['Genus']} {row['Species']}', axis=1)
        self.all_species = list(all_sp)
        
    def get_species_name_list(self, df):
        return df.apply(lambda row: f'{row['Genus']} {row['Species']}', axis=1).tolist()
        
    def get_properties(self):
        gram_positive_df = self.df[self.df['Gram Stain'] == 'Positive']
        gram_positive_list = self.get_species_name_list(gram_positive_df)
        gram_positive = {'Gram positive species': gram_positive_list}
        self.properties.append(gram_positive)

        gram_negative_df = self.df[self.df['Gram Stain'] == 'Negative']
        gram_negative_list = self.get_species_name_list(gram_negative_df)
        gram_negative = {'Gram negative species': gram_negative_list}
        self.properties.append(gram_negative)
        
        rod_shape_df = self.df[self.df["Shape"] == "Rod"]
        rod_shape_list = self.get_species_name_list(rod_shape_df)
        rod_shape = {'Rod shape species': rod_shape_list}
        self.properties.append(rod_shape)
        
        sphere_shape_df = self.df[self.df["Shape"].isin(SPHERE_SHAPE)]
        sphere_shape_list = self.get_species_name_list(sphere_shape_df)
        sphere_shape = {'Sphere shape species': sphere_shape_list}
        self.properties.append(sphere_shape)
        
        other_shape_df = self.df[self.df["Shape"].isin(OTHER_SHAPE)]
        other_shape_list = self.get_species_name_list(other_shape_df)
        other_shape = {'Other shape species': other_shape_list}
        self.properties.append(other_shape)
        
        less_than_40_gc_content_df = self.df[self.df["GC Content"] < 40]
        less_than_40_gc_content_list = self.get_species_name_list(less_than_40_gc_content_df)
        less_than_40_gc_content = {'GC content < 40%': less_than_40_gc_content_list}
        self.properties.append(less_than_40_gc_content)
        
        between_40_60_gc_content_df = self.df[(self.df['GC Content'] >= 40) & (self.df['GC Content'] <= 60)]
        between_40_60_gc_content_list = self.get_species_name_list(between_40_60_gc_content_df)
        between_40_60_gc_content = {'GC content: 40-60%': between_40_60_gc_content_list}
        self.properties.append(between_40_60_gc_content)

        more_than_60_gc_content_df = self.df[self.df["GC Content"] > 60]
        more_than_60_gc_content_list = self.get_species_name_list(more_than_60_gc_content_df)
        more_than_60_gc_content = {'GC content > 60%': more_than_60_gc_content_list}
        self.properties.append(more_than_60_gc_content)