import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
substations_df = pd.read_csv(os.path.join(BASE_DIR, "substations.csv"))

print("=== SUBSTATIONS ANALYSIS ===")

# 1. Operational Status Distribution
print("--- Breakdown by Operational Status ---")
status_counts = substations_df["status"].value_counts()
print(status_counts)

# 2. Substations per Utility Provider
print("\n--- Substation Count by Utility ID ---")
utility_counts = substations_df["utility_id"].value_counts()
print(utility_counts)

# 3. Geographic Footprint 
print("\n--- Geographic Bounds ---")
print(f"Latitude Range : {substations_df['latitude'].min():.4f} to {substations_df['latitude'].max():.4f}")
print(f"Longitude Range: {substations_df['longitude'].min():.4f} to {substations_df['longitude'].max():.4f}")