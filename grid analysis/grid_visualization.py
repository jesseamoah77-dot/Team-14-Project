import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load datasets
lines_df = pd.read_csv(os.path.join(BASE_DIR, "lines.csv"))
substations_df = pd.read_csv(os.path.join(BASE_DIR, "substations.csv"))

print("=== GENERATING GEOGRAPHIC GRID MAP ===")

# --- OUTLIER FILTERING ---
# Filter out substations with extreme coordinate values (e.g. typos/placeholders)
lat_q1, lat_q3 = substations_df['latitude'].quantile([0.25, 0.75])
lat_iqr = lat_q3 - lat_q1

long_q1, long_q3 = substations_df['longitude'].quantile([0.25, 0.75])
long_iqr = long_q3 - long_q1

# Keep substations within 3x IQR
valid_subs = substations_df[
    (substations_df['latitude'] >= lat_q1 - 3 * lat_iqr) &
    (substations_df['latitude'] <= lat_q3 + 3 * lat_iqr) &
    (substations_df['longitude'] >= long_q1 - 3 * long_iqr) &
    (substations_df['longitude'] <= long_q3 + 3 * long_iqr)
]

valid_ids = set(valid_subs['substation_id'])

# Initialize Graph
G = nx.Graph()

pos = {}
for _, row in valid_subs.iterrows():
    node_id = row['substation_id']
    G.add_node(node_id, name=row['substation_name'])
    pos[node_id] = (row['longitude'], row['latitude'])

# Add edges between valid substations
for _, row in lines_df.iterrows():
    src = row['source_substation_id']
    tgt = row['target_substation_id']
    if src in valid_ids and tgt in valid_ids:
        G.add_edge(src, tgt)

# Plotting
plt.figure(figsize=(10, 8))

nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue', edgecolors='navy')
nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6, edge_color='darkgray')
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

plt.title("Power Grid Map", fontsize=15)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle='--', alpha=0.4)

output_path = os.path.join(BASE_DIR, "grid_network_map.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()