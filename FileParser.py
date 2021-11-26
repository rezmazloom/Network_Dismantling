import json
import itertools

def loadData(filename):
    f=open(filename)
    data=json.load(f)
    return data

def getEdges(data):
    edges=[]
    for node_pairs in data:
        node_pair=(node_pairs[0], node_pairs[1])
        edges.append(node_pair)
    return edges

def getNodes(edges):
    return set(itertools.chain.from_iterable(edges))

def getFileObject(filename):
    f=open(filename, 'r')
    return f

def getEdges2(fileObj):
    edges=[]
    for line in fileObj:
        line=line.strip('\n')
        tokens=line.split(' ')
        node_pair=(tokens[0], tokens[1])
        edges.append(node_pair)
    return edges