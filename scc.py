from GraphPlus import GraphPlus

def make_graph():
    "Make the graph from section 7.18 of Miller & Ranum."
    g = GraphPlus()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('B', 'E')
    g.add_edge('C', 'C')
    g.add_edge('C', 'F')
    g.add_edge('D', 'B')
    g.add_edge('D', 'G')
    g.add_edge('E', 'A')
    g.add_edge('E', 'D')
    g.add_edge('F', 'H')
    g.add_edge('G', 'E')
    g.add_edge('H', 'I')
    g.add_edge('I', 'F')
    return g

def transpose(g):
    """Calculate and return the transpose of the given graph G.  G is not changed."""
    gT = GraphPlus()
    for v in g:
        for to_v in v.get_neighbors():
            gT.add_edge(to_v.get_key(), v.get_key())
    return gT

def print_graph(g):
    for v in g:
        print(v.get_key(), ':', [x.get_key() for x in v.get_neighbors()])

def closing_time(pair):
    """Return the second item in the given pair."""
    return pair[1]

def keys_by_closing_time(g):
    """Return a list of the vertex keys in g, sorted by closing time."""
    vertex_list = []
    for v in g:
        vertex_list.append((v.get_key(), v.get_closing_time()))
    print(vertex_list)
    vertex_list.sort(key=closing_time, reverse=True)
    print(vertex_list)
    key_list = []
    for pair in vertex_list:
        key_list.append(pair[0])
    return key_list

def dfs_by_key_list(g, key_list):
    """Perform a depth-first search on graph G, checking the vertices in the order
    specified by KEY_LIST."""
    for key in key_list:
        if g.get_vertex(key).color == "white":
            g.dfs_visit(g.get_vertex(key))

def main(args):
    g = make_graph()
    print_graph(g)
    print()
    g.dfs()
    gT = transpose(g)
    print_graph(gT)

    key_list = keys_by_closing_time(g)
    print(key_list)
    print()

    dfs_by_key_list(gT, key_list)
    for v in gT:
        print(v)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))