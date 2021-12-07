import FileParser as fp
import Graph as gp
import networkx as nx
import flow_measure as fm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from os.path import join
import os
import linecache
import json
import sys

filename='node-edge-pairs.json'
data=fp.loadData(filename)
edges=fp.getEdges(data)
nodes=fp.getNodes(edges)

'''filename2='email-Eu-core-temporal.txt'
fileObject=fp.getFileObject(filename2)
edges=fp.getEdges2(fileObject)
nodes=fp.getNodes(edges)'''

def buildAdjacencyList(G: nx.Graph):
    adjacency_list={}
    for n in G.nodes:
        neighbors=G.neighbors(n)
        adjacency_list[n]=list(neighbors)
    return adjacency_list

def save_plot(G, path, position):
    nx.draw_networkx(G, pos=position, with_labels=False, node_size=10, font_weight='bold')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def largest_component_fraction(G, N=None):
    if N is None:
        N = G.number_of_nodes()
    gcc=sorted(nx.connected_components(G), key=len, reverse=True)
    B=G.subgraph(gcc[0])
    q=B.number_of_nodes()/N
    return q

def getMaxValueFromDict(d):
    return np.max(np.array([*d.values()]))

def compute_measures(G, measure_results):
    row = [-1] * len(measures)
    for idx,measure in enumerate(measures):
        result = measure(G)
        
        if type(result) == dict:
            result = getMaxValueFromDict(result)
        elif type(result) in [None, np.float64, int, float, np.int64]:
            pass
        elif type(result) in [np.complex128]:
            result = result.astype(float)
        else:
            print(f"Something unexpected happned {type(result)}")
        row[idx] = result
    #measure_results =measure_results.append(pd.DataFrame(row.reshape(1,-1), columns=measures_col), ignore_index=True)
    measure_results.append(row)


if __name__ == "__main__":
    graph=gp.BuildGraph(nodes, edges)
    node_positions=nx.spring_layout(graph.G)
    G=graph.G
    # Largest component selection
    gcc=sorted(nx.connected_components(G), key=len, reverse=True)
    B=G.subgraph(gcc[0])
    G = nx.Graph(B)


    adjacency_list=buildAdjacencyList(G)
    N=G.number_of_nodes()

    #Deleted and reinserted nodes list
    '''
    deleted_nodes=[
        216439974, 712707184, 726762081, 615112623, 216475664, 729524223, 216427641, 216432533, 216462589, 729523798, 661589862, 726774707, 216487768, 216471439, 726770812, 721793906, 216368351, 721634926, 216430153, 726767890, 726769785, 216451169, 5288322376, 5288322350, 216434379, 700331164, 216493871, 216431260, 726776862, 615112671, 726781750, 726774125, 712707139, 726775812, 216427664, 1529258166, 216464362, 216485388, 1247769516, 726765813, 216494383, 857444986, 216441567, 726779625, 729488887, 712707557, 721635465, 1444098620, 5288308389, 267885350, 651838511, 216515272, 734844277, 216430525, 216471893, 216464031, 5879243694, 726767853, 713844814, 721834885, 216442670, 733302435, 726768277, 721634004, 216439010, 734273516, 216474016, 726780884, 721834973, 282597300, 712707082, 726772750, 274621814, 721635400, 216432520, 726767871, 726778258, 216463939, 700331199, 216368355, 216428693, 726760245, 216437539, 726778758, 5288322227, 721784449, 726782425, 1409131236, 3793408140, 726760581, 216514007, 216463990, 5879243693, 734272912, 216469810, 726762091, 687847677, 5880234344, 721642883, 726763091, 733309076, 734835075, 726740711, 712707604, 721791247, 734276427, 726776848, 726770175, 216431231, 5288322333, 5880234322, 726762103, 729499043, 726763109, 3793408144, 216432515, 721635392, 733311091, 726772237, 726768348, 726760329, 700331123, 734272817, 700419433, 712707477, 729489036, 687940709, 729523790, 216451474, 726766476, 721634384, 721634488, 726781181, 3588552659, 726781213, 9181749293
    ]
    reinserted_nodes=[
        729523790, 216432515, 726781213, 3588552659, 726781181, 721634384, 700331123, 721634488, 726766476, 216451474, 729489036, 726772237, 687940709, 712707477, 700419433, 734272817, 726760329, 726768348, 733311091, 721635392
    ]
    '''
    #FILEPATH = "Results/BB Road3/Result_BBRoad_Largest_BC_S1.txt"
    #DIRNAME= "figuresBC_S1"

    FILEPATH = sys.argv[1]
    DIRNAME= sys.argv[2]
    deleted_nodes = json.loads(linecache.getline(FILEPATH, 8))
    reinserted_nodes = json.loads(linecache.getline(FILEPATH, 11))

    if not os.path.isdir(DIRNAME):
        os.mkdir(DIRNAME)

    measures=[fm.critical_fraction, fm.closeness_centrality, fm.edge_betweenness_centrality, fm.edge_connectivity,
                fm.edge_load_centrality, fm.harmonic_centrality, fm.efficiency, fm.natural_connectivity, fm.node_betweenness_centrality,
                fm.node_connectivity, fm.node_load_centrality, fm.reaching_centrality, largest_component_fraction, 
                nx.number_connected_components, fm.reaching_centrality_local, fm.efficiency_local, fm.EGR, fm.subgraph_centrality
            ]
    measures_col = [x.__name__ for x in measures]
    del_measure_results = []

    compute_measures(G,del_measure_results)
    save_plot(G,join(DIRNAME, "D.png"), position=node_positions)

    #Measure with deleted nodes
    for idx,n in enumerate(deleted_nodes):
        G.remove_node(n)
        compute_measures(G,del_measure_results)
        if idx % 10 == 0:
            print (f"D{idx}")
            # del current_positions[n]
            save_plot(G,join(DIRNAME, f"D{idx}.png"), position=node_positions)

    in_measure_results = []
    save_plot(G,join(DIRNAME, "I.png"), position=node_positions)

    #Measure with reinserted nodes
    for idx, n in enumerate(reinserted_nodes):
        reinsert_node_neighbors=adjacency_list[n]
        if n not in G:
            G.add_node(n)
        reinsert_edges=[]
        for i in reinsert_node_neighbors:
            if i in G:
                reinsert_edges.append((n,i))
        G.add_edges_from(reinsert_edges)

        compute_measures(G,in_measure_results)
        if idx % 10 == 0:
            print (f"I{idx}")
            # current_positions[n] = node_positions[n]
            save_plot(G,join(DIRNAME, f"I{idx}.png"), position=node_positions)
        
    save_plot(G,join(DIRNAME, f"I{len(reinserted_nodes)-1}.png"), position=node_positions)
    
    DIRNAME = DIRNAME.replace("figures", "")
    pd.DataFrame(del_measure_results, columns=measures_col).to_csv(f"Result_BBRoad_Robustness_{DIRNAME}_del.csv")
    pd.DataFrame(in_measure_results, columns=measures_col).to_csv(f"Result_BBRoad_Robustness_{DIRNAME}_in.csv")
