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
SKIP_COLUMNS = ["Domain", "Genus", "Species"]


class GameDataset:
    def __init__(self, dataset: str) -> None:
        self.df = pd.read_excel(dataset)
        self.columns = list(self.df.columns)
        self.all_species = ()
        self.properties = []
        self.all_species = self.get_all_species()

    def get_all_species(self) -> list:
        # Get all species for search list
        all_sp = self.df.apply(
            lambda row: f"{row['Genus']} {row['Species']}", axis=1
        ).tolist()
        all_sp.sort()

        return all_sp

    def get_species_name_list(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automate name extract
        Returns all names as list (eg. 'Vibrio cholerae')
        """

        return df.apply(lambda row: f"{row['Genus']} {row['Species']}", axis=1).tolist()

    def create_property_tuple(self, col: str, prop: pd.Series) -> tuple:
        """
        Args: col is column's name, prop is pandas series (column name with value, and size (count))
        Creates names list
        Returns tuple, [0]: 'column_name: *linebreak* property_value', [1]: list of names with common property values
        """

        # Get filtered df
        prop_df = self.df[self.df[col] == prop[0]]
        # Extract Genus Species name as list
        prop_list = self.get_species_name_list(prop_df)
        # Create (Label str, list) tuple
        # Add line break (\n) for better display
        prop_result = (f"{col}:\n{prop[0]}", prop_list)

        return prop_result

    def get_properties(self) -> None:
        """
        Get all property values with at least 5 occurence (eg. in column 'Foodborne' there are at least 5 'yes')
        Handle special property values
        """

        for col in self.columns:
            # Skip some column
            if col in SKIP_COLUMNS:
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

    def get_shape_property(self) -> None:
        rod_shape_df = self.df[self.df["Shape"] == "Rod"]
        rod_shape_list = self.get_species_name_list(rod_shape_df)
        rod_shape = ("Shape:\nRod", rod_shape_list)
        self.properties.append(rod_shape)

        sphere_shape_df = self.df[self.df["Shape"].isin(SPHERE_SHAPE)]
        sphere_shape_list = self.get_species_name_list(sphere_shape_df)
        sphere_shape = ("Shape:\nSphere", sphere_shape_list)
        self.properties.append(sphere_shape)

        other_shape_df = self.df[self.df["Shape"].isin(OTHER_SHAPE)]
        other_shape_list = self.get_species_name_list(other_shape_df)
        other_shape = ("Shape:\nNOT Rod or Sphere", other_shape_list)
        self.properties.append(other_shape)

    def get_gc_content_property(self) -> None:
        less_than_40_gc_content_df = self.df[self.df["GC Content"] < 40]
        less_than_40_gc_content_list = self.get_species_name_list(
            less_than_40_gc_content_df
        )
        less_than_40_gc_content = ("GC content\n< 40%", less_than_40_gc_content_list)
        self.properties.append(less_than_40_gc_content)

        between_40_60_gc_content_df = self.df[
            (self.df["GC Content"] >= 40) & (self.df["GC Content"] <= 60)
        ]
        between_40_60_gc_content_list = self.get_species_name_list(
            between_40_60_gc_content_df
        )
        between_40_60_gc_content = (
            "GC content:\n40-60%",
            between_40_60_gc_content_list,
        )
        self.properties.append(between_40_60_gc_content)

        more_than_60_gc_content_df = self.df[self.df["GC Content"] > 60]
        more_than_60_gc_content_list = self.get_species_name_list(
            more_than_60_gc_content_df
        )
        more_than_60_gc_content = ("GC content\n> 60%", more_than_60_gc_content_list)
        self.properties.append(more_than_60_gc_content)

    def get_pigment_property(self) -> None:
        not_pigmented_df = self.df[self.df["Pigment Production"] == "No"]
        not_pigmented_list = self.get_species_name_list(not_pigmented_df)
        not_pigmented = ("Pigment Production:\nNo", not_pigmented_list)
        self.properties.append(not_pigmented)

        pigmented_df = self.df[self.df["Pigment Production"] != "No"]
        pigmented_list = self.get_species_name_list(pigmented_df)
        pigmented = ("Pigment Production:\nYes", pigmented_list)
        self.properties.append(pigmented)
