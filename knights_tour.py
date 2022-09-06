from pythonds3.graphs import Graph

def gen_legal_moves(row, col, board_size):
    new_moves = []
    move_offsets = [
        (-1, -2),  # left-down-down
        (-1, 2),   # left-up-up
        (-2, -1),  # left-left-down
        (-2, 1),   # left-left-up
        (1, -2),   # right-down-down
        (1, 2),    # right-up-up
        (2, -1),   # right-right-down
        (2, 1),    # right-right-up
    ]
    for r_off, c_off in move_offsets:
        if 0 <= row + r_off < board_size and 0 <= col + c_off < board_size:
            new_moves.append((row + r_off, col + c_off))
    return new_moves

def knight_graph(board_size):
    kt_graph = Graph()
    for row in range(board_size):
        for col in range(board_size):
            node_id = row * board_size + col
            new_positions = gen_legal_moves(row, col, board_size)
            for row2, col2 in new_positions:
                other_node_id = row2 * board_size + col2
                kt_graph.add_edge(node_id, other_node_id)
    return kt_graph

def order_by_avail(n):
    """Sort the neighbors list by the number of unvisited neighbors each neighbor has."""
    res_list = []
    for v in n.get_neighbors():
        if v.color == "white":
            c = 0
            for w in v.get_neighbors():
                if w.color == "white":
                    c = c + 1
            res_list.append((c, v))
    res_list.sort(key=lambda x: x[0])
    return [y[1] for y in res_list]

def knight_tour(n, path, u, limit):
    """Create a knight's tour of a graph containing Vertex u.
    Parameters: n: current path length
                path: current path
                u: current square (node)
                limit: how long the path should be to give a full tour"""
    u.color = "gray"
    path.append(u)
    if n < limit:
        neighbors = order_by_avail(u)
        i = 0
        done = False
        while i < len(neighbors) and not done:
            if neighbors[i].color == "white":
                done = knight_tour(n + 1, path, neighbors[i], limit)
            i = i + 1
        if not done:  # prepare to backtrack
            path.pop()
            u.color = "white"
    else:
        done = True
    return done

def print_graph(g):
    for v in g:
        print(v.get_key(), ':', [x.get_key() for x in v.get_neighbors()])

def main(args):
    board_size = 8
    g = knight_graph(board_size)
    print_graph(g)
    done = False
    start = 0
    path = []
    while not done and start < board_size * board_size:
        done = knight_tour(0, path, g.get_vertex(start), board_size * board_size - 1)
        if not done:
            start = start + 1
    
    if not done:
        print('Failed.')
    else:
        print("Path:")
        for v in path:
            print(v)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))