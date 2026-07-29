import os
import pandas as pd

# Get the folder directory where overview.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path to each CSV file
lines_path = os.path.join(BASE_DIR, "lines.csv")
substations_path = os.path.join(BASE_DIR, "substations.csv")
utilities_path = os.path.join(BASE_DIR, "utilities.csv")

# Load the datasets
lines_df = pd.read_csv(lines_path)
substations_df = pd.read_csv(substations_path)
utilities_df = pd.read_csv(utilities_path)

print("--- Lines Overview ---")
print(lines_df.info())