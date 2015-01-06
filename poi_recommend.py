import poi_graph as poi
import networkx as nx
import datetime
import json
import math
from time import time
import multiprocessing as mp

# ================ shared functions ====================

# run method
def run_method(f):
    predict_dict = f()
    method = f.__name__
    write_prediction(method, predict_dict)
    evaluate(method)

# output accuracy to result.txt
def evaluate(method, prediction_path='../output/poi_recommendation/',testing_path='../input/Gowalla_new/POI/'):
    # input: testing file's path, result file's path and method name
    # output: output the accuracy in result.txt
    answers = dict()
    predictions = dict()
    with open(testing_path+'Gowalla_testing.txt','r') as fi:
        for line in fi:
            entry = line.strip().split('\t')
            user = entry[0]
            place = 'p'+entry[4]
            if answers.get(user, 0) == 0:
                answers[user] = list()
            answers[user].append(place)
    with open(prediction_path+'result_'+method+'.txt', 'r') as fi2:
        for line in fi2:
            entry = line.strip().split()
            user = entry[0]
            places = entry[1:-1]
            predictions[user] = places
    user_num = len(answers)
    bingo = 0 
    for user in predictions.keys():
        answer_places = answers[user]
        for place in predictions[user]:
            if place in answer_places:
                bingo = bingo+1
                answer_places.remove(place)
    accuracy = float(bingo)/(3*len(answers))
    with open('../output/poi_recommendation/result.txt', 'a') as fo:
        fo.write(method+'\t'+str(accuracy)+'\t'+str(datetime.datetime.now())+'\n')


# write prediction dictionary to the file under output/poi_recommendation
def write_prediction(method, predict_dict):
    output_path = '../output/poi_recommendation/'
    predict_list = sorted(predict_dict.keys())
    with open(output_path+'result_'+method+'.txt', 'w') as fo:
        for user in predict_list:
            output_str = str(user)
            for place in predict_dict[user]:
                output_str = output_str+'\t'+str(place)
            fo.write(output_str+'\n')

def choice(weighted_choices):
# weighted_choices is a tuple list such as [(choice1, weight1), (choice2, weight2)]
    from itertools import accumulate
    from bisect import bisect
    from random import random
    choices, weights = zip(*weighted_choices)
    cumdist = list(accumulate(weights))
    x = random() * cumdist[-1]
    #print('choice',choices[bisect(cumdist, x)])
    return choices[bisect(cumdist, x)]

def read_vectors2json(file_path, file_name):
    with open(file_path+file_name, 'r') as fi:
        result_dict = json.loads(fi.read())
    return result_dict

def write_vectors2json(output_dict, file_path, file_name):
    # if need indent?
    jsonString = json.dumps(output_dict, sort_keys=True)
    with open(file_path+file_name, 'w') as fo:
        fo.write(jsonString)

# =============== cf fucntions ==================

# ====vectors of places and users
def write_vector_matrix(user_list, place_list, poi_graph, social_graph):
    # norm users vector and then output
    # norm items vector and then output
    user_norm_dict = norm_vector_by_graph(user_list,poi_graph)
    place_norm_dict = norm_vector_by_graph(place_list, poi_graph)
    write_vectors2json(user_norm_dict, '../output/poi_recommendation/', 'user_norm_vector.txt')
    write_vectors2json(place_norm_dict, '../output/poi_recommendation/', 'place_norm_vector.txt')

def norm_vector_by_graph(origin_list, graph):
    items_norm_dict = dict()
    # get all norm vectors
    for item in origin_list:
        normValue = float()
        norm_dict = dict()
        # get vector
        for n in graph.neighbors(item):
            norm_dict[n] = graph.edge[item][n]['num_checkin']
            normValue = normValue+norm_dict[n]**2
        normValue = normValue**0.5
        # norm the vector
        for i in norm_dict.keys():
            norm_dict[i] = norm_dict[i]/normValue
        items_norm_dict[item] = norm_dict
    return items_norm_dict

# ======= cal cosines
def write_users_cosine(output_path, top_k, social_graph):
    user_vectors_dict = read_vectors2json(output_path, 'user_norm_vector.txt')
    user_list = user_vectors_dict.keys()
    # get candidates
    user_candidates_dict = dict()
    # write social candidates
    for user in user_list:
        two_level_friends = set()
        for n in social_graph.neighbors(user):
            if n in user_list:
                two_level_friends.add(n)
            for n2 in social_graph.neighbors(n):
                if n2 in user_list:
                    two_level_friends.add(n2)
        two_level_friends = list(two_level_friends)
        user_candidates_dict[user] = two_level_friends
    write_cosine_matrix(user_vectors_dict, user_candidates_dict, output_path, 'user_cosine_matrix.txt')
    write_top_k_cosine_matrix(output_path, 'user_cosine_matrix.txt', top_k, 'user_top_'+str(top_k)+'_cosine_matrix.txt')


# calculate and write cosine matrix
def write_cosine_matrix(vectors_dict, candidates_dict, output_path, cos_file_name):
    print('start computing cosine matrix')
    cos_matrix_dict = dict()
    item_list = sorted(candidates_dict.keys())
    # for every item, calculating cosine similarity

    for item in item_list:
        s = time()
        print(item)
        candidate_list = candidates_dict[item]
        for candidate in candidate_list:
            cos = cal_cosine(vectors_dict[item], vectors_dict[candidate])
            try: 
                cos_matrix_dict[item][candidate] = cos
            except:
                cos_matrix_dict[item] = dict()
                cos_matrix_dict[item][candidate] = cos
        e= time()
        print(e-s)
    write_vectors2json(cos_matrix_dict, output_path, cos_file_name)

    
# write top k cosine matrix to the file
def write_top_k_cosine_matrix(file_path, file_name, top_k, top_k_cos_file_name):
    top_k_matrix_dict = dict()
    cos_matrix_dict = read_vectors2json(file_path, file_name)
    top_k = top_k+1
    print('over reading')
    for item, cos_dict in cos_matrix_dict.items():
        end = min(top_k, len(cos_dict))
        cos_list = sorted(cos_dict.items(), key=lambda d:d[1], reverse = True)[1:end]
        top_k_cos_dict = dict()
        for t in cos_list:
            if t[1]!=0.0:
                top_k_cos_dict[t[0]] = t[1]
        top_k_matrix_dict[item] = top_k_cos_dict
    write_vectors2json(top_k_matrix_dict, file_path, top_k_cos_file_name)



# calculate the cosine of two vectors
def cal_cosine(dict1, dict2):
    # input two norm vector
    cos = float()
    for item in dict1.keys():
        cos = cos + dict1.get(item, 0)*dict2.get(item, 0)
    return cos





# recommend place to the user by cf user-based model
def cf_preprocess(input_path='../input/Gowalla_new/POI/', output_path='../output/poi_recommendation/',top_k=10):
    # # load social and poi graph
    # poi_graph, user_list, place_list = poi.create_poi_graph(input_path)
    # social_graph = poi.create_social_graph(input_path)
    # poi.update_user_hometown(social_graph, poi_graph)

    # # write vectors of users or places
    # write_vector_matrix(user_list, place_list, poi_graph, social_graph)

    
    # # cal user cosine matrix by social graph
    # print('start cf user-based')
    # write_users_cosine(output_path, top_k, social_graph)
    write_top_k_cosine_matrix(output_path, 'user_cosine_matrix.txt', top_k, 'user_top_'+str(top_k)+'_cosine_matrix.txt')

    # cal place cosine matrix
    # place_vector_dict = read_vectors2json(output_path, 'place_norm_vector.txt')
    # write_cosine_matrix(place_vector_dict, output_path, 'place_cosine_matrix.txt')
    # write_top_k_cosine_matrix(output_path, 'place_cosine_matrix.txt', top_k, 'place_top_'+str(top_k)+'_cosine_matrix.txt')



# ============= recommend methods ===============

def cf_user(top_k=10, output_path='../output/poi_recommendation'):
    predict_dict = dict()
    user_near_places = read_vectors2json(output_path, 'user_near_places.txt')
    user_list = user_near_places.keys()
    # read top_k file 
    cos_matrix_dict = read_vectors2json(output_path, 'user_top_'+str(top_k)+'_cosine_matrix.txt')
    user_vectors_dict = read_vectors2json(output_path, 'user_norm_vector.txt')
    # cal user avg score
    user_avg_dict = dict()
    for user, place_dict in user_vectors_dict.items():
        avg = sum(place_dict.values())/float(len(place_dict))
        user_avg_dict[user] = avg
    # start to cal unknown places
    for user in user_list:
        candi_list = user_near_places[user]
        candi_set = set(candi_list)
        avg = user_avg_dict[user]
        for sim_user, cos in cos_matrix_dict[user].items():
            friend_avg = user_avg_dict[sim_user]
            for place, place_score in user_vectors_dict[sim_user]:
                if place in candi_set:
                    user_vectors_dict[user][place] = user_vectors_dict[user].get(place,0)+ cos*(place_score-friend_avg)
        # for place in candi_list:
        #   place_score = avg
        #   for sim_user, cos in cos_matrix_dict[user].items():
        #       place_score = place_score+cos*(user_vectors_dict[user][place]-
        #   user_vectors_dict[place] = place_score
    write_vectors2json(user_vectors_dict, output_path, 'user_cf_user_vector.txt')
    for user in user_list:
        predict_list = list()
        for i in range(0,3):
            predict_list.append(choice(place_item))
        predict_dict[user] = predict_list
    return predict_dict

# =============== cf multiprocess ==================

def cf_user_mp(top_k=10, output_path='../output/poi_recommendation/', nprocs = 16):
    s= time()
    predict_dict = dict()
    users_unvisited_place_score = dict()
    user_near_places = read_vectors2json(output_path, 'user_near_places.txt')
    user_list = user_near_places.keys()
    # read top_k file 
    cos_matrix_dict = read_vectors2json(output_path, 'user_top_'+str(top_k)+'_cosine_matrix.txt')
    user_vectors_dict = read_vectors2json(output_path, 'user_norm_vector.txt')
    # cal user avg score
    user_avg_dict = dict()
    for user, place_dict in user_vectors_dict.items():
        avg = sum(place_dict.values())/float(len(place_dict))
        user_avg_dict[user] = avg
    # start to cal unknown places
    num_user = len(user_list)
    out_q = mp.Queue()
    chunk_size = int(math.ceil(num_user/nprocs))
    procs = list()
    for i in range(nprocs):
        if i == nprocs-1:
            users = user_list[i*chunk_size:]
        else:
            users = user_list[i*chunk_size:(i+1)*chunck_size]
        p = mp.Process(target=worker, args=(user_near_places, user_avg_dict, cos_matrix_dict, user_vectors_dict, out_q))
        p.start()
        procs.append(p)
    for i in range(nprocs):
        users_unvisited_place_score.update(out_q.get())
    for p in procs:
        p.join()
    e= time()
    print('time of cf', e-s)
    write_vectors2json(users_unvisited_place_score, output_path, 'user_unvisited_place_score.txt')
    for user in user_list:
        user_vectors_dict[user].update(users_unvisited_place_score)
    write_vectors2json(user_vectors_dict, output_path, 'user_cf_user_vector.txt')
    for user in user_list:
        predict_list = list()
        for i in range(0,3):
            predict_list.append(choice(place_item))
        predict_dict[user] = predict_list
    return predict_dict

def worker(users, user_near_places, user_avg_dict, cos_matrix_dict, user_vectors_dict, out_q):
    users_unvisited_place_score = dict()
    for user in users:
        print(user)
        unvisited_place_score = dict()
        candi_list = user_near_places[user]
        candi_set = set(candi_list)
        avg = user_avg_dict[user]
        for sim_user, cos in cos_matrix_dict[user].items():
            friend_avg = user_avg_dict[sim_user]
            for place, place_score in user_vectors_dict[sim_user]:
                if place in candi_set:
                    unvisited_place_score[place] = unvisited_place_score.get(place, 0) + cos*(place_score-friend_avg)
                    # user_vectors_dict[user][place] = user_vectors_dict[user].get(place,0)+ cos*(place_score-friend_avg)
        users_unvisited_place_score[user] = unvisited_place_score
        break
    out_q.put(users_unvisited_place_score)



# recommend place to the user by cf item-based model
def cf_item(top_k=10, output_path='../output/poi_recommendation'):
    predict_dict = dict()
    user_near_places = read_vectors2json(output_path, '')
    user_list = user_near_places.keys()
    # need to be add
    for user in user_list:
        predict_list = list()
        for i in range(0,3):
            predict_list.append(choice(place_item))
        predict_dict[user] = predict_list
    return predict_dict
    return predict_dict



def most_visited_random_method(output_path='../output/poi_recommendation/'):
    predict_dict = dict()
    file_name = 'user_norm_vector.txt'
    user_norm_dict = read_vectors2json(output_path, file_name)
    for user, place_dict in user_norm_dict.items():
        predict_list = list()
        place_item = place_dict.items()
        for i in range(0,3):
            predict_list.append(choice(place_item))
        predict_dict[user] = predict_list
    return predict_dict

def most_visited_one_method(output_path='../output/poi_recommendation/'):
    predict_dict = dict()
    file_name = 'user_norm_vector.txt'
    user_norm_dict = read_vectors2json(output_path, file_name)
    for user, place_dict in user_norm_dict.items():
        predict_list = list()
        place_item = place_dict.items()
        place_rank = sorted(place_item, key=lambda d:d[1], reverse=True)
        for i in range(0,3):
            predict_list.append(place_rank[0][0])
        predict_dict[user] = predict_list
    return predict_dict

# add time stamp in location to predict 


# run_method(most_visited_one_method)
# run_method(most_visited_random_method)

# run_method(cf_user)

# cf_preprocess()
