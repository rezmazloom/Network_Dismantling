from typing import overload
import networkx as nx

class BuildGraph:
    def __init__(self, nodes, edges):
        self.G=nx.Graph()
        self.nodes=nodes
        self.edges=edges
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(edges)
        self.adjacency_list=self.buildAdjacencyList()
        self.N=self.G.number_of_nodes()

    def findNeighbors(self, n):
        
        return list(self.G.neighbors(n))
        '''
        neighbors=[]
        for key, value in self.G[n].items():
            neighbors.append(key)
        return neighbors
        '''
        

    def buildAdjacencyList(self):
        adjacency_list={}
        for n in self.nodes:
            neighbors=self.findNeighbors(n)
            adjacency_list[n]=neighbors
        return adjacency_list