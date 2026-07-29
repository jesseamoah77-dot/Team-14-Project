import os
import pandas as pd

# Get the folder directory where overview.py is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load the CSV files into variables first
lines_df = pd.read_csv(os.path.join(BASE_DIR, "lines.csv"))
substations_df = pd.read_csv(os.path.join(BASE_DIR, "substations.csv"))
utilities_df = pd.read_csv(os.path.join(BASE_DIR, "utilities.csv"))

# 2. Now you can safely inspect them
print("--- Datasets Shape ---")
print(f"Lines: {lines_df.shape}")
print(f"Substations: {substations_df.shape}")
print(f"Utilities: {utilities_df.shape}\n")

print("--- Lines First 5 Rows ---")
<<<<<<< HEAD
print(lines_df.head())
=======
print(lines_df.head())
>>>>>>> c646667d34677ac6990df10386b271456a0cfaab
