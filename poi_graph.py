import networkx as nx
import datetime as dt
from time import time

# create user and place points
def create_poi_graph(file_path):
	poi_graph = nx.Graph()
	# add users
	with open(file_path+'Gowalla_edges.txt','r') as fu:
		for line in fu:
			users = line.strip().split()
			usera = int(users[0])
			userb = int(users[1])
			for user in users:
				poi_graph.add_node(int(user), followers=0)
			poi_graph.add_edge(usera, userb)
	# add spot and user, place link
	with open(file_path+'Gowalla_training.txt', 'r') as fi:
		for line in fi:
			entry = line.strip().split()
			user = entry[0]
			latitude = entry[2]
			longtitude = entry[3]
			place = entry[-1]
			date_string = entry[1]
			checkin_time = dt.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
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
			poi_graph.add_node(user, type='user')
			poi_graph.add_node(placeID, type='place', lat=latitude, lng=longtitude, total_checkin = total_checkin)
			poi_graph.add_edge(user, placeID, num_checkin=num_checkin+1, checkin_time_list=clist)
	print(poi_graph.nodes())
	update_user_info(file_path, poi_graph)
	update_place_info(file_path, poi_graph)

	return poi_graph

# add total checkin
def update_place_info(file_path, graph):
    """update the basic information of a place to the graph"""
    spot_file = open(file_path+'spots_info.dat', 'r')
    for line in spot_file:
        entry = line.strip().split()
        placeID = 'p'+entry[0]
        cat = int(entry[2])
        # if exist? total_checkin?
        total =  int(entry[4])
        latitude = float(entry[6])
        longtitude = float(entry[8])
        if graph.has_node(placeID):
            graph.add_node(placeID, type='place', category=cat, total_checkin_spot=total, \
                    lat=latitude, lng=longtitude)
        else:
            graph.add_node(placeID, type='place', category=cat, total_checkin_spot=total, \
                    lat=latitude, lng=longtitude, total_checkin=total)

# add hometown and followers information
def update_user_info(file_path, graph):
	user_file_name = 'users_info_new.dat'
	with open(file_path+user_file_name,'r') as user_file:
		for line in user_file:
			entry = line.strip().split('\t')
			user = int(entry[0])
			hometown = entry[2]
			follower_count = int(entry[4])
			graph.add_node(user, type='user', followers=follower_count, hometown=hometown)

# def cf_user():

# def cf_item():

poi_graph = create_poi_graph('../input/Gowalla_new/POI/')
