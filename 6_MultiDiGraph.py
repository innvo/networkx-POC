import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

max_edges_edge_type = 5

# Your data
edges_data = pd.DataFrame({
    'src': ['A', 'A', 'A','A','A'],
    'dst': ['B', 'C', 'D', 'C','D'],
    'edge_type': ['person_address', 'person_receipt', 'person_address','person_receipt','person_address' ],
    'role': ['X', 'attorney','','preparer',''],
    'addr_date': ['2023-12-05', '', '2021-01-05', '','2023-12-05']
})

nodes_data = pd.DataFrame({
    'id': ['A','B','C','D'],
    'node_type': ['person', 'address', 'receipt','address'],
    'node_name': ['ERIC', '123 MAIN ST', 'R12345', '123 MAIN STREET'],
    'receipt_payment_date': ['', '', '2023-12-05', '']
})

# Create a directed graph
G = nx.MultiDiGraph()

# Add nodes and edges to the graph
for _, row in nodes_data.iterrows():
    G.add_node(row['id'], node_type=row['node_type'], node_name=row['node_name'], receipt_payment_date=row['receipt_payment_date'])

for _, row in edges_data.iterrows():
    G.add_edge(row['src'], row['dst'], edge_type=row['edge_type'], role=row['role'], addr_date=row['addr_date'])

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='skyblue', node_size=1500, arrows=True)
nx.draw_networkx_labels(G, pos)

# Draw edges with a curve
for (u, v, d) in G.edges(data=True):
    same_edge_count = len([edge for edge in G.edges(data=True) if edge[0] == u and edge[1] == v])
    for i in range(same_edge_count):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], connectionstyle=f'arc3, rad = {0.6 * i}', arrowstyle='->')

# Draw edge labels
edge_count = {}
for (u, v, d) in G.edges(data=True):
    role = d['role']
    addr_date = d['addr_date']
    if role:
        if (u, v) not in edge_count:
            edge_count[(u, v)] = 0
        label_pos = (pos[u] + pos[v]) / 2  # Midpoint between source and destination nodes
        label_pos += np.array([0, 0.1 * edge_count[(u, v)]])  # Adjust label position based on number of edges
        plt.text(label_pos[0], label_pos[1], f'role: {role}', fontsize=10)
        edge_count[(u, v)] += 1
    if addr_date:
        if (u, v) not in edge_count:
            edge_count[(u, v)] = 0
        label_pos = (pos[u] + pos[v]) / 2  # Midpoint between source and destination nodes
        label_pos += np.array([0, 0.1 * edge_count[(u, v)]])  # Adjust label position based on number of edges
        plt.text(label_pos[0], label_pos[1], f'date: {addr_date}', fontsize=10)
        edge_count[(u, v)] += 1

plt.show()