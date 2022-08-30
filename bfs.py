from pythonds3.graphs import Graph
from pythonds3.basic import Queue

def build_graph(filename):
    buckets = {}
    the_graph = Graph()
    with open(filename, "r", encoding="utf8") as file_in:
        all_words = file_in.readlines()
    # create buckets of words that differ by 1 letter
    for line in all_words:
        word = line.strip()
        for i, _ in enumerate(word):
            bucket = f"{word[:i]}_{word[i + 1 :]}"
            buckets.setdefault(bucket, set()).add(word)

    # add edges between different words in the same bucket
    for similar_words in buckets.values():
        for word1 in similar_words:
            for word2 in similar_words - {word1}:
                the_graph.add_edge(word1, word2)
    return the_graph

def main():
    g:Graph = build_graph('wordlist.txt')
    g.reset_distances()
    g.bfs(g.get_vertex('sage')) # Actually sets shortest distances from "sage"
    g.traverse('sage', 'fool')

if __name__ == '__main__':
    main()
    import sys
    sys.exit()
