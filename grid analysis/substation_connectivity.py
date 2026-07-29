import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

lines_df = pd.read_csv(os.path.join(BASE_DIR, "lines.csv"))
substations_df = pd.read_csv(os.path.join(BASE_DIR, "substations.csv"))

print("=== SUBSTATION NETWORK CONNECTIVITY ===")

# 1. Count outgoing and incoming lines per substation
outgoing = lines_df['source_substation_id'].value_counts()
incoming = lines_df['target_substation_id'].value_counts()

# 2. Combine line counts into a single summary table
connectivity_df = pd.concat([outgoing, incoming], axis=1, keys=['outgoing_lines', 'incoming_lines']).fillna(0)
connectivity_df['total_connections'] = connectivity_df['outgoing_lines'] + connectivity_df['incoming_lines']

# 3. Merge with substation names
hub_summary = substations_df.merge(
    connectivity_df, 
    left_on='substation_id', 
    right_index=True, 
    how='left'
).fillna(0)

# Clean up data types for display
count_cols = ['outgoing_lines', 'incoming_lines', 'total_connections']
hub_summary[count_cols] = hub_summary[count_cols].astype(int)

# 4. Display the top grid hubs
top_hubs = hub_summary.sort_values(by='total_connections', ascending=False)

print("\n--- Top Grid Hubs (Most Connected Substations) ---")
print(top_hubs[['substation_id', 'substation_name', 'total_connections', 'status']].head(5))