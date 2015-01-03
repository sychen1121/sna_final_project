import poi_graph as poi
import networkx as nx
import datetime
import json



# ================ shared methods ====================

# output accuracy to result.txt
def evaluate(testing_path, prediction_path, method):
    # input: testing file's path, result file's path and method name
    # output: output the accuracy in result.txt
    answers = dict()
    predictions = dict()
    with open(testing_path+'Gowalla_testing.txt','r') as fi:
        for line in fi:
            entry = line.strip().split('\t')
            user = int(entry[0])
            place = 'p'+entry[4]
            if answers.get(user, 0) == 0:
                answers[user] = place
            else:
                answers[user] = answers[user].append(place)
    with open(prediction_path+'result_'+method+'.txt', 'r') as fi2:
        for line in fi2:
            entry = line.strip().split()
            user = int(entry[0])
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
        fo.write(method+'\t'+str(accuracy)+'\t'+str(datetime.datetime.now()))


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

# =============== cf fucntions ==================

def write_vector_matrix(user_list, place_list, poi_graph, social_graph):
	# norm users vector and then output
	# norm items vector and then output
	user_norm_dict = norm_vector_by_graph(user_list,poi_graph)
	place_norm_dict = norm_vector_by_graph(place_list, poi_graph)
	write_vectors2json(user_norm_dict, '../output/poi_recommendation/', 'user_norm_vector.txt')
	write_vectors2json(place_norm_dict, '../output/poi_recommendation/', 'place_norm_vector.txt')


# calculate and write cosine matrix
def write_cosine_matrix(matrix_dict, output_path,cos_file_name):
	print('start computing cosine matrix')
	cos_matrix_dict = dict()
	item_list = sorted(matrix_dict.keys())
	# for every item, calculating cosine similarity
	for i, itemi in enumerate(item_list):
		sim_dict = dict()
		j = i+1
		while j < len(item_list):
			print(j)
			itemj = item_list[j]
			cos = cal_cosine(matrix_dict[itemi], matrix_dict[itemj])
			try: 
				cos_matrix_dict[itemi][itemj] = cos
			except:
				cos_matrix_dict[itemi] = dict()
				cos_matrix_dict[itemi][itemj] = cos
			try:			
				cos_matrix_dict[itemj][itemi] = cos
			except:
				cos_matrix_dict[itemj] = dict()
				cos_matrix_dict[itemj][itemi] = cos
			j = j+1
	write_vectors2json(cos_matrix_dict, output_path, cos_file_name)

	
# write top k cosine matrix to the file
def write_top_k_cosine_matrix(file_path, file_name, top_k, top_k_cos_file_name):
	top_k_matrix_dict = dict()
	cos_matrix_dict = read_vectors2json(file_path, file_name)
	for item, cos_dict in cos_matrix_dict.items():
		cos_list = sorted(cos_dict.iteritems(), key=lambda d:d[1], reverse = True)[0:top_k]
		top_k_cos_dict = dict()
		for t in cos_list:
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

def read_vectors2json(file_path, file_name):
	with open(file_path+file_name, 'r') as fi:
		result_dict = json.loads(fi.read())
	return result_dict

def write_vectors2json(output_dict, file_path, file_name):
	# if need indent?
	jsonString = json.dumps(output_dict, sort_keys=True)
	with open(file_path+file_name, 'w') as fo:
		fo.write(jsonString)

# recommend place to the user by cf user-based model
def cf_preprocess(input_path='../input/Gowalla_new/POI/', output_path='../output/poi_recommendation/',top_k=10):
	# # load social and poi graph
	# poi_graph, user_list, place_list = poi.create_poi_graph(input_path)
	# social_graph = poi.create_social_graph(input_path)
	# poi.update_user_hometown(social_graph, poi_graph)

	# # write vectors of users or places
	# write_vector_matrix(user_list, place_list, poi_graph, social_graph)

	# read vectors of user or places and write cosine sim
	user_vector_dict = read_vectors2json(output_path, 'user_norm_vector.txt')
	print('over read user')
	place_vector_dict = read_vectors2json(output_path, 'place_norm_vector.txt')
	write_cosine_matrix(user_vector_dict, output_path, 'user_cosine_matrix.txt')
	write_cosine_matrix(place_vector_dict, output_path, 'place_cosine_matrix.txt')
	write_top_k_cosine_matrix(output_path, 'user_cosine_matrix.txt', top_k, 'user_top_'+str(top_k)+'_cosine_matrix.txt')
	write_top_k_cosine_matrix(output_path, 'place_cosine_matrix.txt', top_k, 'place_top_'+str(top_k)+'_cosine_matrix.txt')

def cf_user(graph, user_list, place_list, top_k, top_k_file_name, output_path='../output/poi_recommendation'):
	predict_dict = dict()
	# read top_k file 
	cos_matrix_dict = read_vectors2json(output_path, 'user_top_'+str(top_k)+'_cosine_matrix.txt')
	# cal places score
	# user_avg_score = 
	# output top 3 score places
	# cal write prediction
	# evaluation
	
	return predict_dict

# recommend place to the user by cf item-based model
def cf_item(graph, user_list, place_list, output_path):
    predict_dict = dict()
    return predict_dict

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


cf_preprocess()

# cf_user(poi_graph, user_list, place_list, '../output/poi_recommendation/')

# cf_item(poi_graph, user_list, place_list, '../output/poi_recommendation/')
