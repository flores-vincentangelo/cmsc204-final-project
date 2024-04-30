import csv
import os

dirname = os.path.dirname(__file__)

def get_nodes():
    node_list = []
    with open(os.path.join(dirname, 'nodes.csv')) as nodes_csv:
        csv_reader = csv.reader(nodes_csv, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                node_list.append(row[0])
    return node_list

def get_edges():
    edge_tuple_arr = []
    with open(os.path.join(dirname, 'edges.csv')) as edges_csv:
        csv_reader = csv.reader(edges_csv, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                edge_tuple_arr.append((row[0], row[1], int(row[2])))
    return edge_tuple_arr