import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
utilities_df = pd.read_csv(os.path.join(BASE_DIR, "utilities.csv"))

print("=== UTILITIES OVERVIEW ===")
print(utilities_df.head())