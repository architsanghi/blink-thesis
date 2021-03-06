import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import pydotplus

# filename = "./dot files/09-Traceroutable/traceroutable.json"
# filename = "./dot files/03-L2_Flooding/Other ports/l2_flooding_other_ports.json"
# filename = "./dot files/02-Repeater/repeater_without_table.json"
# filename = "./dot files/11-Packet-Loss-Detection/loss-detection.json"
# filename = "./firewall_tofino/prog_firewall_tofino.p4"


def activate_node(g, start_node):          
    stack = [start_node]

    while stack:
        node = stack.pop()
        preds = g.predecessors(node)
        stack += preds
        print('%s -> %s' % (node, preds))


def print_details(data):
    if isinstance(data,(list, tuple,set)):
        for i in data:
            print("\t",i)
    elif isinstance(data,dict):
        for i in data.keys():
            print("\t",i," : ",data[i])

def extract_actions(filename):
    data = None
    action_list = []
    with open(filename, 'r') as f:
        data = json.load(f)

    for action in data['actions']:
        action_list.append(action['name'])
    
    action_list = list(set(action_list))
    return action_list

def extract_tables_actions(filename):
    data = None
    name_to_action = {}
    with open(filename, 'r') as f:
        data = json.load(f)

    for name in data['pipelines']:
        for table in name["tables"]:
            if "ingress" in table["name"]:
                name_to_action[table["name"]] =  [x for x in table["actions"]]
                
    # print("Number of tables")
    # print((name_to_action))
    return name_to_action

def extract_nodename_condition(filename):
    """This function creates dictionary of node
    names with its corresponding conditions."""
    data = None
    node_to_condition_map = {}
    with open(filename, 'r') as f:
        data = json.load(f)
    node_to_condition_map = {}
    for name in data['pipelines']:
        for condition in name['conditionals']:
            if 'source_info' in condition.keys():
                node_to_condition_map[condition['name']] = condition['source_info']['source_fragment']
    
  
    return node_to_condition_map

def extract_tables_next_actions(filename):
    """This Function extracts NEXT_ACTIONS associated with
     the table from json file."""
    data = None
    table_to_next_action = {}
    with open(filename, 'r') as f:
        data = json.load(f)

    for name in data['pipelines']:
        for table in name["tables"]: 
            table_to_next_action[table['name']] = table['next_tables']

    # print("@@@@: ",table['name'], ": @@@@:",table['next_tables'])
    # print("next action of tables are")
    # print((table_to_next_action))
    # print("ending next action here")
    return table_to_next_action

def extract_conditionals(filename):
    """This function creates dictionary of conditionals with its 
    corresponding next actions based on the condition 
    evaluation "True or False"."""
    data = None
    with open(filename, 'r') as f:
        data = json.load(f)

    conditions_to_nextstep = {}
    for name in data['pipelines']:
        for condition in name['conditionals']:
            if 'source_info' in condition.keys():
                conditions_to_nextstep[condition['name']] = {'true_next':condition['true_next'],'false_next':condition['false_next']}
                # conditions_to_nextstep[condition['source_info']['source_fragment']] = {'true_next':condition['true_next'],'false_next':condition['false_next']}
                # conditions_to_nextstep[condition['name'] = {'true_next':condition['true_next'],'false_next':condition['false_next']}
    return conditions_to_nextstep

##############################
#### START CREATING NODES ####
##############################

# def create_nodes(filename):
#     nodes = []
#     table_actions = extract_tables_actions(filename)
#     conditionals_nextstep = extract_conditionals(filename)

#     for conditional in conditionals_nextstep.keys():
#         if conditional not in nodes:
#             nodes.append(conditional)
#     for table in table_actions.keys():
#         if table not in nodes:
#             nodes.append(table)
#     for ac in table_actions.values():
#         if not isinstance(ac,(tuple,set,list)):
#             nodes.append(ac)
#         else:
#             for acc in ac:
#                 nodes.append(acc)
#     # Removing Duplicates:
#     nodes = list(set(nodes))
#     print("total number of nodes are")
#     print(len(nodes))
#     return nodes

##############################
#### END CREATING NODES ####
##############################

#This is a utility function. Input: Dictionary
# Returns: list of keys and values where value != None
def get_notNone_values(data):
    val = []
    key = []
    for k in data.keys():
        if data[k] is not None and data[k] != 'None' and (data[k] != 'Null' and data[k] != 'null'):
            val.append(data[k])
            key.append(k)
    
    # print("\n\t # get_notNone_values: ")
    # print_details(data)
    # print(key,val)
    return key, val
##############################
#### START CREATING EDGES ####
##############################
switch_case = {}
def create_edges(filename):
    edges = []
    # Table_actions contains names of all programmer tables
    table_actions = extract_tables_actions(filename)
    #table_next_actions contains next hop for every table 
    table_next_actions = extract_tables_next_actions(filename)
    #nodename_condition maps node name to conditional step of tables.
    nodename_condition = extract_nodename_condition(filename)
    #conditional_nextstep points to next table according to condition(true_next,false_next)
    conditionals_nextstep = extract_conditionals(filename)
    # print("Start TOTAL NUMBER OF DISTINCT NODES ")
    # print(len(table_next_actions))
    # print("Ending TOTAL NUMBER OF DISTINCT NODES ")
    for key in conditionals_nextstep.keys():
        if isinstance(conditionals_nextstep[key]['true_next'],(list, set, tuple)):
            for k1 in conditionals_nextstep[key]['true_next']:
                if k1 is not None and key != 'NoAction':
                    edges.append({"src":key,"dst":k1,"weight":0})
        else:
            if conditionals_nextstep[key]['true_next'] is not None and key != 'NoAction':
                edges.append({"src":key,"dst":conditionals_nextstep[key]['true_next'],"weight":0})

        if isinstance(conditionals_nextstep[key]['false_next'],(list, set, tuple)):
            for k1 in conditionals_nextstep[key]['false_next']:
                if k1 is not None and key != 'NoAction':
                    edges.append({"src":key,"dst":k1,"weight":0})
        else:
            if conditionals_nextstep[key]['false_next'] is not None and key != 'NoAction':
                edges.append({"src":key,"dst":conditionals_nextstep[key]['false_next'],"weight":0})

    """If Switch case is used we have to extract it from Next_action of the table."""
    #  Maps table names to their respective actions just for programmer tables.
    for key in table_next_actions.keys():
        if "ingress" in key:
            if key in table_actions.keys():
                for ac in table_actions[key]:
                    if key != 'NoAction':
                        edges.append({'src':key, 'dst':ac, 'weight':0})


    # table_next_actions = extract_tables_next_actions(filename)
    # print("\n\tSwitch Case@@: ", table_next_actions)
    

    for key in table_next_actions.keys():
        vals = []
        keys, vals = get_notNone_values(table_next_actions[key])
        for k,v in zip(keys, vals):

            # edges.append({'src':k, 'dst':v, 'weight':0})
            # print("\n\t@@Keys:",k,"\n\t@@vals:",v)
            ##Write code if there are multiple values in "k"

            if "ingress" in k and (k!=v):
                edges.append({'src':k, 'dst':v, 'weight':0})
                switch_case[key] = {'src':k, 'dst':v, 'weight':0}
            else:
                edges.append({'src':key, 'dst':v, 'weight':0})
                switch_case[key] = {'src':key, 'dst':v, 'weight':0}

    """Replace Node name in the edges with exact P4 code snippet."""
    # print("total edges before are",len(edges))

    #Remove such elements with similar 'src' and 'dst'
    for e in edges:    
        if e['src'] == e['dst']:
            # print("\n\t@@@@ BEFORE: ",edges)
            edges.remove(e)
            # print("\n\t@@@@ AFTER: ",edges)
    print("total edges after are",len(edges))
    return edges

##############################
##### END CREATING EDGES #####
##############################

def create_cfg(filename):

    # nodes = create_nodes(filename)
    nodes = []
    # print(filename)
    weighted_edges = create_edges(filename)    
    edge_list = []

    for e in weighted_edges:
        edge_list.append((e["src"], e["dst"], e["weight"]))
    
    """Remove duplicate edges"""
    edge_list = list(set(edge_list))

    # print("total number of edges are ")
    # print(len(edge_list))

    """Remove such elements with similar 'src' and 'dst'."""
    for e in edge_list:
        if e[0] == e[1]:
            edge_list.remove(e)

    for e in edge_list:
        nodes.append(e[0])
        nodes.append(e[1])
    # print("end printing edges")
    nodes = list(set(nodes))

    print("Total Nodes/states in graph are", len(nodes))
    

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edge_list)

   

    h=G.to_undirected()
    # print(nx.is_connected(h))

    #Graph Layout
    # pos = nx.shell_layout(G) 
    nx.draw_shell(G, with_labels = True, arrows=True) 
    plt.show()
   

    # print("\n\t Nodes: ")
    # print_details(nodes)

    # print("\n\t Weighted Edges: ",type(edge_list))
    # print_details(edge_list)

    # cycle = nx.find_cycle(G)
    # print("\n\t cycle: ",cycle)

    # print("total number of edges are", len(edge_list))
 


    
    topological_order = list(nx.topological_sort(G))
    rev_topological_order = list(reversed(list(nx.topological_sort(G))))

    # print(topological_order)
    # print(len(topological_order))
    

    # print(topological_order)
    leaf_vertex = [v for v, d in G.out_degree() if d == 0]
    start_vertex = [v for v, d in G.in_degree() if d==0]

    print("leaf vertices are", leaf_vertex)

    print("\n")
    print("\n")

    print("start vertex is",start_vertex)

    print("\n")
    print("\n")


    path_list = []    



    ####################################
    #### START BALL-LARUS ALGORITHM ####
    ####################################


    weighted_edges = []
    for e in edge_list:
        weighted_edges.append({'src':e[0], 'dst':e[1], 'weight':e[2]})

    num_path = {}
    for v in rev_topological_order:
        if v in leaf_vertex:
            num_path[v] = 1
        else:
            num_path[v] = 0
            for e in G.out_edges(v):
                ind = weighted_edges.index({'src':e[0], 'dst':e[1],'weight': 0})
                weighted_edges[ind]['weight'] = num_path[v]
                num_path[v] = num_path[v] + num_path[e[1]]

    ####################################
    #### END BALL-LARUS ALGORITHM ######
    ####################################

    
    # print("entering here")
    pos_w=0
    max_path_weight_possible=0
    for i in weighted_edges:
        if i['weight']>0:
            pos_w=pos_w + 1
            print(i)
    
    print("Number of positive weight edges are",pos_w)
    # max_path_length= -1
    # min_path_length= 10000
    # min_path=[]
    # max_path=[]
    # for i in path_list:
    #     if len(i)>max_path_length:
    #         max_path_length=len(i)
    #         max_path=i
    #     if len(i)<min_path_length:
    #         min_path_length=len(i)
    #         min_path=i

    # for i in weighted_edges:
    #     print(i)
        



    # print("Minimum Path length is", min_path)
    # print("Maximum Path length is ",max_path)

    return weighted_edges, G

# weighted_edges, graph = create_cfg(filename)

def augmentor(p4_filename, json_filename):
    import re
    # print(json_filename)
    # jsonfile = "./dot files/03-L2_Flooding/Other ports/l2_flooding_other_ports.json"
    # jsonfile = "./dot files/09-Traceroutable/traceroutable.json"
    jsonfile = json_filename

    weighted_edges, graph = create_cfg(jsonfile)



    actions = extract_actions(jsonfile)
    tables = extract_tables_actions(jsonfile)
    conditions = extract_conditionals(jsonfile)

    # print("\n\tTables :")
    # print(tables.keys())

    # print("\n\tConditions :")
    # print(conditions.keys())

    # print("\n\t@@Weighted Edges :")
    # print_details(weighted_edges)

    # print("\n\tSwitch Case:", switch_case)
    


    # data = None
    # with open(p4_filename, 'r') as f:
    #     data = f.read()
    #     new_data = data
    #     nodes_and_weights = {}

    #     index_metadata = new_data.find('{', new_data.find('struct metadata')) + 1
    #     meta_data = "\n\tbit<16> BL; \n"
    #     new_data = new_data[0:index_metadata] + meta_data + new_data[index_metadata+1:]

    #     for we in weighted_edges:
    #         src = we['src']
    #         dst = we['dst']

    #         weight = int(we['weight'])

    #         #If the "src" Node is an action then annotate the BL valriable to the Action.
    #         if src in actions:
    #             # if 'NoAction' in src:
    #             #     continue
    #             nodes_and_weights[src] = weight
    #             if len(src.split('.')) > 1:
    #                 src = src.split('.')[1]
    #                 search_string = "action "+ str(src)
    #             else:
    #                 search_string = "action "+ str(src)

    #             annotate_string = "\n\t ig_md.BL = ig_md.BL + "+str(weight)+";\n"

    #             if new_data.find(search_string) != -1 and int(weight) > 0:
    #                 req_ind = new_data.find('{', new_data.find(search_string)) + 1
    #                 new_data = new_data[0:req_ind] + annotate_string + new_data[req_ind+1:]
    #             # print("\n\tindex: ",req_ind," : ", src)
    #         #If the "dst" Node is an action then annotate the BL valriable to the Action.
    #         elif dst in actions:
    #             # if 'NoAction' in dst:
    #             #     continue
    #             nodes_and_weights[dst] = weight
    #             if len(dst.split('.')) > 1:
    #                 dst = dst.split('.')[1]
    #                 search_string = "action "+ str(dst)
    #             else:
    #                 search_string = "action "+ str(dst)
    #             annotate_string = "\n\t\t ig_md.BL = ig_md.BL + "+str(weight)+";\n"
    #             if new_data.find(search_string) != -1 and int(weight) > 0:
    #                 req_ind = new_data.find('{', new_data.find(search_string)) + 1
    #                 new_data = new_data[0:req_ind] + annotate_string + new_data[req_ind+1:]
    #         elif src in conditions.keys() and dst in tables.keys():
    #             search_string = src
    #             nodes_and_weights[src] = weight
    #             annotate_string = "\n\telse{ ig_md.BL = ig_md.BL + "+str(weight)+";}\n"
    #             req_ind = new_data.find(search_string) + len(search_string)-1
    #             req_ind = new_data.find(search_string, req_ind)
    #             req_ind = new_data.find("}", req_ind)
    #             if int(weight) > 0:
    #                 new_data = new_data[0:req_ind+1] + annotate_string + new_data[req_ind+1:]
    #         elif src in conditions.keys():
    #             search_string = src
    #             nodes_and_weights[src] = weight
    #             # annotate_string = "\n\t\t ig_md.BL = ig_md.BL + "+str(weight)+";\n"
    #             # req_ind = new_data.find(search_string) + len(search_string)-1
    #             # req_ind = new_data.find(search_string, req_ind)
    #             # req_ind = new_data.find("{", req_ind)
    #             # if int(weight) > 0:
    #             #     new_data = new_data[0:req_ind] + annotate_string + new_data[req_ind+1:]
                    
    #             # print("\n\treq_ind: ", req_ind, "\t search_string: ", search_string)
    #         else:
    #             print("you have to change this part")
    




    # print("\n\t nodes_and_weights: ")
    # print_details(nodes_and_weights)
    

    # topological_order = list(nx.topological_sort(graph))    
    # leaf_vertex = [v for v, d in graph.out_degree() if d == 0]
    # path_list = []
    # path_number=0
    # for leaf in leaf_vertex:
    #     for path in nx.all_simple_paths(graph, source='tbl_main150', target=leaf ):
    #     	path_number= path_number + 1
    #     	print(path_number)
    #     	path_list.append(path)

    # print("\n\t path_list: ")
    # print_details(path_list)
   

    # path_weight = {}
    # count = 0
    # for path in path_list:
    #     w = 0
    #     dest_leaf="none"
    #     for p in path:
    #         dest_leaf=p
    #         if p in nodes_and_weights:
    #             w = w + nodes_and_weights[p]
    #         else:
    #             w = w + 0
    #     path_weight[count] = {'path':path, 'weight':w}
    #     # print(w,dest_leaf,path)
    #     count = count+1


    # print(nodes_and_weights['nh_avaibility_2_tmp == 1w0'])

    # u'nh_avaibility_2_tmp == 1w0', u'nh_avaibility_3_tmp == 1w0
    
    # for we in weighted_edges:
    #     src = we['src']
    #     dst = we['dst']
    #     if src=='nh_avaibility_2_tmp == 1w0' and dst=='nh_avaibility_3_tmp == 1w0':
    #         weight = int(we['weight'])
    #         print("weight is",weight)
    #         print("this is",nodes_and_weights['nh_avaibility_3_tmp == 1w0'])

    # count=0
    # check_ball_larus_encoding=[]
    # for path in path_list:
    #     w = 0
    #     length=len(path)-1
    #     for i in range(length):
    #         weight_to_add=0
    #         for we in weighted_edges:
    #             src = we['src']
    #             dst = we['dst']
    #             weight = int(we['weight'])
    #             if src==path[i] and dst==path[i+1]:
    #                 weight_to_add=weight
    #                 break

    #         w = w + weight_to_add
    #     check_ball_larus_encoding.append(w)

    pos_weights=0;
    zero_weights=0;

    # print("TOTAL NUMBER OF PATHS ARE", len(path_list))

    for we in weighted_edges:
        src = we['src']
        dst = we['dst']
        weight = int(we['weight'])
        if weight>0:
            pos_weights= pos_weights + 1;
        else:
            zero_weights= zero_weights + 1;

    # print(pos_weights)
    # print(zero_weights)


    
    # original_length=len(check_ball_larus_encoding)
    # set_original_list=set(check_ball_larus_encoding)
    # set_length=len(set_original_list)

    # print(check_ball_larus_encoding)




    # print("\n\t path_weight: ")
    # print_details(path_weight)
 
jsonfile = "./main.json"
p4filename = "./main_before_aug.p4"
# p4filename = "./dot files/09-Traceroutable/traceroutable.p4"
augmentor(p4filename, jsonfile)