# Graph Processing Solution

A Python-based utility to analyze directed graphs and compute structural and algorithmic properties.

## Features

- Parse directed graphs from CSV files
- Detect if a graph is a Directed Acyclic Graph (DAG)
- Calculate maximum in-degree and out-degree
- Compute PageRank scores using the Stanford PageRank algorithm
- Handle large graphs efficiently with optimized data structures

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

Clone the repository and navigate to the project directory:

```bash
cd graph_solution
chmod +x graph_solution
```

## Usage

Run the executable with a graph file as input:

```bash
./graph_solution path/to/graph.csv
```

### Input Format

The input file should be a CSV file with directed edges, one per line:

```csv
source_node_id,target_node_id
```

Example:

```csv
1,2
2,3
3,1
```

Both source and target node IDs must be non-negative integers.

### Output Format

The program outputs five metrics to standard output:

```
is_dag: true/false
max_in_degree: <integer>
max_out_degree: <integer>
pr_max: <float>
pr_min: <float>
```

Example:

```
is_dag: true
max_in_degree: 2
max_out_degree: 2
pr_max: 0.372381
pr_min: 0.135169
```

## Output Metrics Explained

- **is_dag**: Boolean indicating whether the graph is acyclic (true/false)
- **max_in_degree**: Maximum number of incoming edges to any single node
- **max_out_degree**: Maximum number of outgoing edges from any single node
- **pr_max**: Highest PageRank score across all nodes (6 decimal places)
- **pr_min**: Lowest PageRank score across all nodes (6 decimal places)

## Implementation Details

### DAG Detection

Uses depth-first search with three node states (unvisited, visiting, visited) to detect cycles. If a back edge is encountered, the graph contains a cycle.

### PageRank Algorithm

Implements the Stanford PageRank algorithm with the following parameters:

- Damping factor: 0.85
- Iterations: 20
- Sink nodes: Treated as linking to all nodes equally
- Initialization: Uniform distribution across all nodes

The transition matrix is row-stochastic (each row sums to 1).

### Performance Optimizations

- In-degrees are cached during graph construction for O(1) lookup
- Reverse adjacency lists are built for efficient PageRank computation
- Iterative PageRank computation avoids redundant operations

## Project Structure

```
graph_solution/
├── graph_solution          # Main executable script
├── graph_processor.py      # Core graph processing module
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## License

This is a systems engineering interview challenge solution.
