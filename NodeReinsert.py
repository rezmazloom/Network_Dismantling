import networkx as nx

class Reinsert():
    def __init__(self, graph, adjacency_list, deleted_nodes, N):
        self.dismantled_graph=graph
        self.adjacency_list=adjacency_list
        self.deleted_nodes=deleted_nodes
        self.N=N

    def findReinsertNode(self, deleted_nodes):
        max_component_no=0
        reinsert_node=None
        for dn in deleted_nodes:
            component_list=[]
            neighbors=self.adjacency_list[dn]
            for n in neighbors:
                for sg in nx.connected_components(self.dismantled_graph):
                    component=self.dismantled_graph.subgraph(sg)
                    if n in component:
                        if len(component_list)==0:
                            component_list.append(component)
                        else:
                            for c in component_list:
                                if nx.is_isomorphic(c, component):
                                    pass
                                else:
                                    component_list.append(component)
                        break
            if len(component_list)>=max_component_no:
                max_component_no=len(component_list)
                reinsert_node=dn
        return reinsert_node

    def reinsertNode(self):
        reinserted_nodes=[]
        gcc=sorted(nx.connected_components(self.dismantled_graph), key=len, reverse=True)
        B=self.dismantled_graph.subgraph(gcc[0])
        q=B.number_of_nodes()/self.N
        while len(self.deleted_nodes)>0:
            reinsert_node=self.findReinsertNode(self.deleted_nodes)
            reinsert_node_neighbors=self.adjacency_list[reinsert_node]
            if reinsert_node not in self.dismantled_graph:
                self.dismantled_graph.add_node(reinsert_node)
            reinsert_edges=[]
            for i in reinsert_node_neighbors:
                if i in self.dismantled_graph:
                    reinsert_edges.append((reinsert_node,i))
            self.dismantled_graph.add_edges_from(reinsert_edges)
            reinserted_nodes.append(reinsert_node)
            gcc=sorted(nx.connected_components(self.dismantled_graph), key=len, reverse=True)
            B=self.dismantled_graph.subgraph(gcc[0])
            q=B.number_of_nodes()/self.N
            if q>=0.01:
                self.dismantled_graph.remove_node(reinsert_node)
                reinserted_nodes.remove(reinsert_node)
            self.deleted_nodes.remove(reinsert_node)

        return self.dismantled_graph, reinserted_nodes