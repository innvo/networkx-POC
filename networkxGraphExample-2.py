import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import numpy as np

node_count = 10
# Generate a list of random node IDs
node_ids = list(range(1, node_count + 1))

# Generate a list of random node types
node_types = np.random.choice(['person', 'address', 'receipt'], node_count)

# Generate a list of random node names
node_names = ['Node ' + str(i) for i in range(1, node_count + 1)]

# Create a DataFrame for the nodes data
nodes_data = pd.DataFrame({
    'id': node_ids,
    'node_type': node_types,
    'node_name': node_names
})

# Generate a list of random source nodes for the edges
edge_src = random.choices(node_ids, k=node_count)

# Generate a list of random destination nodes for the edges
edge_dst = random.choices(node_ids, k=node_count)

# Generate a list of random edge types
edge_types = np.random.choice(['person_address', 'person_receipt'], node_count)

# Generate a list of 50 random source nodes for the edges
edge_src = random.choices(node_ids, k=50)

# Generate a list of 50 random destination nodes for the edges
edge_dst = random.choices(node_ids, k=50)

# Generate a list of 50 random edge types
edge_types = np.random.choice(['person_address', 'person_receipt'], 50)

# Create a DataFrame for the edges data
edges_data = pd.DataFrame({
    'src': edge_src,
    'dst': edge_dst,
    'edge_type': edge_types
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

# Create a node size list
node_size = [10000 / len(G.nodes) for _ in G.nodes]
# Create a node size dictionary
node_size_dict = {node: size for node, size in zip(G.nodes, node_size)}
print(node_size)

# Create a node color map
color_map = {'person': 'red', 'address': 'green', 'receipt': 'yellow'}
colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes]

# Create a node labels dictionary
# labels = {node: f"{G.nodes[node]['node_name'][:10]} ({G.degree(node)})" for node in G.nodes}
labels = {node: G.nodes[node]['node_name'] if size >= 250 else '' for node, size in zip(G.nodes, node_size)}

# Create an edge color map
edge_color_map = {'person_address': 'orange', 'person_receipt': 'blue'}
edge_colors = [edge_color_map[G.edges[edge]['edge_type']] for edge in G.edges]

# Create an edge labels dictionary
# edge_labels = {(u, v): G.edges[u, v]['edge_type'] for u, v in G.edges}
edge_labels = {(u, v): G.edges[u, v]['edge_type'] if node_size_dict[u] >= 250 and node_size_dict[v] >= 250 else '' for u, v in G.edges}

# Set the figure size
plt.figure(figsize=(10, 10), dpi=80)

# Adjust the top of the subplot parameters
plt.subplots_adjust(top=2.0)


# Plot the graph
nx.draw(G, pos, node_color=colors, edge_color=edge_colors, node_size=node_size,labels=labels, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Create a legend
node_legend_handles = [mpatches.Patch(color=color, label=node_type) for node_type, color in color_map.items()]
edge_legend_handles = [mpatches.Patch(color=color, label=edge_type) for edge_type, color in edge_color_map.items()]

plt.legend(handles=node_legend_handles + edge_legend_handles, loc='upper left')

# Add a title (acting as subtitle)
plt.title('Subtitle Here') ## THIS IS NOT WORKING

# Add a suptitle (acting as main title)
plt.suptitle('Example Network Graph', weight='bold', fontsize='16')
# Get the current axes
ax = plt.gca()

# Get the range of the axes
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Add a border
plt.plot([xlim[0], xlim[0], xlim[1], xlim[1], xlim[0]], [ylim[0], ylim[1], ylim[1], ylim[0], ylim[0]], color='black')


plt.show()

