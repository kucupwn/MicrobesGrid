import pandas as pd


class GameDataset:
    def __init__(self, dataset: pd.DataFrame) -> None:
        self.df = dataset
        self.columns = list(self.df.columns)
        self.all_species = ()
        self.properties = []
        self.all_species = self.get_all_species()
        self.sphere_shape = ["Coccobacillus","Diplococcus","Staphylococcus","Streptococcus","Tetrad",]
        self.spiral_shape = ["Spiral", "Spirillum"]
        self.other_shape = ["Filamentous", "Pleomorphic", "Vibrio"]
        self.skip_columns = ["Domain", "Genus", "Species"]

    def get_all_species(self) -> list:
        # Get all species for search list
        all_sp = self.df.apply(
            lambda row: f"{row['Genus']} {row['Species']}", axis=1
        ).tolist()
        all_sp.sort()

        return all_sp

    def get_species_name_list(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automated name extract
        Returns all names as list (eg. 'Vibrio cholerae')
        """

        return df.apply(lambda row: f"{row['Genus']} {row['Species']}", axis=1).tolist()

    def create_property_tuple(self, col: str, prop: pd.Series) -> tuple:
        """
        Args: col is column's name, prop is pandas series (column name with value, and size (count))
        Creates names list
        Returns a tuple, [0]: 'column_name: *linebreak* property_value', [1]: list of names with common property values
        """

        # Get filtered df
        prop_df = self.df[self.df[col] == prop.iloc[0]]
        # Extract Genus Species name as list
        prop_list = self.get_species_name_list(prop_df)
        # Create (Label str, list) tuple
        # Add line break (\n) for better display
        prop_result = (f"{col}:\n{prop.iloc[0]}", prop_list)

        return prop_result

    def get_properties(self) -> None:
        """
        Get all property values with at least 5 occurence (eg. in column 'Foodborne' there are at least 5 'yes')
        Handle special property values
        """

        for col in self.columns:
            # Skip some column
            if col in self.skip_columns:
                continue

            # Custom functions for exception
            if col == "Shape":
                self.get_shape_property()
                continue

            if col == "GC Content":
                self.get_gc_content_property()
                continue

            if col == "Pigment Production":
                self.get_pigment_property()
                continue

            # Value counter
            col_values = self.df.groupby(col, as_index=False).size()

            # Universal function for most
            for _, prop in col_values.iterrows():
                # At least 5 occurence of a value
                if prop["size"] >= 5:
                    prop_result = self.create_property_tuple(col, prop)
                    # Append to all properties
                    self.properties.append(prop_result)

    # Special property values
    def get_special_property(self, df: pd.DataFrame, prop_text: str):
        prop_list = self.get_species_name_list(df)
        result = (prop_text, prop_list)
        self.properties.append(result)

    def get_shape_property(self) -> None:
        rod_shape_df = self.df[self.df["Shape"] == "Rod"]
        self.get_special_property(rod_shape_df, "Shape:\nRod")

        sphere_shape_df = self.df[self.df["Shape"].isin(self.sphere_shape)]
        self.get_special_property(sphere_shape_df, "Shape:\nSphere")

        other_shape_df = self.df[self.df["Shape"].isin(self.other_shape)]
        self.get_special_property(other_shape_df, "Shape:\nNOT Rod or Sphere")

    def get_gc_content_property(self) -> None:
        less_than_40_gc_content_df = self.df[self.df["GC Content"] < 40]
        self.get_special_property(less_than_40_gc_content_df, "GC content\n< 40%")

        between_40_60_gc_content_df = self.df[
            (self.df["GC Content"] >= 40) & (self.df["GC Content"] <= 60)
        ]
        self.get_special_property(between_40_60_gc_content_df, "GC content:\n40-60%")

        more_than_60_gc_content_df = self.df[self.df["GC Content"] > 60]
        self.get_special_property(more_than_60_gc_content_df, "GC content\n> 60%")

    def get_pigment_property(self) -> None:
        not_pigmented_df = self.df[self.df["Pigment Production"] == "No"]
        self.get_special_property(not_pigmented_df, "Pigment Production:\nNo")

        pigmented_df = self.df[self.df["Pigment Production"] != "No"]
        self.get_special_property(pigmented_df, "Pigment Production:\nYes")
