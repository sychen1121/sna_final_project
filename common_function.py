def create_social_graph(file_path):
    """create social network as a graph from gowalla.train.txt"""
    import networkx as nx
    from time import time
    social_graph = nx.Graph()
    file = open(file_path+'gowalla.train.txt', 'r')
    user_info = open(file_path+'users_info_new.dat', 'r')
    edge_list = list()
    not_friend_list = list()    
    s = time()
    for line in file:
        entry = line.strip().split()
        if entry[2] == '1':
            edge_list.append((int(entry[0]), int(entry[1])))
        else:
            not_friend_list.append((int(entry[0]), int(entry[1])))
    social_graph.add_edges_from(edge_list)
    for line in user_info:
        entry = line.strip().split('\t')
        user = int(entry[0])
        h = entry[2]
        fc = int(entry[4])
#        substring = line.strip().split('hometown', maxsplit=1)
#        user = int(substring[0].strip())
#        part = (substring[1].split('follower_count'))
#        h = part[0].strip()
#        fc = part[1].strip()
        social_graph.add_node(user, hometown=h, follower_count=fc)
    e = time()
    print('time for social_graph', e-s)
    return social_graph, not_friend_list

def create_checkin_info(file_path):
    """create_checkin_information from file_path"""
    import networkx as nx
    import datetime as dt
    from time import time
    checkin_info = nx.Graph()    
    checkin_file = open(file_path+'checkins_info.dat', 'r')
    s = time()
    for line in checkin_file:
        entry = line.strip().split()
        user = int(entry[0])
        for checkin in entry[1:]:
            place = (int(checkin.split(':')[3]))
            date_string = checkin.split('Z')[0]
#            checkin_time = dt.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
            checkin_time = date_string
            placeID='p'+str(place)
            if checkin_info.has_edge(user, placeID):
                num = checkin_info.edge[user][placeID]['num_checkin']
                clist = checkin_info.edge[user][placeID]['checkin_time_list']
            else:
                num = 0
                clist = list()
            if checkin_info.has_node(placeID):
                total = checkin_info.node[placeID]['total_checkin']
            else:
                total = 0
            clist.append(checkin_time)
            checkin_info.add_node(user, type='user')
            checkin_info.add_edge(user, placeID, num_checkin=num+1, checkin_time_list=clist)
            checkin_info.add_node(placeID, type='place', category=0, total_checkin=total+1, \
                    lat=0.0, lng=0.0, total_checkin_spot=0)
    e = time()
    print("time of checkin:", e-s)
# to get number of checkin:
# number of checkin = checkin_info.edge[user][place]['num_checkin']

    s = time()
    update_place_info(file_path, checkin_info)
    e = time()
    print("time of spot", e-s)

    s = time()
    update_place_entropy(checkin_info)
    e = time()
    print("time of entropy", e-s)
#    print(checkin_info.node[378468])
#    print(checkin_info.node['p378468'])
#    print(checkin_info.node['p6616040'])

    return checkin_info

def update_place_info(file_path, checkin_info):
    """update the basic information of a place to the graph"""
    spot_file = open(file_path+'spots_info.dat', 'r')
    for line in spot_file:
        entry = line.strip().split()
        placeID = 'p'+entry[0]
        cat = int(entry[2])
        total =  int(entry[4])
        latitude = float(entry[6])
        longtitude = float(entry[8])
        if checkin_info.has_node(placeID):
            checkin_info.add_node(placeID, type='place', category=cat, total_checkin_spot=total, \
                    lat=latitude, lng=longtitude)
        else:
            checkin_info.add_node(placeID, type='place', category=cat, total_checkin_spot=total, \
                    lat=latitude, lng=longtitude, total_checkin=total)

def update_place_entropy(checkin_info):
    """compute the entropy of places in the place graph"""
    for n in checkin_info.nodes():
        if checkin_info.node[n]['type'] == 'place':
            e = compute_entropy(checkin_info, n)
            checkin_info.add_node(n, entropy=e)

def compute_entropy(checkin_info, place):
    """the function compute the entropy of a place from the checkin info"""
    from math import log    
    users = checkin_info.neighbors(place)
    total_checkin = checkin_info.node[place]['total_checkin']
    entropy = 0.0
    for user in users:
        num_checkin = checkin_info.edge[user][place]['num_checkin']
        fraction = float(num_checkin/total_checkin)
        entropy += fraction * log(fraction)
    entropy *= -1
    return entropy    
def get_geocode(address):
    """obtain a geocode of an address by using google map api"""
    import googlemaps as gmaps
    client = gmaps.Client(key='AIzaSyABja4kcCMTjVLYMepiO5q2MtoWuxfK7NI')
    tmp = client.geocode(address)
    lat = float(tmp[0]['geometry']['location']['lat'])
    lng = float(tmp[0]['geometry']['location']['lng'])
    return (lat, lng)

def get_distance(origins, destinations):
    """
        obtain distances from origins to destinations
        by using google map api
        format of origins/destinations: Bobcaygeon+ON|41.43206,-81.38992|(41.43206,-81.38992)
    """
    import googlemaps as gmaps
    import json
    client = gmaps.Client(key='AIzaSyABja4kcCMTjVLYMepiO5q2MtoWuxfK7NI')
    tmp = client.distance_matrix(origins, destinations, language='en_US')
    result = dict()
    try:
        if tmp['status'] == 'OK':
            origin_addresses = tmp['origin_addresses']
            destination_addresses = tmp['destination_addresses']
            for i, row in enumerate(tmp['rows']):
                origin = origin_addresses[i]
                result[origin] = dict()
                for j, element in enumerate(row['elements']):
                    destination = destination_addresses[j]
                    if element['status'] == 'OK':
                        result[origin][destination] = int(element['distance']['value'])
                    else:
                        raise Exception
        else:
            raise Exception
    except Exception:
        print("query error")
    return result
