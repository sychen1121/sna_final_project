import poi_graph as poi
import networkx as nx
import datetime
import json
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

def cal_sim_matrix(user_list, place_list, poi_graph, social_graph):
	# norm users vector and then output
	# norm items vector and then output
	user_norm_dict = norm_vector_by_graph(user_list,poi_graph)
	place_norm_dict = norm_vector_by_graph(place_list, poi_graph)
	write_sim_json(user_norm_dict, '../output/poi_recommendation/', 'user_norm_vector.txt')
	write_sim_json(place_norm_dict, '../output/poi_recommendation/', 'place_norm_vector.txt')

	# user_vectors = dict()
	# for user in user_list:
def norm_vector_by_graph(origin_list, graph):
	items_norm_dict = dict()
	# get all norm vectors
	for item in origin_list:
		normValue = float()
		norm_dict = dict()
		# get vector
		for n in graph.neighbors(item):
			norm_dict[n] = graph.edge[item][n]['num_checkin']
			normValue = norm_dict[n]**2
		normValue = normValue**(1/2)
		# norm the vector
		for i in norm_dict.keys():
			norm_dict[i] = norm_dict[i]/normValue
		items_norm_dict[item] = norm_dict
	return items_norm_dict

def write_sim_json(output_dict, file_path, file_name):
	# if need indent?
	jsonString = json.dumps(output_dict, sort_keys=True)
	with open(file_path+file_name, 'w') as fo:
		fo.write(jsonString)


def cf_user(graph, user_list, place_list, output_path):
	# for user in user_list:
	# for user in user_list:
		# graph.node[user]
	predict_dict = dict()
	return predict_dict

def cf_item(graph, user_list, place_list, output_path):
	predict_dict = dict()
	return predict_dict

poi_graph, user_list, place_list = poi.create_poi_graph('../input/Gowalla_new/POI/')
social_graph = poi.create_social_graph('../input/Gowalla_new/POI/')
update_user_hometown(social_graph, poi_graph)
cal_sim_matrix(user_list, place_list, poi_graph, social_graph)
# cf_user(poi_graph, user_list, place_list, '../output/poi_recommendation/')
# cf_item(poi_graph, user_list, place_list, '../output/poi_recommendation/')
