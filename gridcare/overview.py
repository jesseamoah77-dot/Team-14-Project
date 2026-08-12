"""
overview.py
GridCare - Grid Topology & Contingency Overview

Generates high-level statistical summaries and runs N-1 contingency analysis
from the grid network dataset.
"""

import sys
from pathlib import Path

# Automatically add script directory and project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

for path in [SCRIPT_DIR, PROJECT_ROOT, PROJECT_ROOT / "grid analysis", PROJECT_ROOT / "gridcare"]:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

import pandas as pd
import networkx as nx

# Import functions from network_builder (replaces old contingency_analysis module)
from network_builder import build_grid_graph, run_n_minus_one_contingency, find_data_file


def print_grid_overview():
    print("=" * 60)
    print("           GRIDCARE POWER GRID OVERVIEW & ANALYTICS          ")
    print("=" * 60)

    # 1. Dataset File Checks & Summaries
    try:
        substations_path = find_data_file('substations.csv')
        lines_path = find_data_file('lines.csv')

        df_substations = pd.read_csv(substations_path)
        df_lines = pd.read_csv(lines_path)

        print(f"\n[Dataset Statistics]")
        print(f" • Total Substations Registered: {len(df_substations)}")
        print(f" • Total Transmission Lines:    {len(df_lines)}")

        if 'capacity_mw' in df_substations.columns:
            total_substation_cap = df_substations['capacity_mw'].sum()
            print(f" • Total Substation Capacity:  {total_substation_cap:,.2f} MW")

        if 'capacity_mw' in df_lines.columns:
            total_line_cap = df_lines['capacity_mw'].sum()
            print(f" • Total Line Capacity:        {total_line_cap:,.2f} MW")

    except FileNotFoundError as e:
        print(f"\n[Error] {e}")
        return

    # 2. Network Graph Analysis
    print("\n[Network Topology & Resilience Analysis]")
    grid = build_grid_graph()
    
    # 3. N-1 Contingency Failure Run
    lines_df, substations_df = run_n_minus_one_contingency(grid)

    print("\n" + "=" * 60)
    print("Overview complete.")


if __name__ == "__main__":
    print_grid_overview()