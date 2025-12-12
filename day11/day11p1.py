#!/usr/bin/env python3

import networkx as nx

if __name__ == "__main__":
    G = nx.DiGraph()
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            parent, children_raw = line.rstrip().split(": ")
            G.add_node(parent)
            for child in children_raw.split(" "):
                G.add_edge(parent, child) 
    print(len(list(nx.all_simple_paths(G, "you", "out"))))

