def create_checkin_info(file_path):
    """create_checkin_information from file_path"""
    import networkx as nx
    from time import time
    checkin_info = nx.Graph()    
    f = open(file_path, 'r')
    s = time()
    for line in f:
        entry = line.strip().split()
        user = int(entry[0])
        place_list = list() #visited place list
        for checkin in entry[1:]:
            place_list.append(int(checkin.split(':')[3]))
        for place in place_list: #the checkin number of visited places
            num = place_list.count(place)
            checkin_info.add_edge(user, place, num_checkin=num)
    e = time()
# to get number of checkin:
# number of chekin = checkin_info.edge[user][place]['num_checkin']
    print("time of creating:", e-s)
    return checkin_info
