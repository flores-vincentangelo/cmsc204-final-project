import csv
import os

dirname = os.path.dirname(__file__)

def get_nodes():
    node_data = {
        "node_list": [],
        "positions": {

        }
    }

    with open(os.path.join(dirname, 'nodes.csv')) as nodes_csv:
        csv_reader = csv.reader(nodes_csv, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                node_data["node_list"].append(row[0])
                node_data['positions'][row[0]] = (int(row[1]), int(row[2]))
    return node_data

def get_edges():
    edge_tuple_arr = []
    with open(os.path.join(dirname, 'edges.csv')) as edges_csv:
        csv_reader = csv.reader(edges_csv, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                edge_tuple_arr.append((row[0], row[1], float(row[2])))
    return edge_tuple_arr