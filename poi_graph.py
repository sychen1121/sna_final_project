import networkx as nx
import multiprocessing as mp
import datetime as dt
import math
# from poi_recommend import write_vectors2json
# from poi_recommend import read_vectors2json
from time import time

# create link between users
def create_social_graph(file_path):
    social_graph = nx.Graph()
    s=time()
    with open(file_path+'Gowalla_edges.txt','r') as fu:
        for line in fu:
            users = line.strip().split()
            usera = users[0]
            userb = users[1]
            social_graph.add_node(usera, type='user', followers=0, hometown='None')
            social_graph.add_node(userb, type='user', followers=0, hometown='None')
            social_graph.add_edge(usera, userb)
    update_user_info(file_path, social_graph)
    e=time()
    print('time of social_graph', e-s)
    return social_graph

# create users, places and links btw users and places
def create_poi_graph_from_file(file_path):
    from time import time
    poi_graph = nx.Graph()
    user_list = list()
    place_list = list()
    s=time()
    training_file = open(file_path+'processing_Gowalla_train.txt', 'r')
    edge_list = list()
    # create user-place edge with attribute number of checkin and checkin time list
    for line in training_file:
        entry = line.strip().split()
        user = entry[0]
        placeID = entry[1]
        num_checkin = int(entry[2])
        time_list = list()
        for i in range(num_checkin):
#            checkin_time = dt.datetime.strptime(entry[3+i], "%Y-%m-%dT%H:%M:%SZ")
            checkin_time = entry[3+i]
            time_list.append(checkin_time)
        edge_list.append((user, placeID, {'num_checkin':num_checkin, 'checkin_time_list':time_list}))
    poi_graph.add_edges_from(edge_list)
    # create user list from user statistic
    user_stat = open(file_path+'user_stat.txt', 'r')
    tmp_list = list()
    for line in user_stat:
       user = line.strip().split()[0]
       total_checkin_spot = int(line.strip().split()[1])
       tmp_list.append((user, {'type':'user','total_checkin_spot': total_checkin_spot}))
       user_list.append(user)
    poi_graph.add_nodes_from(tmp_list)
    # create place list and add place info into poi_graph
    checkin_spot_stat = open(file_path+'checkin_spot_stat.txt', 'r')
    tmp_list = list()
    for line in checkin_spot_stat:
        entry = line.strip().split(',')
        placeID = entry[0]
        lat = float(entry[1])
        lng = float(entry[2])
        total_checkin = int(entry[3])
        place_list.append(placeID)
        tmp_list.append((placeID, {'type':'place','lat':lat, 'lng':lng, 'total_checkin': total_checkin}))
    poi_graph.add_nodes_from(tmp_list)
    update_place_info(file_path, poi_graph)
    e=time()
    print('time of creating poi_graph from file', e-s)

    return poi_graph, user_list, place_list
    

# create users, places, and links between users and places
def create_poi_graph(file_path):
    from time import time
    poi_graph = nx.Graph()
    user_list = list()
    place_list = list()
    user_set = set()
    place_set = set()
    # add users
    s=time()
    with open(file_path+'Gowalla_training.txt', 'r') as fi:
        for line in fi:
            entry = line.strip().split()
            user = int(entry[0])
            latitude = entry[2]
            longtitude = entry[3]
            place = entry[-1]
            #date_string = entry[1]
            #checkin_time = dt.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            checkin_time = entry[1]
            placeID = 'p'+place
            if poi_graph.has_node(placeID):
                total_checkin = poi_graph.node[placeID]['total_checkin']
            else:
                total_checkin = 0
            if poi_graph.has_edge(user, placeID):
                num_checkin = poi_graph.edge[user][placeID]['num_checkin']
                clist = poi_graph.edge[user][placeID]['checkin_time_list']
            else:
                num_checkin = 0
                clist = list()
            clist.append(checkin_time)
            user_set.add(user)
            place_set.add(placeID)
            poi_graph.add_node(user, type='user')
            poi_graph.add_node(placeID, type='place', lat=latitude, lng=longtitude, total_checkin = total_checkin+1)
            poi_graph.add_edge(user, placeID, num_checkin=num_checkin+1, checkin_time_list=clist)
    user_list = sorted(list(user_set))
    place_list = sorted(list(place_set))
    update_place_info(file_path, poi_graph)
    e=time()
    print('time of creating poi_graph', e-s)
    return poi_graph, user_list, place_list

# add total checkin
def update_place_info(file_path, graph):
    """update the basic information of a place to the graph"""
    spot_file = open(file_path+'spots_info.dat', 'r')
    for line in spot_file:
        entry = line.strip().split()
        placeID = 'p'+entry[0]
        cat = int(entry[2])
        total =  int(entry[4])
        latitude = float(entry[6])
        longtitude = float(entry[8])
        if graph.has_node(placeID):
            graph.add_node(placeID, type='place', category=cat, total_checkin_spot=total, \
                    lat=latitude, lng=longtitude)
        # need not to add place if no one have checked in there
        # else:
            # graph.add_node(placeID, type='place', category=cat, total_checkin_spot=total, \
                    # lat=latitude, lng=longtitude, total_checkin=total)

# add hometown and followers information
def update_user_info(file_path, graph):
    user_file_name = 'users_info_new.dat'
    with open(file_path+user_file_name,'r') as user_file:
        for line in user_file:
            entry = line.strip().split('\t')
            user = entry[0]
            hometown = entry[2]
            follower_count = int(entry[4])
            graph.add_node(user, type='user', followers=follower_count, hometown=hometown)
def update_hometown_geocode(social_graph, user_list):
    """transform all users' hometown to geocode"""
    import common_function as cf
    user_hometown_dict = dict()
    # count = 0
    for user in user_list:
        hometown = social_graph.node[user]['hometown']    
        if not isinstance(hometown, tuple):
            # count = count+1
            geocode = cf.get_geocode(hometown)
            social_graph.add_node(user, hometown=geocode)

# make the most visited place as home
def update_user_hometown(social_graph, poi_graph):
    s=time()
    for node in poi_graph.nodes():
        if poi_graph.node[node]['type'] == 'user':
            if not social_graph.has_node(node):
                social_graph.add_node(node, type='user', followers=0, hometown='None')
            # if social_graph.node[node]['hometown']=='None':
            neighbors = poi_graph.neighbors(node)
            checkin_nums= list()
            for n in neighbors:
                num_checkin = poi_graph.edge[node][n]['num_checkin']
                checkin_nums.append(num_checkin)
            try:
                home_checkin = max(checkin_nums)
                home = neighbors[checkin_nums.index(home_checkin)]
                hometown = (poi_graph.node[home]['lat'], poi_graph.node[home]['lng'])
                social_graph.node[node]['hometown'] = hometown
                # print(social_graph.node[node]['hometown'])
            except:
                print('really no hometown')
    e=time()
    print('time of updating hometown', e-s)
    # for node in social_graph.nodes(data=True):
        # if node[1]['hometown'] != 'None':
            # print(node)
# ===candidate====for each user=============

def spot_candidate2(social_graph, poi_graph, user_list, place_list, nprocs=8, output_path='../output/poi_recommendation/'):
    def worker(social_graph, poi_graph, users, place_list, out_q):
        user_near_places = dict()
        for user in users:
            f_lat = 0.0 
            f_lng = 0.0 

            hometown = social_graph.node[user]['hometown']
            h_lat = hometown[0]
            h_lng = hometown[1]
            checked_spots = poi_graph.neighbors(user)

            # get max lat and lng
            for spot in checked_spots:
                dc_lat = abs(poi_graph.node[spot]['lat']-h_lat)
                dc_lng = abs(poi_graph.node[spot]['lng']-h_lng)
                if dc_lat > f_lat:
                    f_lat = dc_lat
                if dc_lng > f_lng:
                    f_lng = dc_lng
            unvisited_spots = set(place_list)-set(checked_spots)
            near_spots = list()

            for public_spot in unvisited_spots:
                dp_lat = abs(poi_graph.node[public_spot]['lat']-h_lat)
                dp_lng = abs(poi_graph.node[public_spot]['lng']-h_lng)
                if dp_lat<f_lat and dp_lng<f_lng:
                    near_spots.append(public_spot)
            if len(near_spots)<500:
                f_lat = (f_lat+0.2)
                f_lng = (f_lng+0.2)

            # if dc_lat and dc_lng are too small
            near_spots = list()
            for public_spot in unvisited_spots:
                dp_lat = abs(poi_graph.node[public_spot]['lat']-h_lat)
                dp_lng = abs(poi_graph.node[public_spot]['lng']-h_lng)
                if dp_lat<f_lat and dp_lng<f_lng:
                    near_spots.append(public_spot)
            user_near_places[user] = near_spots
#            print(user, len(near_spots))
        out_q.put(user_near_places)
    # master part
    s=time()
    num_user = len(user_list)
    out_q = mp.Queue()
    chunk_size = int(math.ceil(num_user/nprocs))
    procs = []
    for i  in range(nprocs):
        if i == nprocs - 1:
            users = user_list[i*chunk_size:]
        else:
            users = user_list[i*chunk_size:(i+1)*chunk_size]
        p = mp.Process(target=worker, args=(social_graph, poi_graph, users, place_list, out_q))
        procs.append(p)
        p.start()
    user_near_places = dict()
    for i in range(nprocs):
        user_near_places.update(out_q.get())
    for p in procs:
        p.join()
    # write to a file
    out_file = open(output_path+'user_candidate_places_num.txt', 'w')
    out_file2= open(output_path+'user_candidate_places_list.txt', 'w')
    for user,candidates in user_near_places.items():
        print(user, len(candidates), file=out_file)
        print(user, end=' ', file=out_file2)
        for place in candidates:
            print(place, end=' ', file=out_file2)
        print('', file=out_file2)
#    write_vectors2json(user_near_places, output_path, 'user_near_places.txt')
    e=time()
    print('time of find spot candidates of unvisited_spots', e-s)
    return user_near_places


def geo_dist(l1,l2):
    return math.sqrt((l2[1]-l1[1])**2 + (l2[0]-l1[0])**2)
    
def spot_candidate(social_graph,poi_graph):
    candidate_userpair = dict()
    for user in social_graph.nodes():
        max_dis = 0.0
        
        location = social_graph.node[user]['hometown'] 
        checked_set = poi_graph.neighbors(user)
        
        for spot in checked_set:
            spot_location =( poi_graph.node[spot]['lat'],poi_graph.node[spot]['lng']) #lat = y, lng = x
            distance = geo_dist(location, spot_location)
            
            if distance > max_dis:
                max_dis = distance

        spot_list = checked_set
        for public_spot in poi_graph.nodes():
            if poi_graph.node[public_spot]['type'] == 'user':
                continue
            elif public_spot in checked_set:
                continue
            else:
                p_location = (poi_graph.node[public_spot]['lat'],poi_graph.node[public_spot]['lng'])
                p_dis = geo_dist(location, p_location)
                if p_dis <= max_dis:
                    spot_list.append(public_spot)
        
        candidate_userpair[user] = spot_list
        
    write_vectors2json(candidate_userpair, "../output/poi_recommendation/", "candidate_spot")


