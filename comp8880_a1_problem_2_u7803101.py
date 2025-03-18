# -*- coding: utf-8 -*-
"""COMP8880 a1 - Problem 2 - u7803101.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JqOy7pLTV9aYQe3xq3Kp3ZPEDHC0iycP
"""

from google.colab import files

uploaded = files.upload()

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

cities = pd.read_csv('global-cities.dat', sep='|', header=None, engine='python')
network = pd.read_csv('global-net.dat', sep='\s+', header=None, engine='python')

cities.columns = ['Airport_Code', 'NodeID', 'City']
network.columns = ['node1', 'node2']

G = nx.Graph()

# A node is a city
for idx, row in cities.iterrows():
    node_id = str(row['NodeID'])
    G.add_node(
        node_id,
        Airport_Code=row['Airport_Code'],
        City=row['City']
    )

# an edge is an airline
for idx, row in network.iterrows():
    node1 = str(row['node1'])
    node2 = str(row['node2'])
    G.add_edge(node1, node2)

# 2-1

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print('Number of nodes:', num_nodes)
print('Number of edges:', num_edges)

# 2-2

connected_components = list(nx.connected_components(G))
num_of_components = len(connected_components)
print('Number of connected components:', num_of_components)

largest_cc = max(connected_components, key=len)
G_largest = G.subgraph(largest_cc).copy()
print('Largest component nodes:', G_largest.number_of_nodes())
print('Largest component edges:', G_largest.number_of_edges())

# 2-3

# Calculate the degree of each node
degree_list = G_largest.degree()
sorted_degree = sorted(degree_list, key=lambda x: x[1], reverse=True)

top10_degree = sorted_degree[:10]
for node_id, deg in top10_degree:
    city_name = G_largest.nodes[node_id]['City']  # Get city name from node
    print(f'{city_name} - {deg}')

# 2-4

import matplotlib.pyplot as plt
import collections

degree_of_nodes = [d for n, d in G.degree()]
degree_counts = collections.Counter(degree_of_nodes)

x = sorted(degree_counts.keys())  # the sorted list of unique degree values
total_nodes = G.number_of_nodes()
y = [degree_counts[x] / total_nodes for x in x] # fraction of nodes with each degree value

fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# Degree Distribution
ax[0].scatter(x, y)
ax[0].set_title('Degree Distribution')
ax[0].set_xlabel('Degree')
ax[0].set_ylabel('Fraction of Nodes')
ax[0].grid(True)

# log-log scale
ax[1].scatter(x, y)
ax[1].set_xscale('log')
ax[1].set_yscale('log')
ax[1].set_title('Degree Distribution (log-log Scale)')
ax[1].set_xlabel('Degree (log scale)')
ax[1].set_ylabel('Fraction of Nodes (log-log scale)')
ax[1].grid(True, which='both')

plt.tight_layout()
plt.show()

# 2-5

diameter = nx.diameter(G_largest)
print('Diameter of the largest component:', diameter)

# a pair of nodes and its shortest path length is diameter
nodes_largest = list(G_largest.nodes())
longest_path = None

for i in range(len(nodes_largest)):
    for j in range(i+1, len(nodes_largest)):
        source = nodes_largest[i]
        target = nodes_largest[j]
        # get the shortest path
        path = nx.shortest_path(G_largest, source=source, target=target)
        if len(path) - 1 == diameter:
            longest_path = path
            break
    if longest_path:
        break

if longest_path:
    # print the path with cities' name
    path_cities = [G_largest.nodes[n]['City'] for n in longest_path]
    print(' - '.join(path_cities))

# 2-6

def find_node_by_city(city):
    for n, data in G.nodes(data=True):
        if city in data['City']:
            return n
    return None

node_cbr = find_node_by_city('Canberra')
node_cpt = find_node_by_city('Cape Town')

if node_cbr and node_cpt:
    path_cbr_cpt = nx.shortest_path(G_largest, source=node_cbr, target=node_cpt)
    path_cities = [G_largest.nodes[n]['City'] for n in path_cbr_cpt]
    print(f'Smallest number of flights from CBR to CPT needed: {len(path_cbr_cpt)-1}')
    print(' - '.join(path_cities))

# 2-7

betweenness = nx.betweenness_centrality(G_largest, normalized=True)
# sort by betweenness
sorted_bc = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
top10_bc = sorted_bc[:10]

for node_id, bc_value in top10_bc:
    city_name = G_largest.nodes[node_id]['City']
    print(f'{city_name} - {bc_value:.5f}')