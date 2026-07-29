import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
lines_df = pd.read_csv(os.path.join(BASE_DIR, "lines.csv"))

print("=== TRANSMISSION LINES ANALYSIS ===")

# 1. Total & Average Capacity
total_capacity = lines_df["capacity_mw"].sum()
avg_capacity = lines_df["capacity_mw"].mean()
print(f"Total Grid Capacity: {total_capacity:,} MW")
print(f"Average Line Capacity: {avg_capacity:.2f} MW\n")

# 2. Voltage Breakdown
print("--- Breakdown by Voltage Level (kV) ---")
voltage_counts = lines_df["voltage_kv"].value_counts()
print(voltage_counts)

# 3. Highest Capacity Lines (Bottlenecks / Critical Paths)
print("\n--- Top 3 Highest Capacity Lines ---")
top_lines = lines_df.sort_values(by="capacity_mw", ascending=False).head(3)
print(top_lines[["line_id", "source_substation_id", "target_substation_id", "capacity_mw"]])