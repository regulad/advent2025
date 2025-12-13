#!/usr/bin/env python3

from functools import cache

from frozendict import frozendict
import networkx as nx

if __name__ == "__main__":
    G = nx.DiGraph()
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            parent, children_raw = line.rstrip().split(": ")
            G.add_node(parent)
            for child in children_raw.split(" "):
                G.add_edge(parent, child) 
    # I tried using a naive soluition to count the number of paths between nodes, but unfortunately it was too slow
    # Going to need to use a little bit of graph theory I don't entirely comprehend.
    
    @cache
    def get_num_of_paths_to(node1: str) -> frozendict[str, int]:
        """
        Returns a dictionary of items

            N: J

        where there are J ways to reach N from node `node`.
        """
        paths_to: dict[str, int] = {}
        paths_to[node1] = 1
        # This is going to return all of the nodes in the graph. 
        # It's guaranteed that a node will NOT appear unless all of its children have already appeared.
        # This means its iterated over in topological order.
        for parent in nx.topological_sort(G):
            # This answer is more or less copied from a peer of mine while paraphrasing it to use semantics
            # that make sense to me.
            # AI EXPLANATION: 
            #     Number of paths from A to C: sum of (paths from A to B) for all nodes 
            #     B that are direct parents of C
            # My understanding: 
            #     We do this in topological order so all of the parents are processed before the children 
            #     of each parent, making the count accurate once it gets to the individual child
            for child in G.successors(parent):
                # A sucessor is a node that is a DIRECT child of a node, and not a parent of a node.
                # (A neighbor is either a parent or a child of a node)

                # I can't use += here because it's not guaranteed child is already inside
                paths_to[child] = paths_to.get(parent, 0) + paths_to.get(child, 0)
        # Frozendict needed when returning into a cache.
        return frozendict(paths_to)

    def get_num_paths_between_nodes(node1: str, node2: str) -> int:
        return get_num_of_paths_to(node1)[node2]

    links_svr_fft = get_num_paths_between_nodes("svr", "fft")
    links_svr_dac = get_num_paths_between_nodes("svr", "dac")

    links_fft_dac = get_num_paths_between_nodes("fft", "dac")
    links_dac_fft = get_num_paths_between_nodes("dac", "fft")

    links_dac_out = get_num_paths_between_nodes("dac", "out")
    links_fft_out = get_num_paths_between_nodes("fft", "out")

    print(links_svr_fft * links_fft_dac * links_dac_out + links_svr_dac * links_dac_fft * links_fft_out)

