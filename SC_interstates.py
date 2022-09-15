from pythonds3.basic import Stack
from pythonds3.graphs import Vertex, Graph

class GraphPlus(Graph):
    """pythonds3 Graph class with additions."""
    def add2WayEdge(self, fro:Vertex, to:Vertex, weight:int = 0) -> None:
        """Add a 2-way edge to the graph."""
        self.add_edge(fro, to, weight)
        self.add_edge(to, fro, weight)

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

def print_path(v: Vertex) -> None:
    """Print out the shortest path from the starting vertex to V."""
    # Use a Stack
    path: Stack = Stack()
    # Don't push the first node onto the stack, because it gets special treatment
    current: Vertex = v
    while current.get_previous() is not None:
        current = current.get_previous()
        path.push(current)
    # Print the nodes on the Stack
    while not path.is_empty():
        current = path.pop()
        print('{0} ({1}) \u2192'.format(current.get_key(), current.get_distance()),
                end=' ')
    # Print the original v    
    print('{0} ({1})'.format(v.get_key(), v.get_distance()))

def print_path_recursively(v: Vertex) -> None:
    """Print out a path, except the last node.  Do it recursively."""
    if v.get_previous() is not None:
        print_path_recursively(v.get_previous())
        print('\u2192', end=' ')
    print('{0} ({1})'.format(v.get_key(), v.get_distance()), end=' ')

def main():
    g = makeSCInterstates()
    # for v in g:
    #     print(v.get_key(), end=': ')
    #     for neighbor in v.get_neighbors():
    #         print(neighbor.get_key(), end=' ')
    #     print()
    # print()

    g.dijkstra(g.get_vertex('SPB'))
    for v in g:
        print_path_recursively(v)
        print()
        #print_path(v)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
