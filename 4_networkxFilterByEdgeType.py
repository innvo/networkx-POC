import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Your data
edges_data = pd.DataFrame({
    'src': ['A', 'A', 'A'],
    'dst': ['B', 'C', 'D'],
    'edge_type': ['person_address', 'person_receipt', 'person_address'],
    'role': ['', 'attorney', '']
})
0

nodes_data = pd.DataFrame({
    'id': ['A','B','C','D'],
    'node_type': ['person', 'address', 'receipt','address'],
    'node_name': ['ERIC', '123 MAIN ST', 'R12345', '123 MAIN STREET'],
    'receipt_payment_date': ['', '', '2023-12-05', '']
})

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for _, row in nodes_data.iterrows():
    G.add_node(row['id'], node_type=row['node_type'], node_name=row['node_name'], receipt_payment_date=row['receipt_payment_date'])

for _, row in edges_data.iterrows():
    G.add_edge(row['src'], row['dst'], edge_type=row['edge_type'], role=row['role'])

# Get unique edge types
unique_edge_types = edges_data['edge_type'].unique()

# Ask user to select edge types to display
print("Select the edge types to display (separated by commas):")
for i, edge_type in enumerate(unique_edge_types):
    print(f"{i}: {edge_type}")

selected_edge_types_indices = input("Enter the numbers corresponding to the edge types: ")
selected_edge_types_indices = list(map(int, selected_edge_types_indices.split(',')))

# Get the selected edge types
selected_edge_types = [unique_edge_types[i] for i in selected_edge_types_indices]

# Filter the edges to display
edges_to_display = [(u, v) for u, v in G.edges if G.edges[u, v]['edge_type'] in selected_edge_types]

# Create a set of nodes to display, including all nodes in the selected edges
nodes_to_display = set()
for edge in edges_to_display:
    nodes_to_display.add(edge[0])
    nodes_to_display.add(edge[1])

# Draw the graph
nx.draw(G, with_labels=True, nodelist=nodes_to_display, edgelist=edges_to_display)

plt.show()