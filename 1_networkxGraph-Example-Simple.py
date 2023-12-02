import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Hardcoded edges and nodes data
edges_data = pd.DataFrame({
    'src': ['A', 'A'],
    'dst': ['B', 'C'],
    'edge_type': ['person_address', 'person_receipt'],
    'role': ['', 'attorney']
})

nodes_data = pd.DataFrame({
    'id': ['A','B','C'],
    'node_type': ['person', 'address', 'receipt'],
    'node_name': ['ERIC', '123 MAIN ST', 'R12345']
})

# Create a networkx graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for _, row in nodes_data.iterrows():
    G.add_node(row['id'], node_type=row['node_type'], node_name=row['node_name'])

for _, row in edges_data.iterrows():
    G.add_edge(row['src'], row['dst'], edge_type=row['edge_type'], role=row['role'])

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
#edge_labels = {(u, v): G.edges[u, v]['edge_type'] for u, v in G.edges}
# edge_labels = {(u, v): G.edges[u, v]['role'] if G.edges[u, v]['edge_type'] == 'person_receipt' and G.edges[u, v]['role'] == 'attorney' else G.edges[u, v]['edge_type'] for u, v in G.edges}
# Create an edge labels dictionary
edge_labels = {(u, v): "Role: " + G.edges[u, v]['role'] if G.edges[u, v]['edge_type'] == 'person_receipt' and G.edges[u, v]['role'] == 'attorney' else G.edges[u, v]['edge_type'] for u, v in G.edges}
# Set the figure size
plt.figure(figsize=(10, 10), dpi=80)

# Adjust the top of the subplot parameters
plt.subplots_adjust(top=2.0)

# Create a node size list
node_size = [10000 / len(G.nodes) for _ in G.nodes]
print(node_size)

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

