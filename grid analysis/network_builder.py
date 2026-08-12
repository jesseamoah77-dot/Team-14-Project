"""
network_builder.py
GridCare - Power Grid Network Topology & Resilience Analysis

Builds a NetworkX graph representation of the power grid from CSV data
and performs N-1 contingency analysis to identify single points of failure.
"""

from pathlib import Path
import pandas as pd
import networkx as nx


def find_data_file(filename: str) -> Path:
    """Dynamically locates a dataset file across common project directories."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    candidates = [
        script_dir / filename,
        script_dir / filename.capitalize(),
        project_root / filename,
        project_root / filename.capitalize(),
        project_root / "gridcare" / filename,
        project_root / "gridcare" / filename.capitalize(),
    ]

    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"Could not locate '{filename}'. Verified search paths:\n"
        + "\n".join(f" - {p}" for p in candidates[:3])
    )


def get_column(df: pd.DataFrame, possible_names: list, default=None):
    """Finds the first matching column name from a list of possibilities."""
    for name in possible_names:
        if name in df.columns:
            return name
    return default


def build_grid_graph(substations_file='substations.csv', lines_file='lines.csv') -> nx.Graph:
    """Reads CSVs and builds a NetworkX graph of the power grid."""
    substations_path = find_data_file(substations_file)
    lines_path = find_data_file(lines_file)

    print("Loading grid datasets...")
    print(f" • Substations: {substations_path.name}")
    print(f" • Transmission Lines: {lines_path.name}")

    df_substations = pd.read_csv(substations_path)
    df_lines = pd.read_csv(lines_path)

    # Standardize column headers (strip spaces, lowercase)
    df_substations.columns = df_substations.columns.str.strip().str.lower()
    df_lines.columns = df_lines.columns.str.strip().str.lower()

    # Detect key columns for transmission lines
    source_col = get_column(
        df_lines, 
        ['source_substation_id', 'source_id', 'source', 'from_id', 'from', 'substation_a', 'start_node']
    )
    target_col = get_column(
        df_lines, 
        ['target_substation_id', 'target_id', 'target', 'to_id', 'to', 'substation_b', 'end_node']
    )

    if not source_col or not target_col:
        raise KeyError(
            f"Could not find source/target columns in '{lines_path.name}'. "
            f"Found columns: {list(df_lines.columns)}"
        )

    G = nx.Graph()

    # 1. Add Substation Nodes
    node_id_col = get_column(df_substations, ['substation_id', 'id', 'node_id'], default='id')
    
    for _, row in df_substations.iterrows():
        node_id = row[node_id_col]
        G.add_node(
            node_id,
            name=row.get('name', f"Substation_{node_id}"),
            lat=row.get('latitude', row.get('lat', 0.0)),
            lon=row.get('longitude', row.get('lon', 0.0)),
            capacity_mw=row.get('capacity_mw', row.get('capacity', 0))
        )

    # 2. Add Transmission Line Edges
    for _, row in df_lines.iterrows():
        u = row[source_col]
        v = row[target_col]
        G.add_edge(
            u,
            v,
            line_id=row.get('line_id', row.get('id', f"{u}-{v}")),
            voltage_kv=row.get('voltage_kv', row.get('voltage', 0)),
            max_capacity_mw=row.get('capacity_mw', row.get('max_capacity_mw', 0))
        )

    print(
        f"Graph built successfully: {G.number_of_nodes()} substations and "
        f"{G.number_of_edges()} transmission lines."
    )
    return G


def run_n_minus_one_contingency(G: nx.Graph):
    """Simulates single-component failures (N-1 Analysis)."""
    baseline_components = nx.number_connected_components(G)
    print("\n--- N-1 Contingency Resilience Analysis ---")
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
    grid = build_grid_graph()
    lines_df, substations_df = run_n_minus_one_contingency(grid)