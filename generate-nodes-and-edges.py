import csv
import os
import json
import random

dirname = os.path.dirname(__file__)



def generate_pos(h, v):
    pos_mapping = {
    "h": {
        "H12": 0,
        "H11": 1,
        "H10": 2,
        "H9": 3,
        "H8": 4,
        "H7": 5,
        "H6": 6,
        "H5": 7,
        "H4": 8,
        "H3": 9,
        "H2": 10,
        "H1": 11,
    },
    "v": {
        "H7": 0,
        "H6": 1,
        "V1": 2,
        "H3": 3,
        "H2": 4,
        "V2": 5,
        "V3": 6,
        "V4": 7,
        "V5": 8,
        "V6": 9,
        "V7": 10,
        "V8": 11,

    }
}
    if v == "B1":
        return (pos_mapping["v"][h], pos_mapping["h"][h])
    else:
        return (pos_mapping["v"][v], pos_mapping["h"][h])
                    

vertical_roads = []
horizontal_roads = []
row_values = []
node_dict = {}
pos_dict = {}
with open(os.path.join(dirname, 'tmp/nodes-from-map-basic.csv')) as edges2_csv:
    csv_reader2 = csv.reader(edges2_csv, delimiter=',')
    iterator = 1
    for idx, row in enumerate(csv_reader2):
        row_values.append([])

        if idx == 0:
            vertical_roads = row
            continue

        for idx2, column_val in enumerate(row):
                        
            if idx2 == 0:
                horizontal_roads.append(column_val)
                row_values[idx].append(column_val)
                continue
            if column_val == 'x':
                h = horizontal_roads[idx - 1]
                v = vertical_roads[idx2]
                id =  iterator
                node_object = {
                    "h": h, "v": v, "id": id
                }

                if v == "B1" and (h == "H1" or h == "H4"):
                    continue
                elif (h == "H1" and v == "V2") or (h == "H4" and v == "V1"):
                    node_object["b"] = "B1"
                
                key = f"{h}{v}"
                key += node_object["b"] if "b" in node_object else ''
                
                row_values[idx].append(f'{node_object['h']}-{node_object['v']}')
                node_dict[key] = node_object
                pos = generate_pos(h, v)
                pos_dict[key] = pos
                iterator += 1
            else:
                row_values[idx].append('')
vertical_roads.pop(0)

# makes a csv file simillar to the node-from-map-basic.csv
with open(os.path.join(dirname, 'tmp/nodes-from-map-advance.csv'), 'w') as write_csv_file:
    writer = csv.writer(write_csv_file)
    writer.writerow(vertical_roads)
    writer.writerows(row_values)

# write the list of nodes
f = open(os.path.join(dirname, 'tmp/nodes_dict.json'), 'w')
f.write('{')
for idx, (node_key, v) in enumerate(node_dict.items()):
    f.write(f'"{node_key}": {json.dumps(v)},\n')
f.write('}')
f.close()
print(f"node list count: {len(node_dict.keys())}/86") # must have 86 nodes

# make final nodes.csv file
f = open(os.path.join(dirname, 'nodes.csv'), 'w')
f.write('nodes,x,y\n')
for key in node_dict.keys():
    f.write(f"{key},{pos_dict[key][0]},{pos_dict[key][1]}\n")
f.close()

horizontal_time_weights = []
vertical_time_weights = []
b_time_weight = random.randint(1,10)
for i in horizontal_roads:
    horizontal_time_weights.append(random.randint(1,10))
for i in vertical_roads:
    vertical_time_weights.append(random.randint(1,10))


# make edges
edge_dict = {}
edge_list = []
for idx, h in enumerate(horizontal_roads):
    for idx2, v in enumerate(vertical_roads):

        h_top = horizontal_roads[idx - 1] if idx - 1 >= 0 else None
        h_bot = horizontal_roads[idx + 1] if idx + 1 < len(horizontal_roads) else None
        v_left = vertical_roads[idx2 - 1] if idx2 - 1 >= 0 else None
        v_right = vertical_roads[idx2 + 1] if idx2 + 1 < len(vertical_roads) else None
        
        def check_special_case(test_string):
            if test_string == "H1V2" or test_string == "H4V1":
                return test_string + "B1"
            else:
                return test_string

        node_key = check_special_case(h+v)
        node_top_key = check_special_case(f"{h_top}{v}")
        node_bot_key = check_special_case(f"{h_bot}{v}")
        node_left_key = check_special_case(f"{h}{v_left}")
        node_right_key = check_special_case(f"{h}{v_right}")
        
        node = node_dict[node_key] if node_key in node_dict else None
        node_top = node_dict[node_top_key] if node_top_key in node_dict else None
        node_bot = node_dict[node_bot_key] if node_bot_key in node_dict else None
        node_left = node_dict[node_left_key] if node_left_key in node_dict else None
        node_right = node_dict[node_right_key] if node_right_key in node_dict else None



        edge_dict.setdefault("H2B1-H1V2B1",{})
        edge_dict.setdefault("H2B1-H2V2",{})
        edge_dict.setdefault("H3B1-H4V1B1",{})
        edge_dict.setdefault("H3B1-H3V2",{})
        edge_dict.setdefault("H4V1B1-H6B1",{})

        if node is None:
            continue
        if node_top:
            if edge_dict.get(f"{node_key}-{node_top_key}") is None and edge_dict.get(f"{node_top_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_top_key}"] = {}
                edge_list.append([node_key, node_top_key, vertical_time_weights[idx2]])
        if node_bot:
            if edge_dict.get(f"{node_key}-{node_bot_key}") is None and edge_dict.get(f"{node_bot_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_bot_key}"] = {}
                edge_list.append([node_key, node_bot_key, vertical_time_weights[idx2]])
        if node_left:
            if edge_dict.get(f"{node_key}-{node_left_key}") is None and edge_dict.get(f"{node_left_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_left_key}"] = {}
                edge_list.append([node_key, node_left_key, horizontal_time_weights[idx]])
        if node_right:
            if edge_dict.get(f"{node_key}-{node_right_key}") is None and edge_dict.get(f"{node_right_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_right_key}"] = {}
                edge_list.append([node_key, node_right_key, horizontal_time_weights[idx]])
        pass
edge_list.append(["H2B1", "H1V2B1", b_time_weight])
edge_list.append(["H2B1", "H2V2", b_time_weight])
edge_list.append(["H3B1", "H4V1B1", b_time_weight])
edge_list.append(["H3B1", "H3V2", b_time_weight])
edge_list.append(["H4V1B1", "H6B1", b_time_weight])
# write the list of edges
f = open(os.path.join(dirname, 'tmp/edges_dict.json'), 'w')
f.write('{')
for idx, (node_key, v) in enumerate(edge_dict.items()):
    f.write(f'"{node_key}": {json.dumps(v)},\n')
f.write('}')
f.close()
print(f"edge list count: {len(edge_dict.keys())}/153")

print(f"edge list count: {len(edge_list)}/153")
f = open(os.path.join(dirname, 'edges.csv'), 'w')
f.write('start_node,end_node,weight\n')
for element in edge_list:
    f.write(f"{element[0]},{element[1]},{element[2]}\n")
f.close()

print("done")