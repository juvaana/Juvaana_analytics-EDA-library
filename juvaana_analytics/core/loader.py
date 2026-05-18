import pandas as pd

class DataLoader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_csv(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print("[SUCCESS] Data loaded successfully")
            return self.df
        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    def get_df(self):
        return self.df