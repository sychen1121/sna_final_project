import common_function as cf
import feature as ft
import multiprocessing as mp
import math
from time import time
from sys import argv

def worker(file_name, social_graph, checkin_graph, edges, index, label):
    out_list = list()
    train_feature = open(file_name+'.'+str(label)+'.'+str(index)+'.csv', 'w')
    print('label,common_n,overlap_n,aa_n,pa,common_p,overlap_p,w_common_p,w_overlap_p,aa_ent,min_ent,aa_p,min_p',file=train_feature)
    for edge in edges:
        n1 = edge[0]
        n2 = edge[1]
        common_n, overlap_n, aa_n, pa = ft.social_feature(social_graph, n1, n2)
        common_p, overlap_p, w_common_p, w_overlap_p, aa_ent, min_ent, aa_p, min_p = ft.place_feature(checkin_graph, n1, n2)
        out_list.append((common_n,overlap_n,aa_n,pa,common_p,overlap_p,w_common_p,w_overlap_p,aa_ent,min_ent,aa_p,min_p))
    for feature in out_list:
        print(label, end=',', file=train_feature)
        for i in range(len(feature)):
            if i == len(feature)-1:
                print(feature[i], file=train_feature)
            else:
                print(feature[i], end=',', file=train_feature)
#    out_q.put(out_list)

if __name__ == '__main__':
    file_path = argv[1]
    output_path = argv[2]
    nprocs = int(argv[3])
    checkin_graph = cf.create_checkin_info(file_path)
    social_graph, not_friend_list = cf.create_social_graph(file_path)
#    train_feature = open(output_path+'train_feature.csv', 'w')
#    print('label,common_n,overlap_n,aa_n,pa,common_p,overlap_p,w_common_p,w_overlap_p,aa_ent,min_ent,aa_p,min_p',file=train_feature)

# using multiprocessing to speed up the execution
    num_edge = social_graph.number_of_edges()
#    out_q = mp.Queue()
    chunk_size = int(math.ceil(num_edge/nprocs))
    procs = []
    for i  in range(nprocs):
        if i == nprocs - 1:
            edges = social_graph.edges()[i*chunk_size:]
        else:
            edges = social_graph.edges()[i*chunk_size:(i+1)*chunk_size]
        p = mp.Process(target=worker, args=(output_path+'train_feature', social_graph, checkin_graph, edges, i, 1))
        procs.append(p)
        p.start()

#    label_1_feature = list()
#    for i in range(nprocs):
#        label_1_feature += (out_q.get())
    for p in procs:
        p.join()
# compute label 0's feature
    num_edge = len(not_friend_list)
#    out_q2 = mp.Queue()
    chunk_size = int(math.ceil(num_edge/nprocs))
    procs = []
    for i  in range(nprocs):
        if i == nprocs - 1:
            edges = not_friend_list[i*chunk_size:]
        else:
            edges = not_friend_list[i*chunk_size:(i+1)*chunk_size]
        p = mp.Process(target=worker, args=(file_path+'train_feature', social_graph, checkin_graph, edges, i, 0))
        procs.append(p)
        p.start()

#    label_0_feature = list()
#    for i in range(nprocs):
#        label_0_feature += (out_q2.get())
    for p in procs:
        p.join()
# print feature to train_feature.csv
#    for feature in label_1_feature:
#        print('1', end=',', file=train_feature)
#        for i in range(8):
#            if i == 7:
#                print(feature[i], file=train_feature)
#            else:
#                print(feature[i], end=',', file=train_feature)
#    for feature in label_0_feature:
#        print('0', end=',', file=train_feature)
#        for i in range(8):
#            if i == 7:
#                print(feature[i], file=train_feature)
#            else:
#                print(feature[i], end=',', file=train_feature)
#    test = open(file_path+'gowalla.test.txt', 'r')
