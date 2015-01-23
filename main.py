import common_function as cf
import poi_graph as poi
#import poi_recommend as poi_r
import feature as ft
import multiprocessing as mp
import math
from time import time
from sys import argv
import common_stat as cs
def writeFeature(f, label, feature_list):
    """create label and feature to a file"""
    for feature in feature_list:
        if label == -1:
            for i in range(len(feature)):
                if i == len(feature)-1:
                    print(feature[i], file=f)
                else:
                    print(feature[i], end=',', file=f)
        else:
            print(label, end=',', file=f)
            for i in range(len(feature)):
                if i == len(feature)-1:
                    print(feature[i], file=f)
                else:
                    print(feature[i], end=',', file=f)
def computeFeature(social_graph, checkin_graph, edges_list, nprocs, popular_places):
    """using multiprocessing to speed up feature computation"""
    s = time()
    num_edge = len(edges_list)
    out_q = mp.Queue()
    chunk_size = int(math.ceil(num_edge/nprocs))
    procs = []
    for i  in range(nprocs):
        if i == nprocs - 1:
            edges = edges_list[i*chunk_size:]
        else:
            edges = edges_list[i*chunk_size:(i+1)*chunk_size]
        p = mp.Process(target=worker, args=(social_graph, checkin_graph, edges, out_q, popular_places))
        procs.append(p)
        p.start()
    feature_list = list()
    for i in range(nprocs):
        feature_list += (out_q.get())
    for p in procs:
        p.join()
    e = time()
    print("time of feature:", e-s)
    return feature_list

def worker(social_graph, checkin_graph, edges, out_q, popular_places):
    out_list = list()
    for edge in edges:
        n1 = edge[0]
        n2 = edge[1]
        result  = ft.social_feature(social_graph, n1, n2)
        result += ft.place_feature(checkin_graph, n1, n2)
        result += ft.temporal_place_feature(checkin_graph, n1, n2, popular_places)
        if len(edge) == 3:
            answer = edge[2]
            out_list.append((answer,n1,n2)+result)
        else:
            out_list.append((n1,n2)+result)
    out_q.put(out_list)

if __name__ == '__main__':
    input_path = argv[1]
    output_path = argv[2]
    nprocs = int(argv[3])
    command = argv[4]
# command execution
    if command == 'train': # compute train features
# initialize 
        social_graph, not_friend_list = cf.create_social_graph(input_path)
        checkin_graph = cf.create_checkin_info(input_path, social_graph)
        popular_places = cf.get_popular_places(checkin_graph, 10)
        train_feature_file = open(output_path+'train_feature.csv', 'w')
        print('label,n1,n2,common_n,overlap_n,aa_n,pa,TCFC,common_p,overlap_p,w_common_p,w_overlap_p,user_ent,aa_ent,min_ent,aa_p,min_p,pp,geodist,w_geodist,cccp,cccpr,TCS,STCR,StCR,StTCR,StCS',file=train_feature_file)
        label_1_feature = computeFeature(social_graph, checkin_graph, social_graph.edges(), nprocs, popular_places)
        label_0_feature = computeFeature(social_graph, checkin_graph, not_friend_list, nprocs, popular_places)
        writeFeature(train_feature_file, 1, label_1_feature)
        writeFeature(train_feature_file, 0, label_0_feature)
    elif command == 'test': # compute test features
# initialize 
        social_graph, not_friend_list = cf.create_social_graph(input_path)
        checkin_graph = cf.create_checkin_info(input_path, social_graph)
        popular_places = cf.get_popular_places(checkin_graph, 10)
        test = open(input_path+'gowalla.test.txt', 'r')
        edges_list = list()
        for line in test:
            entry = line.strip().split()
            edges_list.append((int(entry[0]), int(entry[1]), entry[2]))
        test_feature_file = open(output_path+'test_feature.csv', 'w')
        print('label,n1,n2,common_n,overlap_n,aa_n,pa,TCFC,common_p,overlap_p,w_common_p,w_overlap_p,user_ent,aa_ent,min_ent,aa_p,min_p,pp,geodist,w_geodist,cccp,cccpr,TCS,STCR,StCR,StTCR,StCS',file=test_feature_file)
        test_feature = computeFeature(social_graph, checkin_graph, edges_list, nprocs, popular_places)
        writeFeature(test_feature_file, -1, test_feature)
    elif command == 'map_verify':
        # just to verify the correctness of a function  
        origins = '花蓮縣花蓮市中美路104號'
        destinations = '花蓮火車站'
        result = cf.get_distance(origins, destinations)
        print(result)
    elif command == 'poi_write':
#        import datetime as dt
#        input_path = 'input/Gowalla_new/POI/'
        poi_graph, user_list, place_list = poi.create_poi_graph(input_path)
        user_stat = open(input_path+'user_stat.txt', 'w')
        checkin_spot_stat = open(input_path+'checkin_spot_stat.txt', 'w')
        processing_train = open(input_path+'processing_Gowalla_train.txt', 'w')
        s = time()
        for place in place_list:
            lat = poi_graph.node[place]['lat']
            lng = poi_graph.node[place]['lng']
            total_checkin = poi_graph.node[place]['total_checkin']
            print(place, lat, lng, total_checkin, file=checkin_spot_stat)
        for user in user_list:
            checkin_spots = poi_graph.neighbors(user)
            user_total_checkin = 0
            for spot in checkin_spots:
                num_checkin = poi_graph.edge[user][spot]['num_checkin']
                user_total_checkin += num_checkin
                time_list = poi_graph.edge[user][spot]['checkin_time_list']
                print(user, spot, num_checkin, end=' ', file=processing_train)
                for t in time_list:
                    print(t, end=' ', file=processing_train) 
                print('', file=processing_train)
            print(user, len(checkin_spots), user_total_checkin, file=user_stat)
        e = time()
        print('time of processing train', e-s)
    elif command == 'hometown_test':
        checkin_graph = cf.create_checkin_info(input_path)
        social_graph, not_friend_list = cf.create_social_graph(input_path)
    elif command == 'poi_stat':
        poi_graph, user_list, place_list = poi.create_poi_graph_from_file(input_path)
        s=time()
        possible_user_dict = poi_r.get_possible_user_from_spots(poi_graph, user_list)
        possible_user = open(input_path+'possible_user.txt', 'w')
        for u,p in possible_user_dict.items():
            print(u,len(p),file=possible_user)
        e=time()
        print('time of possible_user', e-s)
    elif command == 'poi_cos':
        poi_graph, user_list, place_list = poi.create_poi_graph_from_file(input_path)
        s=time()
        poi_r.write_user_cosine_spots(output_path, poi_graph, user_list, 10, 8)
        e=time()
        print('time of user_cosine', e-s)
    elif command == 'lk_social_stat':
        # link prediction
        social_graph, not_friend_list = cf.create_social_graph(input_path)
        cs.get_social_graph_stat(social_graph, output_path)
    elif command == 'poi_social_stat':
        input_path='input/Gowalla_new/POI/'
        output_path='output/poi_recommendation/'
        social_graph = poi.create_social_graph(input_path)
        cs.get_social_graph_stat(social_graph, output_path)



    print("end of execution")
