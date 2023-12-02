import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Hardcoded edges and nodes data
edges_data = pd.DataFrame({
    'src': ['A', 'A'],
    'dst': ['B', 'C'],
    'edge_type': ['person_address', 'person_receipt']
})

nodes_data = pd.DataFrame({
    'id': ['A','B','C'],
    'node_type': ['person', 'address', 'receipt'],
    'node_name': ['ERIC', '123 MAIN ST', 'R12345']
})

# Create a networkx graph
G = nx.Graph()

# Add nodes and edges to the graph
for _, row in nodes_data.iterrows():
    G.add_node(row['id'], node_type=row['node_type'], node_name=row['node_name'])

for _, row in edges_data.iterrows():
    G.add_edge(row['src'], row['dst'], edge_type=row['edge_type'])

# Generate a layout for the graph
pos = nx.spring_layout(G)

# Create a node color map
color_map = {'person': 'red', 'address': 'green', 'receipt': 'yellow'}
colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes]

# Create a node labels dictionary
labels = {node: f"{G.nodes[node]['node_name'][:10]} ({G.degree(node)})" for node in G.nodes}

# Create an edge color map
edge_color_map = {'person_address': 'orange', 'person_receipt': 'blue'}
edge_colors = [edge_color_map[G.edges[edge]['edge_type']] for edge in G.edges]

# Create an edge labels dictionary
edge_labels = {(u, v): G.edges[u, v]['edge_type'] for u, v in G.edges}

# Plot the graph
nx.draw(G, pos, node_color=colors, edge_color=edge_colors, labels=labels, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Create a legend
legend_handles = [mpatches.Patch(color=color, label=node_type) for node_type, color in color_map.items()]
plt.legend(handles=legend_handles)

plt.show()

