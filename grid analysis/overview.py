"""
Overview Pipeline for Component 1: National Electricity Grid Analysis
This script runs the complete grid analysis pipeline:
1. Loads datasets and prints high-level summary statistics.
2. Identifies critical single-point failures (N-1 Contingency Analysis).
3. Generates the interactive geospatial map.
"""

import sys
from pathlib import Path
import pandas as pd

# Setup absolute paths so imports and CSVs work from any execution directory
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

for directory in [SCRIPT_DIR, PROJECT_ROOT]:
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

# Dynamic imports with fallback checks across module files
try:
    from network_builder import build_grid_graph
except ImportError:
    from grid_network_analysis import build_grid_graph

try:
    from grid_network_analysis import run_n_minus_one_contingency
except ImportError:
    from network_builder import run_n_minus_one_contingency

try:
    from grid_visualization import create_interactive_grid_map
except ImportError:
    create_interactive_grid_map = None


def run_full_grid_analysis():
    print("==================================================")
    print("   NATIONAL ELECTRICITY GRID ANALYSIS PIPELINE   ")
    print("==================================================\n")

    # Step 1: Summary Statistics of the Grid Data
    print("Step 1: Loading raw datasets...")
    
    substations_file = SCRIPT_DIR / 'substations.csv'
    lines_file = SCRIPT_DIR / 'lines.csv'
    utilities_file = SCRIPT_DIR / 'utilities.csv'

    df_substations = pd.read_csv(substations_file)
    df_lines = pd.read_csv(lines_file)
    df_utilities = pd.read_csv(utilities_file)

    total_power_capacity = (
        df_substations['capacity_mw'].sum() 
        if 'capacity_mw' in df_substations.columns 
        else 0.0
    )

    print(f" • Total Utilities Monitored: {len(df_utilities)}")
    print(f" • Total Substations Active:  {len(df_substations)}")
    print(f" • Total Transmission Lines: {len(df_lines)}")
    print(f" • Total Installed Capacity: {total_power_capacity:,.2f} MW\n")

    # Step 2: Build Network Graph & Perform N-1 Analysis
    print("Step 2: Building graph model and running resilience checks...")
    grid = build_grid_graph()
    run_n_minus_one_contingency(grid)

    # Step 3: Interactive Geospatial Visualization
    if create_interactive_grid_map:
        print("\nStep 3: Generating interactive grid map...")
        create_interactive_grid_map()
    
    print("\n==================================================")
    print("Grid Analysis Pipeline completed successfully!")


if __name__ == "__main__":
    run_full_grid_analysis()