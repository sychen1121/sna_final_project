import networkx as nx
import time

def build_graph():
    input_dir = "data/"
    
    graph = nx.DiGraph()
    fr = open(input_dir + "users_info_new.dat")
    hometown = list()
    
    for l in fr.readlines():
        l = l.strip('\n')
        l = l.split('\t')
        
        graph.add_node(l[0],follower_count=l[4])
        tmp = l[2]
        graph.node[l[0]]['hometown'] = list()
        
        
        item = tmp.lower()
        graph.node[l[0]]['hometown'].append(item.strip(' \"\'#*&%@$+-'))
        
        
        for spot in graph.node[l[0]]['hometown']:
            if  spot not in hometown:
                hometown.append(spot)
        
        
    return graph,sorted(hometown)