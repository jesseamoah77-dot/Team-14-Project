import unittest
import os
import pandas as pd
import networkx as nx
from contingency_analysis import build_grid_graph, run_n_minus_one_contingency


class TestGridAnalysis(unittest.TestCase):

    def setUp(self):
        """Runs before each test to check if raw data files exist."""
        self.substations_file = 'substations.csv'
        self.lines_file = 'lines.csv'
        
    def test_csv_files_exist(self):
        """Verify that the required data files exist in the directory."""
        self.assertTrue(os.path.exists(self.substations_file), "substations.csv is missing!")
        self.assertTrue(os.path.exists(self.lines_file), "lines.csv is missing!")

    def test_graph_creation(self):
        """Test if the network graph builds correctly with nodes and edges."""
        graph = build_grid_graph(self.substations_file, self.lines_file)
        
        # Verify graph is not empty
        self.assertGreater(graph.number_of_nodes(), 0, "Graph has no substation nodes.")
        self.assertGreater(graph.number_of_edges(), 0, "Graph has no transmission line edges.")

    def test_contingency_analysis(self):
        """Test that the N-1 contingency resilience check runs without crashing."""
        graph = build_grid_graph(self.substations_file, self.lines_file)
        critical_lines, critical_substations = run_n_minus_one_contingency(graph)
        
        # Output should be lists (can be empty if grid is 100% redundant)
        self.assertIsInstance(critical_lines, list)
        self.assertIsInstance(critical_substations, list)


if __name__ == '__main__':
    unittest.main()
