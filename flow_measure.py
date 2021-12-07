import json
from networkx.algorithms.shortest_paths import dense
from networkx.linalg.graphmatrix import adjacency_matrix
from networkx.linalg.laplacianmatrix import laplacian_matrix
import numpy as np
import pandas as pd
import sys
import networkx as nx
import scipy

# (A,B,E1,5)
# {E1:5}
FILEPATH = "data/node-edge-pairs.json"
WEIGHTFILE = "data/edges.json"

# [[nodeA,nodeB,edge]]
def read_data(filepath):
    with open(filepath, "r") as node_edge_file:
        triplets = json.load(node_edge_file)
    node_pairs = [(e[0],e[1]) for e in triplets]
    with open(WEIGHTFILE, "r") as weight_file:
        W = json.load(weight_file)
    weighted_triplets = [(e[0],e[1],W[f"{e[2]}"]) for e in triplets]
    return  weighted_triplets, node_pairs

def build_graph(node_pairs, weighted=True):
    G = nx.Graph()
    if weighted:
        G.add_weighted_edges_from(node_pairs)
    else: 
        G.add_edges_from(node_pairs)
    return G

def degrees(G):
    A = nx.adjacency_matrix(G)
    return np.sum(A,axis=0)

def critical_fraction(G):
    degree_list = degrees(G)
    if type(degree_list) != 'np.ndarray':
        degree_list = np.array(degree_list, dtype=np.uintc)
    k = np.average(degree_list)
    k2 = np.average(np.square(degree_list))
    return 1.0 - (1.0 / (k2/k) - 1.0 )

# returns zero with weighted or unweighted graph ????
def algebraic_connectivity(G):
    return nx.algebraic_connectivity(G)

# return dict of node closeness values
# reciprocal of the average shortest path distance to a node over all other reachable nodes
def closeness_centrality(G):
    return nx.algorithms.closeness_centrality(G)

# return dict of node betweenness values
# sum of the fraction of all-pairs shortest paths that pass through the node
def node_betweenness_centrality(G, normalized=True):
    return nx.algorithms.betweenness_centrality(G,normalized=normalized)

# return dict of edge betweenness values
def edge_betweenness_centrality(G, normalized=True):
    return nx.algorithms.edge_betweenness_centrality(G,normalized=normalized)

# return dict of node load values
# Load centrality is slightly different than betweenness
# fraction of all shortest paths that pass through that node
def node_load_centrality(G, normalized=True):
    return nx.algorithms.load_centrality(G,normalized=normalized)

# returns dict of edge load values
def edge_load_centrality(G):
    return nx.algorithms.edge_load_centrality(G)

# returns dict of node centrality values
# sum of weighted closed walks of all lengths starting and ending at node
def subgraph_centrality(G):
    return nx.algorithms.subgraph_centrality(G)
    #return nx.algorithms.subgraph_centrality_exp(G)

# returns dict of nodes reaching centrality values
# local (LRC): proportion of other nodes reachable from that node
# global: proportion of the graph that is reachable from the neighbors of the node (approximately)
def reaching_centrality(G: nx.Graph, local=False):
    if local:
        result = {}
        for node in G.nodes:
            result[node] = nx.algorithms.local_reaching_centrality(G, node)
        return result
    return nx.algorithms.global_reaching_centrality(G)

def reaching_centrality_local(G):
    return reaching_centrality(G, local=True)

# returns dict of nodes harmonic centrality values
# sum of the reciprocal of the shortest path distances from one node all other nodes 
def harmonic_centrality(G):
    return nx.algorithms.harmonic_centrality(G)

# minimum number of nodes whose removal disconnects the graph
def node_connectivity(G):
    return nx.algorithms.node_connectivity(G)

# minimum number of edges whose removal disconnects the graph
def edge_connectivity(G):
    return nx.algorithms.edge_connectivity(G)

# WARNING: THIS IS SUPER SLOW (I would NOT use it)
# average of local node connectivity over all pairs of nodes of the graph
def average_node_connectivity(G):
    return nx.algorithms.average_node_connectivity(G)

# efficiency: multiplicative inverse of the shortest path distance between a pair of nodes
# global: average efficiency of all pairs of nodes
# local: average global efficiency of the subgraph induced by the neighbors of the node
# unweighted
def efficiency(G, local=False):
    if local:
        return nx.algorithms.local_efficiency(G)
    return nx.algorithms.global_efficiency(G)

def efficiency_local(G):
    return efficiency(G, local=True)

# returns maximum flow AND dict with flows used through each edge
# might be useful when fixing edges
def max_flow(G, source_node, destination_node):
    nx.flow.maximum_flow(G, source_node, destination_node)

#  NOT WORKING
def num_spanning_trees(G):
    laplacian = nx.laplacian_matrix(G)
    lambdas = np.linalg.eigvals(laplacian.A)
    positive_lambdas = (lambdas[lambdas > 0]).astype(float)
    return (1/len(positive_lambdas)) * np.prod(positive_lambdas)

def natural_connectivity(G):
    A = nx.adjacency_matrix(G)
    mius = np.linalg.eigvals(A.A)
    return np.log((1/len(mius)) * np.prod(np.exp(mius)))

# effective graph resistance
def EGR(G):
    laplacian = nx.laplacian_matrix(G)
    lambdas = np.linalg.eigvals(laplacian.A).astype(float)
    return len(lambdas) * np.sum((1/lambdas))


# This should be used with the graph at different steps of Decomposition/Fixing
# Average size of Largest Componenet (LC) over time (steps)
def R_value(G_list):
    avg_lc_size = []
    for G in G_list:
        Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
        LC = G.subgraph(Gcc[0])
        avg_lc_size += [LC.size()/G.size()]
    return np.average(avg_lc_size)

    
if __name__ == "__main__":
    # read_data(sys.argv[1])
    triplets, node_pairs = read_data(FILEPATH)
    G = build_graph(node_pairs,weighted=False)
    GW = build_graph(triplets,weighted=True)
    A = adjacency_matrix(G)
    AC = algebraic_connectivity(G)
    # NST = num_spanning_trees(G)
    #np.savetxt("data/adjacency_matrix.json", A.A, fmt='%d')
    #np.savetxt("data/laplacian_matrix.json", nx.laplacian_matrix(G).A, fmt='%d')
    aa= 0 
