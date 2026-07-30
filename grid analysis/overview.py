"""
Overview Pipeline for Component 1: National Electricity Grid Analysis
This script runs the complete grid analysis pipeline:
1. Loads datasets and prints high-level summary statistics.
2. Identifies critical single-point failures (N-1 Contingency Analysis).
3. Generates the interactive geospatial map.
"""

import pandas as pd
from contingency_analysis import build_grid_graph, run_n_minus_one_contingency
from grid_visualization import create_interactive_grid_map


def run_full_grid_analysis():
    print("==================================================")
    print("   NATIONAL ELECTRICITY GRID ANALYSIS PIPELINE    ")
    print("==================================================\n")
    
    
    # Step 1: Summary Statistics of the Grid Data
  
    print("Step 1: Loading raw datasets...")
    df_substations = pd.read_csv('substations.csv')
    df_lines = pd.read_csv('lines.csv')
    df_utilities = pd.read_csv('utilities.csv')
    
    total_power_capacity = df_substations['capacity_mw'].sum() if 'capacity_mw' in df_substations else 0
    
    print(f"  • Total Utilities Monitored: {len(df_utilities)}")
    print(f"  • Total Substations Active: {len(df_substations)}")
    print(f"  • Total Transmission Lines: {len(df_lines)}")
    print(f"  • Total Installed Capacity: {total_power_capacity:,.2f} MW\n")
    
    # Step 2: Build Network Graph & Perform N-1 Analysis
   
    print("Step 2: Building graph model and running resilience checks...")
    grid_graph = build_grid_graph('substations.csv', 'lines.csv')
    critical_lines, critical_substations = run_n_minus_one_contingency(grid_graph)
    
    print(f"\nResilience Summary:")
    print(f"  • Vulnerable Transmission Lines: {len(critical_lines)}")
    print(f"  • Vulnerable Substations: {len(critical_substations)}\n")
    
    
    # Step 3: Generate Visualizations
   
    print("Step 3: Generating interactive geospatial map...")
    create_interactive_grid_map('substations.csv', 'lines.csv')
    
    print("\n==================================================")
    print(" Pipeline Execution Complete! Check 'interactive_grid_map.html'")
    print("==================================================")


if __name__ == "__main__":
    run_full_grid_analysis()
