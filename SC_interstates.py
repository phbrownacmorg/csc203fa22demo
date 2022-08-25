from Vertex import Vertex
from MR_Graph import Graph

def main():
    g = Graph()
    g.add2WayEdge('SPB', 'AVL', 65)
    g.add2WayEdge('SPB', 'GVL', 35)
    g.add2WayEdge('SPB', 'Clinton', 35)

    for v in g:
        print(v)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())