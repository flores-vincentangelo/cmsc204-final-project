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
node_dict = {}
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
                val = vertical_roads[idx2]
                id =  iterator
                node_object = {
                    "h": h, "v": val, "id": id
                }

                if h == 'B1' and (val == "V2" or val == "V1"):
                    continue
                elif val == "B1" and (h == "H1" or h == "H4"):
                    continue
                elif (h == "H1" and val == "V2") or (h == "H4" and val == "V1"):
                    node_object["b"] = "B1"
                    pass
                
                key = f"{h}{val}"
                key += node_object["b"] if "b" in node_object else ''
                  

                row_values[idx].append(f'{node_object['h']}-{node_object['v']}')
                node_dict[key] = node_object
                iterator += 1
            else:
                row_values[idx].append('')

# makes a csv file simillar to the node-from-map-basic.csv
with open(os.path.join(dirname, 'nodes-from-map-advance.csv'), 'w') as write_csv_file:
    writer = csv.writer(write_csv_file)
    writer.writerow(vertical_roads)
    writer.writerows(row_values)

# write the list of nodes
f = open(os.path.join(dirname, 'nodes2.json'), 'w')
f.write('{')
for idx, (node_key, val) in enumerate(node_dict.items()):
    f.write(f'"{node_key}": {json.dumps(val)},\n')
f.write('}')
f.close()
print(f"node list count: {len(node_dict.keys())}/86") # must have 86 nodes


# make edges
edge_list = []
edge_dict = {}
for idx, (node_key, val) in enumerate(node_dict.items()):
    h_name = val["h"][0]
    h_number = int(val["h"].split(h_name)[1])
    v_name = val["v"][0]
    v_number = int(val["v"].split(v_name)[1])
    id = val["id"]
    b = int(val["b"][1]) if "b" in val else None

    node_top_key = f"{h_name}{h_number - 1}{val["v"]}"
    node_bot_key = f"{h_name}{h_number + 1}{val["v"]}"
    node_left_key = f"{val["h"]}{v_name}{v_number - 1}"
    node_right_key = f"{val["h"]}{v_name}{v_number + 1}"

    node_top = node_dict[node_top_key] if node_top_key in node_dict else None
    node_bot = node_dict[node_bot_key] if node_bot_key in node_dict else None
    node_left = node_dict[node_left_key] if node_left_key in node_dict else None
    node_right = node_dict[node_right_key] if node_right_key in node_dict else None

    if node_top:
        if edge_dict.get(f"{node_key}-{node_top_key}") is None and edge_dict.get(f"{node_top_key}-{node_key}") is None:
            edge_dict[f"{node_key}-{node_top_key}"] = {}
    if node_bot:
        if edge_dict.get(f"{node_key}-{node_bot_key}") is None and edge_dict.get(f"{node_bot_key}-{node_key}") is None:
            edge_dict[f"{node_key}-{node_bot_key}"] = {}
    if node_left:
        if edge_dict.get(f"{node_key}-{node_left_key}") is None and edge_dict.get(f"{node_left_key}-{node_key}") is None:
            edge_dict[f"{node_key}-{node_left_key}"] = {}
    if node_right:
        if edge_dict.get(f"{node_key}-{node_right_key}") is None and edge_dict.get(f"{node_right_key}-{node_key}") is None:
            edge_dict[f"{node_key}-{node_right_key}"] = {}

# write the list of edges
f = open(os.path.join(dirname, 'edges2.json'), 'w')
f.write('{')
for idx, (node_key, val) in enumerate(edge_dict.items()):
    f.write(f'"{node_key}": {json.dumps(val)},\n')
f.write('}')
f.close()
print(f"edge list count: {len(edge_dict.keys())}/153")

print("done")
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