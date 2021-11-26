import FileParser as fp
import Graph as gp
import networkx as nx

'''filename='node-edge-pairs.json'
data=fp.loadData(filename)
edges=fp.getEdges(data)
nodes=fp.getNodes(edges)'''

filename2='email-Eu-core-temporal.txt'
fileObject=fp.getFileObject(filename2)
edges=fp.getEdges2(fileObject)
nodes=fp.getNodes(edges)

graph=gp.BuildGraph(nodes, edges)

'''import json
n=[]
f=open('nodes.json')
d=json.load(f)
for k, v in d.items():
    n.append(int(k))

print(len(n))
print(len(nodes))
diff=list(set(n)-set(nodes))
print(diff)'''


#nodes=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
#edges=[(1,6),(2,4),(3,4),(4,6),(5,6),(6,5),(6,1),(6,4),(6,7),(7,8),(7,10),(8,9),(8,10),(10,11),(10,12),(10,13),(10,14),(11,12),(11,13),(12,13),(12,15),(13,15),(15,16),(16,17)]

print("Number of nodes in the initial graph: "+str(len(nodes)))
print("Number of edges in the initial graph: "+str(len(edges)))

dismantled_graph=nx.Graph()

import NetworkDismantling as ND
nd=ND.Dismantle(graph)

largest_component_fraction=[]
efficiency_list=[]
average_clustering_coefficient=[]
transitivity=[]
number_of_deletion=[]
deleted_nodes=[]
dismantled_graph, largest_component_fraction, efficiency_list, average_clustering_coefficient, transitivity, number_of_deletion, deleted_nodes=nd.dismantle()

import json
filewriter=open("Result_Email_CM.txt", "a")
filewriter.write("Largest Component Fraction\n")
json.dump(largest_component_fraction, filewriter)
filewriter.write("\n\nEfficiency\n")
json.dump(efficiency_list, filewriter)
filewriter.write("\n\nAverage Clustering Coefficient\n")
json.dump(average_clustering_coefficient, filewriter)
filewriter.write("\n\nTransitivity\n")
json.dump(transitivity, filewriter)
filewriter.write("\n\nNumber of Deletion\n")
json.dump(number_of_deletion, filewriter)

#Reinsert
import NodeReinsert as NR
print("Node reinserting started...")
nr=NR.Reinsert(dismantled_graph, graph.adjacency_list, deleted_nodes, graph.N)
dismantled_graph_node_reinserted=nr.reinsertNode()
print("Node reinserting finished")

efficiency_after_reinsert=nx.global_efficiency(dismantled_graph_node_reinserted)
avg_cc_after_reinsert=nx.average_clustering(dismantled_graph_node_reinserted)
transitivity_after_reinsert=nx.transitivity(dismantled_graph_node_reinserted)

filewriter.write("\n\nEfficiency After Reinsert\n")
json.dump([efficiency_after_reinsert], filewriter)
filewriter.write("\n\nAvg CC After Reinsert\n")
json.dump([avg_cc_after_reinsert], filewriter)
filewriter.write("\n\nTransitivity After Reinsert\n")
json.dump([transitivity_after_reinsert], filewriter)

filewriter.close()

#Draw Network
pos=nx.spring_layout(dismantled_graph)
gcc=sorted(nx.connected_components(dismantled_graph_node_reinserted), key=len, reverse=True)
largest_component=dismantled_graph_node_reinserted.subgraph(gcc[0])
print("Largest component size: "+str(largest_component.number_of_nodes()))
for sg in nx.connected_components(dismantled_graph_node_reinserted):
    component=dismantled_graph_node_reinserted.subgraph(sg)
    if component.number_of_nodes()==largest_component.number_of_nodes():
        nx.draw_networkx(component, pos=pos, with_labels=False, node_size=30, font_weight='bold', node_color='red')
    else:
        nx.draw_networkx(component, pos=pos, with_labels=False, node_size=30, font_weight='bold', node_color='purple')
#nx.draw_networkx(dismantled_graph, with_labels=False, node_size=20, font_weight='bold', node_color='red')

import matplotlib.pyplot as plt
plt.title("Network After Dismantling and Node Reinserting (Email All)")
plt.savefig('Email_CM.png')
