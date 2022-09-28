from pythonds3.graphs import Vertex
from GraphPlus import GraphPlus
import graphmaker

def toposort(g: GraphPlus) -> list[Vertex]:
    """Perform a topological sort on the given graph G.
    Returns the result as a list of Vertexes.  G is reset
    in the process.  At the end, G has the times and distances
    from doing a DFS."""
    g.reset()
    g.dfs()
    vertex_list: list[Vertex] = []
    # Put all the vertices on a list
    for v in g:
        vertex_list.append(v)
    vertex_list.sort(key=Vertex.get_closing_time, reverse=True)
    
    return vertex_list


def main(args: list[str]) -> int:
    #g: GraphPlus = graphmaker.makeSCInterstates()
    g: GraphPlus = graphmaker.make_graph_7_18()
    g.print_adjacency_lists()

    vlist: list[Vertex] = toposort(g)
    for v in vlist:
        print(v.get_key(), v.get_closing_time())

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
