class Visualizer:
    
    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df.to_json(orient="records")

    def get_columns(self):
        return list(self.df.columns)