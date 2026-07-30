import pandas as pd
import networkx as nx
import plotly.graph_objects as go

def create_interactive_grid_map(substations_file='substations.csv', lines_file='lines.csv'):
    """
    Creates an interactive Plotly map showing all power substations
    and the transmission lines connecting them.
    """
    # Load the grid datasets
    print("Reading dataset files for visualization...")
    df_substations = pd.read_csv(substations_file)
    df_lines = pd.read_csv(lines_file)
    
    # -------------------------------------------------------------
    # 1. Prepare Line Coordinates (Edges)
    # -------------------------------------------------------------
    # We match source and target IDs to pull latitude & longitude coordinates
    substation_map = df_substations.set_index('substation_id')[['latitude', 'longitude']].to_dict('index')
    
    line_lats = []
    line_lons = []
    
    for _, line in df_lines.iterrows():
        src_id = line['source_id']
        tgt_id = line['target_id']
        
        # Make sure both endpoints exist before drawing the line
        if src_id in substation_map and tgt_id in substation_map:
            line_lats.extend([substation_map[src_id]['latitude'], substation_map[tgt_id]['latitude'], None])
            line_lons.extend([substation_map[src_id]['longitude'], substation_map[tgt_id]['longitude'], None])
            
    # Trace layer for the lines connecting the stations
    lines_trace = go.Scattermapbox(
        lat=line_lats,
        lon=line_lons,
        mode='lines',
        line=dict(width=2, color='#1f77b4'),  # Nice clean blue for transmission lines
        hoverinfo='none',
        name='Transmission Lines'
    )
    
    # -------------------------------------------------------------
    # 2. Prepare Substation Markers (Nodes)
    # -------------------------------------------------------------
    hover_labels = []
    for _, sub in df_substations.iterrows():
        label = (
            f"<b>Substation ID:</b> {sub['substation_id']}<br>"
            f"<b>Capacity:</b> {sub.get('capacity_mw', 'N/A')} MW<br>"
            f"<b>Status:</b> {sub.get('status', 'Active')}"
        )
        hover_labels.append(label)
        
    nodes_trace = go.Scattermapbox(
        lat=df_substations['latitude'],
        lon=df_substations['longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color='#d62728',  # Bright red markers for visibility
            opacity=0.9
        ),
        text=hover_labels,
        hoverinfo='text',
        name='Substations'
    )
    
    # -------------------------------------------------------------
    # 3. Assemble and Style the Interactive Map
    # -------------------------------------------------------------
    fig = go.Figure(data=[lines_trace, nodes_trace])
    
    # Center map on average lat/lon coordinates
    avg_lat = df_substations['latitude'].mean()
    avg_lon = df_substations['longitude'].mean()
    
    fig.update_layout(
        title="<b>National Electricity Grid Network Map</b>",
        mapbox=dict(
            style="open-street-map",  # Clean, open-source base map
            center=dict(lat=avg_lat, lon=avg_lon),
            zoom=6
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True
    )
    
    # Save output to an HTML file so anyone can double-click and open it in a browser
    output_filename = "interactive_grid_map.html"
    fig.write_html(output_filename)
    print(f"Map successfully generated and saved as '{output_filename}'!")

if __name__ == "__main__":
    create_interactive_grid_map()
