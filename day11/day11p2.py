#!/usr/bin/env python3

import networkx as nx
from concurrent.futures import ProcessPoolExecutor

def get_num_paths_between_nodes(G: nx.Graph, node1: str, node2: str) -> int:
    return len(list(nx.all_simple_paths(G, node1, node2)))

if __name__ == "__main__":
    G = nx.DiGraph()
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            parent, children_raw = line.rstrip().split(": ")
            G.add_node(parent)
            for child in children_raw.split(" "):
                G.add_edge(parent, child) 
    with ProcessPoolExecutor() as executor:
        # queue futures
        links_svr_fft_FUT = executor.submit(get_num_paths_between_nodes, G, "svr", "fft")
        links_svr_dac_FUT = executor.submit(get_num_paths_between_nodes, G, "svr", "dac")

        links_fft_dac_FUT = executor.submit(get_num_paths_between_nodes, G, "fft", "dac")
        links_dac_fft_FUT = executor.submit(get_num_paths_between_nodes, G, "dac", "fft")

        links_dac_out_FUT = executor.submit(get_num_paths_between_nodes, G, "dac", "out")
        links_fft_out_FUT = executor.submit(get_num_paths_between_nodes, G, "fft", "out")

        # retrieve results
        links_svr_fft = links_svr_fft_FUT.result()
        links_svr_dac = links_svr_dac_FUT.result()

        links_fft_dac = links_fft_dac_FUT.result()
        links_dac_fft = links_dac_fft_FUT.result()

        links_dac_out = links_dac_out_FUT.result()
        links_fft_out = links_fft_out_FUT.result()

    print(links_svr_fft * links_fft_dac * links_dac_out + links_svr_dac * links_dac_fft * links_fft_out)

