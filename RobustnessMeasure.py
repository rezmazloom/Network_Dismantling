import FileParser as fp
import Graph as gp
import networkx as nx
import flow_measure as fm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename='node-edge-pairs.json'
data=fp.loadData(filename)
edges=fp.getEdges(data)
nodes=fp.getNodes(edges)

'''filename2='email-Eu-core-temporal.txt'
fileObject=fp.getFileObject(filename2)
edges=fp.getEdges2(fileObject)
nodes=fp.getNodes(edges)'''


graph=gp.BuildGraph(nodes, edges)
node_positions=nx.spring_layout(graph.G)
G=graph.G
adjacency_list=graph.adjacency_list
N=graph.N

def getLargestComponentFraction(G, N=graph.N):
    gcc=sorted(nx.connected_components(G), key=len, reverse=True)
    B=G.subgraph(gcc[0])
    q=B.number_of_nodes()/N
    return q

def getMaxValueFromDict(d):
    return np.max(np.array([*d.values()]))

#Deleted and reinserted nodes list
deleted_nodes=[
    726779625, 216437539, 712707082, 726761594, 712707604, 721793906, 726767871, 615112623, 216434379, 216368355, 216427664, 5879243694, 1247769516, 216432533, 216471439, 216442670, 5288322333, 216427636, 726774707, 267885350, 216431257, 726774125, 216439010, 216428693, 216475664, 734273516, 700331164, 721834885, 721635465, 5288322380, 729524223, 726781750, 216458912, 726758896, 726772750, 726774739, 216431231, 733309076, 3793408144, 615112636, 726769547, 729488887, 734844277, 216462589, 726774822, 5879243693, 726766458, 721793799, 726760189, 216464031, 726762081, 615112671, 661589862, 712707553, 368088540, 5288322341, 700331199, 216464362, 1409131237, 216463990, 216474016, 216471893, 216430525, 216493871, 733302435, 726773408, 721634926, 729523798, 726773331, 216430145, 216485388, 729484671, 726781213, 726760581, 721834973, 726760245, 216441567, 216515272, 857444986, 726762091, 216463939, 216494383, 3793408140, 9181749308, 726775812, 721784449, 3588552659, 282597300, 216432520, 216432515, 687940709, 726740711, 733302469, 729499325, 712707557, 712707473, 734272912, 5288322350, 216501463, 726760652, 700331123, 734844009, 726776848, 216460273, 726778758, 734276427, 1383639686, 216451474, 721791247, 733311091, 216451169, 9181749294, 726778338, 216442609, 726763127, 729523790, 726769154, 216432022, 721634384, 216464041, 726762122, 1444098586, 726778258, 1409279940, 1409279937, 615112633, 726779825, 4289849252, 7098875807, 216432513, 581232489, 280270689, 726769480, 721635069, 5886213860, 624641759, 1533386441, 1417483966, 721634982, 216485521, 726763152, 216485495, 267888193, 712707632, 729488918, 726758919, 4921030115, 819672531, 721804725, 5880208793, 712707477, 726766978
]
reinserted_nodes=[
    216368355, 734276427, 216432515, 726778258, 726762122, 216464041, 721634384, 729523790, 726763127, 216442609, 5288322350, 712707473, 9181749308, 726781213, 729484671, 368088540, 216458912, 819672531, 267888193, 1533386441, 5886213860, 726769480, 216432513, 1409279937, 1409279940, 1444098586, 700331123, 726758919, 721635069, 581232489, 726778338, 9181749294, 733311091
]

measures=[fm.critical_fraction, fm.closeness_centrality, fm.edge_betweenness_centrality, fm.edge_connectivity,
            fm.edge_load_centrality, fm.harmonic_centrality, fm.efficiency, fm.natural_connectivity, fm.node_betweenness_centrality,
            fm.node_connectivity, fm.node_load_centrality, fm.reaching_centrality,getLargestComponentFraction, 
            nx.number_connected_components
        ]
measures_col = [x.__name__ for x in measures]

#del_measure_results = pd.DataFrame(columns=measures_col)
del_measure_results = []

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

'''
#Single value
critical_fraction_list=[]
critical_fraction_list.append(fm.critical_fraction(G))

#Dictionary
closeness_centrality_list=[]
max_cc=getMaxValueFromDict(fm.closeness_centrality(G))
closeness_centrality_list.append(max_cc)

node_betweenness_centrality_list=[]
max_nbc=getMaxValueFromDict(fm.node_betweenness_centrality(G))
node_betweenness_centrality_list.append(max_nbc)
'''

compute_measures(G,del_measure_results)
#Measure with deleted nodes
for idx,n in enumerate(deleted_nodes):
    G.remove_node(n)
    compute_measures(G,del_measure_results)
    if idx % 10 == 0:
        print (f"D{idx}")
        nx.draw_networkx(G, pos=node_positions, with_labels=False, node_size=30, font_weight='bold')
        plt.savefig(f"figures1CCM/D{idx}.png")
    
'''
#Reinsert
largest_component_fraction_reinsert=[]
q=getLargestComponentFraction(G, N)
largest_component_fraction_reinsert.append(q)
#Single value
critical_fraction_list_reinsert=[]
critical_fraction_list_reinsert.append(fm.critical_fraction(G))
#Dictionary
closeness_centrality_list_reinsert=[]
max_cc=getMaxValueFromDict(fm.closeness_centrality(G))
closeness_centrality_list_reinsert.append(max_cc)

node_betweenness_centrality_list_reinsert=[]
max_nbc=getMaxValueFromDict(fm.node_betweenness_centrality(G))
node_betweenness_centrality_list_reinsert.append(max_nbc)
'''
in_measure_results = []
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
        print (f"I{idx}\n")
        nx.draw_networkx(G, pos=node_positions, with_labels=False, node_size=30, font_weight='bold')
        plt.savefig(f"figures1CCM/I{idx}.png")
    

pd.DataFrame(del_measure_results, columns=measures_col).to_csv("Result_BBRoad_Robustness_1C_CM_del.csv")
pd.DataFrame(in_measure_results, columns=measures_col).to_csv("Result_BBRoad_Robustness_1C_CM_in.csv")

'''
import json
filewriter=open("Result_BBRoad_Robustness_CM.txt", "a")
for inout_result_list in [del_measure_results, in_measure_results]:
    for idx,measure_results in enumerate(inout_result_list):
        filewriter.write(f"{measures[idx].__name__} During Deletion\n")
        json.dump(measure_results, filewriter)
'''
'''
filewriter.write("Critical Fraction During Deletion\n")
json.dump(critical_fraction_list, filewriter)
filewriter.write("\n\nCritical Fraction During Reinsert\n")
json.dump(critical_fraction_list_reinsert, filewriter)

filewriter.write("\n\nCloseness Centrality During Deletion\n")
json.dump(closeness_centrality_list, filewriter)
filewriter.write("\n\nCloseness Centrality During Reinsert\n")
json.dump(closeness_centrality_list_reinsert, filewriter)

filewriter.write("\n\nNode Betweenness Centrality During Deletion\n")
json.dump(node_betweenness_centrality_list, filewriter)
filewriter.write("\n\nNode Betweenness Centrality During Reinsert\n")
json.dump(node_betweenness_centrality_list_reinsert, filewriter)

filewriter.write("\n\nLargest Component Fraction During Reinsert\n")
json.dump(largest_component_fraction_reinsert, filewriter)
'''