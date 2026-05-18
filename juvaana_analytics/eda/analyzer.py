import pandas as pd

class Analyzer:

    def __init__(self, df):
        self.df = df

    # -----------------------------------
    # DATASET OVERVIEW
    # -----------------------------------
    def overview(self):

        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "missing_values": int(self.df.isnull().sum().sum()),
            "duplicates": int(self.df.duplicated().sum())
        }

    # -----------------------------------
    # COLUMN TYPES
    # -----------------------------------
    def column_types(self):

        numeric = list(
            self.df.select_dtypes(include="number").columns
        )

        categorical = list(
            self.df.select_dtypes(include="object").columns
        )

        datetime = list(
            self.df.select_dtypes(include="datetime").columns
        )

        return {
            "numeric": numeric,
            "categorical": categorical,
            "datetime": datetime
        }

    # -----------------------------------
    # NUMERIC SUMMARY
    # -----------------------------------
    def numeric_summary(self):

        numeric_df = self.df.select_dtypes(include="number")

        summary = {}

        for col in numeric_df.columns:

            summary[col] = {
                "mean": float(numeric_df[col].mean()),
                "median": float(numeric_df[col].median()),
                "std": float(numeric_df[col].std()),
                "min": float(numeric_df[col].min()),
                "max": float(numeric_df[col].max()),
                "missing": int(numeric_df[col].isnull().sum()),
                "skewness": float(numeric_df[col].skew())
            }

        return summary

    # -----------------------------------
    # MISSING VALUES
    # -----------------------------------
    def missing_analysis(self):

        missing = self.df.isnull().sum()

        total = len(self.df)

        result = {}

        for col in self.df.columns:

            result[col] = {
                "missing_count": int(missing[col]),
                "missing_percent": round(
                    (missing[col] / total) * 100,
                    2
                )
            }

        return result

    # -----------------------------------
    # CORRELATION MATRIX
    # -----------------------------------
    def correlations(self):

        corr = self.df.corr(numeric_only=True)

        return corr.round(3).to_dict()

    # -----------------------------------
    # TOP CORRELATIONS
    # -----------------------------------
    def top_correlations(self):

        corr = self.df.corr(numeric_only=True)

        corr_pairs = []

        cols = corr.columns

        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):

                val = corr.iloc[i, j]

                corr_pairs.append({
                    "x": cols[i],
                    "y": cols[j],
                    "corr": round(float(val), 3)
                })

        corr_pairs = sorted(
            corr_pairs,
            key=lambda x: abs(x["corr"]),
            reverse=True
        )

        return corr_pairs[:10]