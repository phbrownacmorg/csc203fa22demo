from pythonds3.basic import Stack
from pythonds3.graphs import Vertex, Graph
from GraphPlus import GraphPlus

def makeSCInterstates():
    g = GraphPlus()
    g.add2WayEdge('SPB', 'AVL', 70)
    g.add2WayEdge('SPB', 'GVL', 30)
    g.add2WayEdge('SPB', 'CLN', 36)
    g.add2WayEdge('SPB', 'CLT', 75)
    g.add2WayEdge('GVL', 'CLN', 46)
    g.add2WayEdge('GVL', 'ATL', 145)
    g.add2WayEdge('CLN', 'CLB', 63)
    g.add2WayEdge('CLB', 'CLT', 93)
    g.add2WayEdge('CLB', 'AUG', 76)
    g.add2WayEdge('CLB', 'FLO', 83)
    g.add2WayEdge('CLB', 'WSL', 62)
    g.add2WayEdge('CLB', 'WSL', 62)
    g.add2WayEdge('WSL', 'FLO', 86)
    g.add2WayEdge('WSL', 'SAV', 99)
    g.add2WayEdge('WSL', 'CHS', 58)
    g.add2WayEdge('FLO', 'FAY', 88)    
    return g

def main():
    g = makeSCInterstates()

    #g.dijkstra(g.get_vertex('SPB'))
    g.prim(g.get_vertex('SPB'))
    g.print_all_paths()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
