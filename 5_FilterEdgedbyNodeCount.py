import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

max_edges_edge_type = 2

# Your data
edges_data = pd.DataFrame({
    'src': ['A', 'A', 'A'],
    'dst': ['B', 'C', 'D'],
    'edge_type': ['person_address', 'person_receipt', 'person_address'],
    'role': ['', 'attorney', '']
})

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

# # Check for nodes with count > 2
# node_counts = edges_data['src'].value_counts()
# nodes_over_2 = node_counts[node_counts > 2].index.tolist()

# Check for edges with count > 2
edge_counts = edges_data.groupby(['edge_type']).size().reset_index(name='count')
edge_counts_list = edge_counts.to_records(index=False).tolist()

for edge_type, count in edge_counts_list:
    if count > max_edges_edge_type:
        print(f"Warning: {edge_type} has count > {max_edges_edge_type}")

# Filter out edges with count > 1
edges_to_display = [(u, v) for u, v, data in G.edges(data=True) if data['edge_type'] not in [edge_type for edge_type, count in edge_counts_list if count > max_edges_edge_type]]

# Create a set of nodes to display, including only nodes in the selected edges
nodes_to_display = set()
for edge in edges_to_display:
    nodes_to_display.add(edge[0])
    nodes_to_display.add(edge[1])

# Create a message for the plot
message = ""
for edge_type, count in edge_counts_list:
    if count > max_edges_edge_type:
        message += f"Warning: {edge_type} has count > {max_edges_edge_type}\n"

if not message:
    message = (f"No edges with count > {max_edges_edge_type}")

# Draw the graph
nx.draw(G, with_labels=True, nodelist=nodes_to_display, edgelist=edges_to_display)

# Display the message on the plot
plt.text(0.0, 0., message, horizontalalignment='left', verticalalignment='bottom', transform=plt.gca().transAxes,  color='red', weight='bold')

# Show the plot
plt.show()