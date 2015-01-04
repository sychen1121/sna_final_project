import networkx as nx
import datetime as dt
from time import time

# create link between users
def create_social_graph(file_path):
	social_graph = nx.Graph()
	with open(file_path+'Gowalla_edges.txt','r') as fu:
		for line in fu:
			users = line.strip().split()
			usera = users[0]
			userb = users[1]
			social_graph.add_node(usera, type='user', followers=0, hometown='None')
			social_graph.add_node(userb, type='user', followers=0, hometown='None')
			social_graph.add_edge(usera, userb)
	update_user_info(file_path, social_graph)
	return social_graph


# create users, places, and links between users and places
def create_poi_graph(file_path):
	poi_graph = nx.Graph()
	user_list = list()
	place_list = list()
	user_set = set()
	place_set = set()
	# add users
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
			user_set.add(user)
			place_set.add(placeID)
			poi_graph.add_node(user, type='user')
			poi_graph.add_node(placeID, type='place', lat=latitude, lng=longtitude, total_checkin = total_checkin+1)
			poi_graph.add_edge(user, placeID, num_checkin=num_checkin+1, checkin_time_list=clist)
	user_list = sorted(list(user_set))
	place_list = sorted(list(place_set))
	update_place_info(file_path, poi_graph)

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

# make the most visited place as home
def update_user_hometown(social_graph, poi_graph):
	for node in poi_graph.nodes():
		if poi_graph.node[node]['type'] == 'user':
			if not social_graph.has_node(node):
				social_graph.add_node(node, type='user', followers=0, hometown='None')
			if social_graph.node[node]['hometown']=='None':
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
	# for node in social_graph.nodes(data=True):
		# if node[1]['hometown'] != 'None':
			# print(node)


# poi_graph, user_list, place_list = create_poi_graph('../input/Gowalla_new/POI/')
# social_graph = create_social_graph('../input/Gowalla_new/POI/')
# update_user_hometown(social_graph, poi_graph)
