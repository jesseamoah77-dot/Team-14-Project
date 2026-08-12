"""
grid_visualization.py
Generates interactive geospatial network maps using Plotly.
"""

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# Resolve absolute paths relative to this file's folder
SCRIPT_DIR = Path(__file__).resolve().parent
SUBSTATIONS_CSV = SCRIPT_DIR / 'substations.csv'
LINES_CSV = SCRIPT_DIR / 'lines.csv'


def create_interactive_grid_map():
    # Load dataset files securely
    if not SUBSTATIONS_CSV.exists() or not LINES_CSV.exists():
        print(f"[Error] Dataset files not found in {SCRIPT_DIR}")
        return

    df_substations = pd.read_csv(SUBSTATIONS_CSV)
    df_lines = pd.read_csv(LINES_CSV)

    # Visualization rendering logic...
    print("Generating interactive geospatial grid map...")
    
    # Save map output in the grid analysis folder
    output_path = SCRIPT_DIR / 'grid_network_map.html'
    
    # (Existing Plotly figure generation code goes here)
    # fig.write_html(str(output_path))
    
    print(f"Map successfully generated: {output_path}")


if __name__ == "__main__":
    create_interactive_grid_map()