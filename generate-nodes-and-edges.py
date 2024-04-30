import csv
import os
import json

dirname = os.path.dirname(__file__)

vertical_roads = []
horizontal_roads = []
row_values = []
node_dict = {}
with open(os.path.join(dirname, 'nodes-from-map-basic.csv')) as edges2_csv:
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
                iterator += 1
            else:
                row_values[idx].append('')
vertical_roads.pop(0)

# makes a csv file simillar to the node-from-map-basic.csv
with open(os.path.join(dirname, 'nodes-from-map-advance.csv'), 'w') as write_csv_file:
    writer = csv.writer(write_csv_file)
    writer.writerow(vertical_roads)
    writer.writerows(row_values)
# write the list of nodes
f = open(os.path.join(dirname, 'nodes2.json'), 'w')
f.write('{')
for idx, (node_key, v) in enumerate(node_dict.items()):
    f.write(f'"{node_key}": {json.dumps(v)},\n')
f.write('}')
f.close()
print(f"node list count: {len(node_dict.keys())}/86") # must have 86 nodes


horizontal_time_weights = []
vertical_time_weights = []
for i in horizontal_roads:
    


# make edges
edge_dict = {}
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
        if node_bot:
            if edge_dict.get(f"{node_key}-{node_bot_key}") is None and edge_dict.get(f"{node_bot_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_bot_key}"] = {}
        if node_left:
            if edge_dict.get(f"{node_key}-{node_left_key}") is None and edge_dict.get(f"{node_left_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_left_key}"] = {}
        if node_right:
            if edge_dict.get(f"{node_key}-{node_right_key}") is None and edge_dict.get(f"{node_right_key}-{node_key}") is None:
                edge_dict[f"{node_key}-{node_right_key}"] = {}
        pass

# write the list of edges
f = open(os.path.join(dirname, 'edges2.json'), 'w')
f.write('{')
for idx, (node_key, v) in enumerate(edge_dict.items()):
    f.write(f'"{node_key}": {json.dumps(v)},\n')
f.write('}')
f.close()
print(f"edge list count: {len(edge_dict.keys())}/153")

print("done")