from pythonds3.basic import Stack
from pythonds3.graphs import Vertex, Graph

class GraphPlus(Graph):
    """pythonds3 Graph class with additions."""
    def add2WayEdge(self, fro:Vertex, to:Vertex, weight:int = 0) -> None:
        """Add a 2-way edge to the graph."""
        self.add_edge(fro, to, weight)
        self.add_edge(to, fro, weight)

    def print_path(self, v: Vertex) -> None:
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

    def print_path_recursively(self, v: Vertex) -> None:
        """Print out a path, except the last node.  Do it recursively."""
        if v.get_previous() is not None:
            self.print_path_recursively(v.get_previous())
            print('\u2192', end=' ')
        print('{0} ({1})'.format(v.get_key(), v.get_distance()), end=' ')

    def print_graph(self) -> None:
        """Print out the graph by printing the path for each vertex."""
        for v in self:
            self.print_path(v)

    def reset(self) -> None:
        """Reset the graph to its initial tate, before any algorithms
        were run on it."""
        for v in self:
            v.set_color('white')
            v.set_distance(0)
            v.set_previous(None)
            v.set_discovery_time(0)
            v.set_closing_time(0)
