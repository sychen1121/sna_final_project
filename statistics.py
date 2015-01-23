def statistics(graph, output_path):
    """compute statistics of the graph"""
    import datetime as dt
# compute time-place distribution
    time_place_dist_stat = dict()
    time_place_dist_file = open(output_path+'time_place_dist.csv', 'w')
    place_sum = 0
    checkin_sum = 0
    for i in range(24):
        time_place_dist_stat[i] = 0
    for p in graph.nodes():
        if graph.node[p]['type'] == 'place':
            place_sum +=1
            time_place_list = list() 
            hour_index = list()
            neighbors = graph.neighbors(p)
            for u in neighbors:
                time_place_list += graph.edge[p][u]['checkin_time_list']
                checkin_sum += graph.edge[p][u]['num_checkin']
            for time in time_place_list:
                t = dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
                hour_index.append(t.hour)
            for i in set(hour_index):
                time_place_dist_stat[i] += 1
    for bin, times in time_place_dist_stat.items():
        print(str(bin)+'-'+str(bin+1), times,sep=',',file=time_place_dist_file)
#        print(place_sum, checkin_sum)

# compute time_checkin distribution
    time_checkin_in_list = list() 
    time_checkin_in_dist_stat = dict()
    time_checkin_in_dist_file = open(output_path+'time_checkin_dist.csv', 'w')
    for n in graph.nodes():
        tmp = list()
        if graph.node[n]['type'] == 'user':
            neighbors = graph.neighbors(n)
            for p in neighbors:
                tmp += graph.edge[n][p]['checkin_time_list']
            time_checkin_in_list += tmp
    for i in range(24):
        time_checkin_in_dist_stat[i] = 0
    for time in time_checkin_in_list:
        t = dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        time_checkin_in_dist_stat[t.hour] += 1
    for bin, times in time_checkin_in_dist_stat.items():
        print(str(bin)+'-'+str(bin+1), times,sep=',',file=time_checkin_in_dist_file)

# compute checkin_user distribution
    checkin_user = list() 
    checkin_user_stat = dict()
    checkin_user_file = open(output_path+'checkin_user.csv', 'w')
    for n in graph.nodes():
        tmp = 0
        if graph.node[n]['type'] == 'user':
            neighbors = graph.neighbors(n)
            for p in neighbors:
                tmp += graph.edge[n][p]['num_checkin']
            checkin_user.append(tmp)
    bins = set(checkin_user)
    for b in bins:
        checkin_user_stat[b] = checkin_user.count(b)
    for bin, times in checkin_user_stat.items():
        print(bin, times,sep=',',file=checkin_user_file)

# compute checkin_place distribution
    checkin_place = list()
    checkin_place_stat = dict()
    checkin_place_file = open(output_path+'checkin_place.csv', 'w')
    for node in graph.nodes():
        if graph.node[node]['type'] == 'place':
            checkin_place.append(graph.node[node]['total_checkin'])
    bins = set(checkin_place)
    for b in bins:
       checkin_place_stat[b] = checkin_place.count(b) 
    for bin, times in checkin_place_stat.items():
        print(bin, times,sep=',',file=checkin_place_file)
