import poi_graph
import networkx as nx
import datetime

# output accuracy
def evaluate(testing_path, prediction_path, method):
	# input: testing file's path, result file's path and method name
	# output: output the accuracy
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


def cf_user(graph, user_list, place_list, output_path):
	# for user in user_list:
#	for user in user_list:
#		graph.node[user]
	predict_dict = dict()
	return predict_dict

def cf_item(graph, user_list, place_list, output_path):
	predict_dict = dict()
	return predict_dict

poi_graph, user_list, place_list = create_poi_graph('../input/Gowalla_new/POI/')
cf_user(poi_graph, user_list, place_list, '../output/poi_recommendation/')
cf_user(poi_graph, user_list, place_list, '../output/poi_recommendation/')
print(len(user_list), len(place_list))
