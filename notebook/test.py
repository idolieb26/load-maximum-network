import numpy as np
import osmnx as ox
import networkx as nx
import igraph as ig

np.random.seed(0)
ox.settings.use_cache = True
ox.__version__



place = "Los Angeles, California, USA"
G = ox.graph_from_xml("./data/Los_Angeles.osm")


# bfs algorithms
# bfs = nx.algorithms.bfs_tree(G, G.nodes[0])

# manual discrete way
# impute speed on all edges missing data
G = ox.add_edge_speeds(G)

# calculate travel time (seconds) for all edges
G = ox.add_edge_travel_times(G)

# see mean speed/time values by road type
edges = ox.graph_to_gdfs(G, nodes=False)
edges["highway"] = edges["highway"].astype(str)
edges.groupby("highway")[["length", "speed_kph", "travel_time"]].mean().round(1)


nodes, edges = ox.graph_to_gdfs(G, nodes=True, fill_edge_geometry=True)
count = 0
total_length = 0

for edge in edges["length"]: 
    total_length = total_length + edge
    count = count + 1
    if total_length >= 100000:
        break

G2 = ox.graph_from_gdfs(nodes, edges[:count+1], graph_attrs=G.graph)
fig, ax = ox.plot_graph(G2, node_color="r")