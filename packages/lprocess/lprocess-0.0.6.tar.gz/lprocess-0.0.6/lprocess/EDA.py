import pandas as pd

class EDA:
    def __init__(self, df):
        self.df = df

    def summary_statistics(self):
        """
        Generate summary statistics for the DataFrame.

        Returns:
        pandas.DataFrame: Summary statistics DataFrame.
        """
        summary_stats = self.df.describe(include='all').transpose()
        summary_stats['missing_values'] = self.df.isnull().sum()
        return summary_stats

    def summary_tables(self):
        """
        Generate summary tables for categorical variables.

        Returns:
        dict: Summary tables for categorical variables.
        """
        summary_tables = {}
        for column in self.df.select_dtypes(include=['object']):
            summary_tables[column] = self.df[column].value_counts()
        return summary_tables
