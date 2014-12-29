def create_checkin_info(file_path):
    """create_checkin_information from file_path"""
    import networkx as nx
    from time import time
    checkin_info = nx.Graph()    
    checkin_file = open(file_path+'checkins_info.dat', 'r')
    spot_file = open(file_path+'spots_info.dat', 'r')
    s = time()
    for line in checkin_file:
        entry = line.strip().split()
        user = int(entry[0])
        place_list = list() #visited place list
        for checkin in entry[1:]:
            place_list.append(int(checkin.split(':')[3]))
        for place in place_list: #the checkin number of visited places
            num = place_list.count(place)
            checkin_info.add_edge(user, place, num_checkin=num)
            checkin_info.add_node(place, category=0, total_checkin=0, lat=0.0, lng=0.0)
    e = time()
    print("time of checkin:", e-s)
# to get number of checkin:
# number of chekin = checkin_info.edge[user][place]['num_checkin']
    for line in spot_file:
        entry = line.strip().split()
        place = int(entry[0])
        cat = int(entry[2])
        total =  int(entry[4])
        latitude = float(entry[6])
        longtitude = float(entry[8])
        checkin_info.add_node(place, category=cat, total_checkin=total, \
                lat=latitude, lng=longtitude)
    s = time()
    print("time of spot", s-e)
    return checkin_info
