import networkx as nx
from Graph import BuildGraph
import numpy as np

class Dismantle(BuildGraph):
    def __init__(self, graph):
        self.G=graph.G
        self.nodes=graph.nodes
        self.edges=graph.edges
        self.N=graph.N

    def calculateRLink(self, n):
        
        neighbors=self.findNeighbors(n)
        neighbor_graph = self.G.subgraph(neighbors)
        return nx.Graph.number_of_edges(neighbor_graph)
        '''
        neighbors=self.findNeighbors(n)
        RLink=0
        i=0
        while(i<len(neighbors)):
            j=i+1
            while(j<len(neighbors)):
                a=neighbors[i]
                b=neighbors[j]
                if(((a,b) in self.edges) or ((b,a) in self.edges)):
                    RLink=RLink+1
                j=j+1
            i=i+1
        return RLink
        '''

    def calculateDismantlingFactor(self, n):
        return self.G.degree(n)/(self.calculateRLink(n)+1)

    def centralityMeasure(self, n):
        neighbors=self.findNeighbors(n)
        gamma_sum=0
        for j in neighbors:
            gamma_sum=gamma_sum+(self.G.degree(j)-1)
        dismantling_factor=self.calculateDismantlingFactor(n)
        centrality_measure=dismantling_factor*(self.G.degree(n)-1)*gamma_sum
        return centrality_measure

    def dfBcCentralityMeasure(self, n):
        bc_list=nx.betweenness_centrality(self.G)
        dismantling_factor=self.calculateDismantlingFactor(n)
        centrality_measure=dismantling_factor*bc_list[n]
        return centrality_measure

    def maxCMFromAllNodes(self):
        max_cm=0
        max_cm_node=None
        for i in self.nodes:
            temp_cm=self.centralityMeasure(i)
            if temp_cm>=max_cm:
                max_cm=temp_cm
                max_cm_node=i
        return max_cm, max_cm_node

    def maxBCFromAllNodes(self):
        max_cm=0
        max_cm_node=None
        cm_list=nx.betweenness_centrality(self.G)
        max_cm_node=max(cm_list, key=cm_list.get)
        max_cm=cm_list[max_cm_node]
        return max_cm, max_cm_node

    def maxDfBcFromAllNodes(self):
        max_cm=0
        max_cm_node=None
        for i in self.nodes:
            temp_cm=self.dfBcCentralityMeasure(i)
            if temp_cm>=max_cm:
                max_cm=temp_cm
                max_cm_node=i
        return max_cm, max_cm_node

    def maxDfBcFromAllNodes2(self):
        rlink = {}
        dismantling_factor = {}
        for n in self.nodes:
            #rlink[n] = nx.Graph.number_of_edges(self.G.subgraph(self.G.neighbors(n)))
            rlink[n] = self.calculateRLink(n)
            #dismantling_factor[n] = self.G.degree(n)/(rlink[n]+1)
            dismantling_factor[n] = self.calculateDismantlingFactor(n)
        bc_list=nx.betweenness_centrality(self.G)
        keys = list(bc_list.keys())
        dfbc = np.array([bc_list[key]*dismantling_factor[key] for key in keys])
        return np.max(dfbc), keys[np.argmax(dfbc)]

            


#print("Algebraic connectivity before dismantling: "+str(nx.algebraic_connectivity(G)))
#print("Efficiency before dismantling: "+str(nx.global_efficiency(G)))

    def dismantle(self):
        #NLS network dismantling algorithm
        #print("Efficiency before dismantling: "+str(nx.global_efficiency(self.G)))
        deletion_count=0
        number_of_deletion=[]
        number_of_deletion.append(deletion_count)
        #efficiency_list=[]
        #efficiency_list.append(nx.global_efficiency(self.G))
        #average_clustering_coefficient=[]
        #average_clustering_coefficient.append(nx.average_clustering(self.G))
        #transitivity=[]
        #transitivity.append(nx.transitivity(self.G))
        print("Dismantling started...")
        threshold=0.01
        N=self.N
        S=[]
        gcc=sorted(nx.connected_components(self.G), key=len, reverse=True)
        B=self.G.subgraph(gcc[0])
        q=B.number_of_nodes()/N
        largest_component_fraction=[]
        largest_component_fraction.append(q)
        while(q>=threshold):
            #max_cm, max_cm_node=self.maxCMFromAllNodes()
            #max_cm, max_cm_node=self.maxBCFromAllNodes()
            max_cm, max_cm_node=self.maxDfBcFromAllNodes2()
            
            S.append(max_cm_node)
            self.G.remove_node(max_cm_node)
            self.nodes.remove(max_cm_node)

            gcc=sorted(nx.connected_components(self.G), key=len, reverse=True)
            B=self.G.subgraph(gcc[0])
            q=B.number_of_nodes()/N

            largest_component_fraction.append(q)
            deletion_count=deletion_count+1
            number_of_deletion.append(deletion_count)
            #efficiency_list.append(nx.global_efficiency(self.G))
            #average_clustering_coefficient.append(nx.average_clustering(self.G))
            #transitivity.append(nx.transitivity(self.G))
            if deletion_count % 10 == 0:
                print(deletion_count)
            #print(B.number_of_nodes())
            

        print("Dismantling finished")
        #print("Efficiency after dismantling: "+str(nx.global_efficiency(self.G)))

        return self.G, largest_component_fraction, number_of_deletion, S
        #print("Number of deleted nodes: "+str(len(S)))

        #print("Algebraic connectivity after dismantling: "+str(nx.algebraic_connectivity(G)))