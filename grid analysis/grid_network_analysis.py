import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load datasets
lines_df = pd.read_csv(os.path.join(BASE_DIR, "lines.csv"))
substations_df = pd.read_csv(os.path.join(BASE_DIR, "substations.csv"))

print("=== COMBINED GRID NETWORK ANALYSIS ===")

# 1. Merge lines with substations for SOURCE station info
merged_df = lines_df.merge(
    substations_df[['substation_id', 'substation_name', 'status']], 
    left_on='source_substation_id', 
    right_on='substation_id', 
    how='left'
).rename(columns={'substation_name': 'source_name', 'status': 'source_status'}).drop(columns=['substation_id'])

# 2. Merge again for TARGET station info
merged_df = merged_df.merge(
    substations_df[['substation_id', 'substation_name', 'status']], 
    left_on='target_substation_id', 
    right_on='substation_id', 
    how='left'
).rename(columns={'substation_name': 'target_name', 'status': 'target_status'}).drop(columns=['substation_id'])

# 3. View transmission lines with real station names
print("\n--- Transmission Connections ---")
print(merged_df[['line_id', 'source_name', 'target_name', 'capacity_mw', 'voltage_kv']].head())
