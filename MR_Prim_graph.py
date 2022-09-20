from pythonds3.graphs import Vertex, Graph
from GraphPlus import GraphPlus

def make_Prim_graph() -> GraphPlus:
    g: GraphPlus = GraphPlus()
    g.add2WayEdge('A', 'B', 2)
    g.add2WayEdge('A', 'C', 3)
    g.add2WayEdge('B', 'C', 1)
    g.add2WayEdge('B', 'D', 1)
    g.add2WayEdge('B', 'E', 4)
    g.add2WayEdge('C', 'F', 5)
    g.add2WayEdge('D', 'E', 1)
    g.add2WayEdge('E', 'F', 1)
    g.add2WayEdge('F', 'G', 1)
    return g

def main():
    g: GraphPlus = make_Prim_graph()
    g.prim(g.get_vertex('A'))
    g.print_graph()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
