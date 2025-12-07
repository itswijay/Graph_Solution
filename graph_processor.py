"""
Graph processing module for directed graph analysis.
Handles DAG detection, degree calculations, and PageRank computation.
"""

import csv
from collections import defaultdict
from typing import Set, Dict, List, Tuple


class Graph:
    """Represents a directed graph using adjacency list representation."""
    
    def __init__(self):
        """Initialize an empty graph."""
        self.adjacency = defaultdict(list)  # adjacency[u] = [v1, v2, ...]
        self.nodes = set()  # All nodes in the graph
    
    def add_edge(self, source: int, target: int) -> None:
        """Add a directed edge from source to target."""
        self.adjacency[source].append(target)
        self.nodes.add(source)
        self.nodes.add(target)
    
    def get_nodes(self) -> Set[int]:
        """Return all nodes in the graph."""
        return self.nodes
    
    def get_in_degree(self, node: int) -> int:
        """Calculate in-degree for a node (number of incoming edges)."""
        count = 0
        for neighbors in self.adjacency.values():
            count += neighbors.count(node)
        return count
    
    def get_out_degree(self, node: int) -> int:
        """Calculate out-degree for a node (number of outgoing edges)."""
        return len(self.adjacency[node])
    
    def get_max_in_degree(self) -> int:
        """Return the maximum in-degree across all nodes."""
        if not self.nodes:
            return 0
        return max(self.get_in_degree(node) for node in self.nodes)
    
    def get_max_out_degree(self) -> int:
        """Return the maximum out-degree across all nodes."""
        if not self.nodes:
            return 0
        return max(self.get_out_degree(node) for node in self.nodes)
    
    def get_adjacency_list(self, node: int) -> List[int]:
        """Return list of neighbors (outgoing edges) for a node."""
        return self.adjacency[node]


def parse_graph_from_csv(filepath: str) -> Graph:
    """
    Parse a graph from a CSV file.
    Each row should be: source_node_id,target_node_id
    """
    graph = Graph()
    try:
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    try:
                        source = int(row[0].strip())
                        target = int(row[1].strip())
                        graph.add_edge(source, target)
                    except ValueError:
                        # Skip rows with non-integer values
                        pass
    except FileNotFoundError:
        raise FileNotFoundError(f"Graph file not found: {filepath}")
    
    return graph


def is_dag(graph: Graph) -> bool:
    """
    Determine if the graph is a Directed Acyclic Graph (DAG).
    Uses DFS with three states: unvisited (0), visiting (1), visited (2).
    Returns True if no cycles are found, False otherwise.
    """
    # States: 0 = unvisited, 1 = visiting (in current DFS path), 2 = visited (done)
    state = {node: 0 for node in graph.get_nodes()}
    
    def has_cycle_dfs(node: int) -> bool:
        """DFS helper to detect cycles."""
        if state[node] == 1:
            # Found a back edge (cycle)
            return True
        if state[node] == 2:
            # Already fully processed
            return False
        
        # Mark as visiting
        state[node] = 1
        
        # Check all neighbors
        for neighbor in graph.get_adjacency_list(node):
            if neighbor not in state:
                # Isolated node encountered during edge traversal
                state[neighbor] = 0
            if has_cycle_dfs(neighbor):
                return True
        
        # Mark as visited
        state[node] = 2
        return False
    
    # Run DFS from all unvisited nodes
    for node in graph.get_nodes():
        if state[node] == 0:
            if has_cycle_dfs(node):
                return False
    
    return True


def compute_pagerank(graph: Graph, damping_factor: float = 0.85, iterations: int = 20) -> Tuple[float, float]:
    """
    Compute PageRank for all nodes in the graph.
    
    Args:
        graph: The input graph
        damping_factor: Damping factor (default 0.85)
        iterations: Number of iterations (default 20)
    
    Returns:
        Tuple of (max_pagerank, min_pagerank)
    """
    nodes = list(graph.get_nodes())
    if not nodes:
        return 0.0, 0.0
    
    n = len(nodes)
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    
    # Initialize PageRank uniformly
    pagerank = [1.0 / n for _ in range(n)]
    
    # Identify sink nodes (nodes with no outgoing edges)
    sink_nodes = set()
    for node in nodes:
        if graph.get_out_degree(node) == 0:
            sink_nodes.add(node)
    
    # PageRank iteration
    for _ in range(iterations):
        new_pagerank = [0.0] * n
        
        # Calculate contribution from sinks
        sink_contribution = 0.0
        if sink_nodes:
            for sink_node in sink_nodes:
                sink_idx = node_to_idx[sink_node]
                sink_contribution += pagerank[sink_idx]
            sink_contribution /= n
        
        # For each node, calculate new PageRank
        for node in nodes:
            node_idx = node_to_idx[node]
            
            # Contribution from sink nodes
            rank = sink_contribution
            
            # Contribution from non-sink nodes that link to this node
            for source_node in nodes:
                source_idx = node_to_idx[source_node]
                out_degree = graph.get_out_degree(source_node)
                
                if out_degree > 0 and node in graph.get_adjacency_list(source_node):
                    rank += pagerank[source_idx] / out_degree
            
            # Apply damping factor and teleportation
            new_pagerank[node_idx] = (1.0 - damping_factor) / n + damping_factor * rank
        
        pagerank = new_pagerank
    
    max_pr = max(pagerank)
    min_pr = min(pagerank)
    
    return max_pr, min_pr
