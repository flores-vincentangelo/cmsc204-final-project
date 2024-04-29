import csv
import os
import json

dirname = os.path.dirname(__file__)
node_dict = {}
with open(os.path.join(dirname, 'nodes.csv')) as nodes_csv:
    csv_reader = csv.reader(nodes_csv, delimiter=',')
    for idx, row in enumerate(csv_reader):
        if idx != 0:
            if row[0] in node_dict:
                pass
            else:
                node_dict[row[0]] = {}
                node_dict[row[0]]["nodes"] = []

edge_tuple_arr = []
with open(os.path.join(dirname, 'edges.csv')) as edges_csv:
    csv_reader = csv.reader(edges_csv, delimiter=',')
    for idx, row in enumerate(csv_reader):
        if idx != 0:
            edge_tuple_arr.append((row[0], row[1], row[2]))

vertical_roads = []
horizontal_roads = []
row_values = []
node_list = []
with open(os.path.join(dirname, 'nodes-from-map-basic.csv')) as edges2_csv:
    csv_reader2 = csv.reader(edges2_csv, delimiter=',')
    iterator = 1
    for idx, row in enumerate(csv_reader2):
        row_values.append([])
        for idx2, column_val in enumerate(row):
            if idx == 0:
                vertical_roads.append(column_val)
            
            if idx2 == 0:
                horizontal_roads.append(column_val)
                row_values[idx].append(column_val)
                continue
            if column_val == 'x':
                h = horizontal_roads[idx]
                v = vertical_roads[idx2]
                id =  iterator
                node_object = {
                    "h": h, "v": v, "id": id
                }

                if h == 'B1' and (v == "V2" or v == "V1"):
                    continue
                elif v == "B1" and (h == "H1" or h == "H4"):
                    continue
                elif (h == "H1" and v == "V2") or (h == "H4" and v == "V1"):
                    node_object["b"] = "B1"
                    pass
                row_values[idx].append(f'{node_object['h']}-{node_object['v']}')
                node_list.append(node_object)
                iterator += 1
            else:
                row_values[idx].append('')
    print(vertical_roads)



with open(os.path.join(dirname, 'nodes-from-map-advance.csv'), 'w') as write_csv_file:
    writer = csv.writer(write_csv_file)
    writer.writerow(vertical_roads)
    writer.writerows(row_values)

f = open(os.path.join(dirname, 'nodes2.json'), 'w')
f.write('{')
for idx, element in enumerate(node_list):
    f.write(f'"{idx + 1}": {json.dumps(element)},\n')
f.write('}')
f.close()

# print(edge_tuple_arr)
# print(json.dumps(node_dict,sort_keys=True, indent=4))

# edges = [('A', 'B', 2), ('A', 'C', 5), ('B', 'D', 3), ('B', 'E', 7),
#              ('C', 'F', 4), ('D', 'G', 2), ('E', 'H', 1), ('F', 'H', 6),
#              ('G', 'H', 3), ('A', 'F', 1), ('C', 'D', 2), ('E', 'G', 5)]
# node_dict2 = {}
# for edge in edges:
#     print(f"{edge[0]},{edge[1]},{edge[2]}")
# for edge in edges:
#     if edge[0] in node_dict2:
#         pass
#     else:
#         node_dict2[edge[0]] = {}

#     if edge[1] in node_dict2:
#         pass
#     else:
#         node_dict2[edge[1]] = {}
    
#     if edge[1] in node_dict2[edge[0]]:
#             pass
#     else:
#         node_dict2[edge[0]][edge[1]] = {}

#     if edge[0] in node_dict2[edge[1]]:
#             pass
#     else:
#         node_dict2[edge[1]][edge[0]] = {}
# print(json.dumps(node_dict2,sort_keys=True, indent=4))