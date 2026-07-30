import pandas as pd
import networkx as nx

def build_grid_graph(substations_file='substations.csv', lines_file='lines.csv'):
    """Reads CSVs and builds a NetworkX graph of the power grid."""
    print("Loading grid datasets...")
    df_substations = pd.read_csv(substations_file)
    df_lines = pd.read_csv(lines_file)
    
    G = nx.Graph()
    
    # 1. Add Substation Nodes
    for _, row in df_substations.iterrows():
        # Using get() to handle optional columns safely
        node_id = row['substation_id'] if 'substation_id' in row else row['id']
        G.add_node(
            node_id,
            name=row.get('name', f"Substation_{node_id}"),
            lat=row.get('latitude', 0.0),
            lon=row.get('longitude', 0.0),
            capacity_mw=row.get('capacity_mw', 0)
        )
        
    # 2. Add Transmission Line Edges
    for _, row in df_lines.iterrows():
        G.add_edge(
            row['source_id'],
            row['target_id'],
            line_id=row.get('line_id', f"{row['source_id']}-{row['target_id']}"),
            voltage_kv=row.get('voltage_kv', 0),
            max_capacity_mw=row.get('max_capacity_mw', 0)
        )
        
    print(f"Graph built successfully with {G.number_of_nodes()} substations and {G.number_of_edges()} transmission lines.")
    return G


def run_n_minus_one_contingency(G):
    """
    Simulates single-component failures (N-1 Analysis) 
    to find single points of failure in the grid network.
    """
    baseline_components = nx.number_connected_components(G)
    print(f"\n--- N-1 Contingency Resilience Analysis ---")
    print(f"Baseline connected components: {baseline_components}")
    
    critical_lines = []
    critical_substations = []
    
    # Test Line (Edge) Failures
    for u, v, data in G.edges(data=True):
        G_temp = G.copy()
        G_temp.remove_edge(u, v)
        new_comp_count = nx.number_connected_components(G_temp)
        
        if new_comp_count > baseline_components:
            critical_lines.append({
                'line_id': data.get('line_id', f"{u}-{v}"),
                'source': u,
                'target': v,
                'resulting_components': new_comp_count
            })
            
    # Test Substation (Node) Failures
    for node in G.nodes():
        G_temp = G.copy()
        G_temp.remove_node(node)
        new_comp_count = nx.number_connected_components(G_temp)
        
        if new_comp_count > baseline_components:
            critical_substations.append({
                'substation_id': node,
                'resulting_components': new_comp_count
            })
            
    # Display Results
    print(f"\nFound {len(critical_lines)} critical transmission line(s) (Single Points of Failure):")
    for line in critical_lines:
        print(f"  • Line {line['line_id']} ({line['source']} <-> {line['target']}): Split grid into {line['resulting_components']} components.")
        
    print(f"\nFound {len(critical_substations)} critical substation(s):")
    for sub in critical_substations:
        print(f"  • Substation {sub['substation_id']}: Split grid into {sub['resulting_components']} components.")
        
    return pd.DataFrame(critical_lines), pd.DataFrame(critical_substations)


if __name__ == "__main__":
    # Execute graph pipeline
    grid = build_grid_graph()
    lines_df, substations_df = run_n_minus_one_contingency(grid)
