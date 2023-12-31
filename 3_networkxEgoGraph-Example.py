import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import numpy as np
import scipy

# Hardcoded edges and nodes data
edges_data = pd.DataFrame({
    'src': ['A', 'A','B'],
    'dst': ['B', 'C', 'D'],
    'edge_type': ['person_address', 'person_receipt','address_person']
})

nodes_data = pd.DataFrame({
    'id': ['A','B','C','D'],
    'node_type': ['person', 'address', 'receipt','person'],
    'node_name': ['ERIC', '123 MAIN ST', 'R12345','DENISE']
})

node_count=25
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

#print((edges_data))

# Create a networkx graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for _, row in nodes_data.iterrows():
    G.add_node(row['id'], node_type=row['node_type'], node_name=row['node_name'])

for _, row in edges_data.iterrows():
    G.add_edge(row['src'], row['dst'], edge_type=row['edge_type'])

# Choose a node for the ego graph
edges_array = edges_data.values
ego_node = edges_array[10,0] # r0eplace with the ID of the node you want to focus on

# Choose a radius for the ego graph
radius = 5  # replace with the desired radius

# Generate the ego graph
ego_G = nx.ego_graph(G, ego_node, radius=radius)

# Generate a layout for the ego graph
ego_pos = nx.spring_layout(ego_G)

# Create a node color map for the ego graph
color_map = {'person': 'red', 'address': 'green', 'receipt': 'yellow'}
ego_node_colors = [color_map[ego_G.nodes[node]['node_type']] for node in ego_G.nodes]

# Set the color of the ego node to purple
ego_node_colors[list(ego_G.nodes).index(ego_node)] = 'purple'

# Create a node size list
ego_node_size = [25000 / len(ego_G.nodes) for _ in ego_G.nodes]
# Create a node size dictionary
ego_node_size_dict = {node: size for node, size in zip(ego_G.nodes, ego_node_size)}
#print(ego_node_size)
print(ego_node_size_dict)

# Create a node labels dictionary for the ego graph
#ego_labels = {node: ego_G.nodes[node]['node_name'] for node in ego_G.nodes}
ego_node_labels = {node: ego_G.nodes[node]['node_name'] if size >= 250 else '' for node,size in zip(ego_G.nodes, ego_node_size)}

# Create an edge color map for the ego graph
edge_color_map = {'person_address': 'orange', 'person_receipt': 'blue', 'address_person': 'purple'}
ego_edge_colors = [edge_color_map[ego_G.edges[edge]['edge_type']] for edge in ego_G.edges]


# Create an edge labels dictionary
# edge_labels = {(u, v): G.edges[u, v]['edge_type'] for u, v in G.edges}
ego_edge_labels = {(u, v): ego_G.edges[u, v]['edge_type'] if ego_node_size_dict[u] >= 1000 and ego_node_size_dict[v] >= 1000 else '' for u, v in ego_G.edges}

# Set the figure size
plt.figure(figsize=(10, 10), dpi=80)

# Adjust the top of the subplot parameters
plt.subplots_adjust(top=2.0)

# Plot the ego graph
nx.draw(ego_G, ego_pos, node_color=ego_node_colors, edge_color=ego_edge_colors, with_labels=True, labels=ego_node_labels)
nx.draw_networkx_edge_labels(ego_G, ego_pos, edge_labels=ego_edge_labels)

# Create a legend
node_legend_handles = [mpatches.Patch(color=color, label=node_type) for node_type, color in color_map.items()]
edge_legend_handles = [mpatches.Patch(color=color, label=edge_type) for edge_type, color in edge_color_map.items()]

plt.legend(handles=node_legend_handles + edge_legend_handles, loc='upper left')

# Add a title (acting as subtitle)
plt.title('Subtitle Here') ## THIS IS NOT WORKING

# Add a suptitle (acting as main title)
plt.suptitle('Example Network Ego Graph', weight='bold', fontsize='16')
# Get the current axes
ax = plt.gca()

# Get the range of the axes
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Add a border
plt.plot([xlim[0], xlim[0], xlim[1], xlim[1], xlim[0]], [ylim[0], ylim[1], ylim[1], ylim[0], ylim[0]], color='black')

# Plot the graph
plt.show()

