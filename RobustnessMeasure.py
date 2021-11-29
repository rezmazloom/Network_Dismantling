import FileParser as fp
import Graph as gp
import networkx as nx
import flow_measure as fm

filename='node-edge-pairs.json'
data=fp.loadData(filename)
edges=fp.getEdges(data)
nodes=fp.getNodes(edges)

'''filename2='email-Eu-core-temporal.txt'
fileObject=fp.getFileObject(filename2)
edges=fp.getEdges2(fileObject)
nodes=fp.getNodes(edges)'''

def getLargestComponentFraction(G, N):
    gcc=sorted(nx.connected_components(G), key=len, reverse=True)
    B=G.subgraph(gcc[0])
    q=B.number_of_nodes()/N
    return q

def getMaxValueFromDict(d):
    values=d.values()
    max_val=max(values)
    return max_val

graph=gp.BuildGraph(nodes, edges)
G=graph.G
adjacency_list=graph.adjacency_list
N=graph.N

#Deleted and reinserted nodes list
deleted_nodes=[734839655, 726779625, 216437539, 712707082, 726761594, 712707604, 721793906, 726767871, 615112623, 216434379, 216368355, 216427664, 5879243694, 1247769516, 216432533, 216471439, 216442670, 5288322333, 216427636, 726774707, 267885350, 216431257, 726774125, 216439010, 216428693, 216475664, 734273516, 700331164, 721834885, 721635465, 5288322380, 729524223, 726781750, 216458912, 726758896, 700331225, 726772750, 726774739, 216431231, 733309076, 3793408144, 216461271, 615112636, 726769547, 726761193, 729488887, 734844277, 216462589, 726760583, 726774822, 5879243693, 726766458, 721793799, 726760189, 216464031, 726762081, 692566562, 615112671, 726759274, 661589862, 712707553, 368088540, 726775131, 5288322341, 726760646, 726760642, 700331199, 216464362, 1409131237, 216463990, 692130351, 216474016, 216471893, 216453322, 726767583, 216430525, 216493871, 726779639, 733302435, 726773408, 721634926, 729523798, 726773331, 216430145, 9206246936, 216485388, 700331507, 729484671, 726781213, 734272742, 5079784655, 726760581, 721834973, 726770593, 726760245, 216441567, 216515272, 692130502, 857444986, 726762091, 216463939, 4225970749, 216494383, 726767908, 726769910, 3793408140, 9181749308, 726775812, 721784449, 4225971002, 4225970888, 9206221314, 3588552659, 282597300, 216432520, 216432515, 733302559, 687940709, 726781712, 726740711, 733302469, 729499325, 712707557, 700331472, 712707473, 734272912, 5288322350, 216501463, 726760652, 734272686, 700331123, 734844009, 6463091815, 726781028, 726776848, 216460273, 726778758, 734276427, 4225970963, 2001830553, 1383639686, 216451474, 721791247, 733311091, 216451169, 9181749294, 4225969372, 726778740, 4225970802, 726778338, 726775667, 216442609, 726763127, 729523790, 726769154, 216432022, 700331283, 721634384, 216464041, 726762122, 1444098586, 216492520, 726778258, 734839021, 1409279940, 1409279937, 216475583, 615112633, 726779825, 4289849252, 7098875807, 216432513, 581232489, 280270689, 726769480, 726767421, 4822005564, 721635069, 726777590, 5886213860, 624641759, 1533386441, 1417483966, 721634982, 216485521, 726763152, 216485495]
reinserted_nodes=[726774707, 712707604, 216471893, 726774739, 726781750, 216475664, 216428693, 216451169, 721791247, 216451474, 2001830553, 726776848, 726781028, 6463091815, 734272686, 726760652, 216501463, 733302469, 726740711, 726781712, 216432515, 3588552659, 726769910, 726760245, 721634926, 726775131, 5288322380, 216442670, 216471439, 734839021, 726763127, 216442609, 726778338, 4225969372, 5079784655, 216460273, 700331123, 700331472, 729499325, 687940709, 733302559, 282597300, 4225970888, 726781213, 692130351, 726758896, 5288322333, 1417483966, 1533386441, 5886213860, 726777590, 4822005564, 726767421, 216432513, 726779825, 216475583, 1409279940, 216492520, 1444098586, 700331283, 726769154, 726775667, 726778740, 726762091, 726760646, 368088540, 216461271, 3793408144, 7098875807, 4225970802, 4225971002, 726761594]

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

#Measure with deleted nodes
for n in deleted_nodes:
    G.remove_node(n)

    #Append single value
    critical_fraction_list.append(fm.critical_fraction(G))

    #Get max from dictionary and append
    max_cc=getMaxValueFromDict(fm.closeness_centrality(G))
    closeness_centrality_list.append(max_cc)

    max_nbc=getMaxValueFromDict(fm.node_betweenness_centrality(G))
    node_betweenness_centrality_list.append(max_nbc)

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

#Measure with reinserted nodes
for n in reinserted_nodes:
    reinsert_node_neighbors=adjacency_list[n]
    if n not in G:
        G.add_node(n)
    reinsert_edges=[]
    for i in reinsert_node_neighbors:
        if i in G:
            reinsert_edges.append((n,i))
    G.add_edges_from(reinsert_edges)

    q=getLargestComponentFraction(G, N)
    largest_component_fraction_reinsert.append(q)

    #Append single value
    critical_fraction_list_reinsert.append(fm.critical_fraction(G))

    #Get max from dictionary and append
    max_cc=getMaxValueFromDict(fm.closeness_centrality(G))
    closeness_centrality_list_reinsert.append(max_cc)

    max_nbc=getMaxValueFromDict(fm.node_betweenness_centrality(G))
    node_betweenness_centrality_list_reinsert.append(max_nbc)

import json
filewriter=open("Result_BBRoad_Robustness_CM.txt", "a")

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