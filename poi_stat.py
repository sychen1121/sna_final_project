import poi_graph as poi
import poi_recommend as pr

# add this for testing
def get_place_visited_ratio(output_path = '../output/poi_recommendation/',testing_path='../input/Gowalla_new/POI/'):
	answers = dict()
	ratio = float()
	count = int()
	with open(testing_path+'Gowalla_testing.txt','r') as fi:
		for line in fi:
			entry = line.strip().split('\t')
			user = entry[0]
			place = 'p'+entry[4]
			if answers.get(user, 0) == 0:
				answers[user] = list()
			answers[user].append(place)
	user_list = answers.keys()
	user_vectors_dict = pr.read_vectors2json(output_path, 'user_norm_vector.txt')
	for user in user_list:
		user_visited_places = user_vectors_dict[user].keys()
		for place in answers[user]:
			if place in user_visited_places:
				count = count+1
	ratio = count / (3*len(user_list))
	print(ratio)
	with open(output_path+'statistic.txt', 'a') as fo:
		fo.write('The Ratio of Visited Places in new places: '+ str(ratio))



# get_place_visited_ratio()

def get_answer_ratio(output_file, output_path='../output/poi_recommendation/', testing_path='../input/Gowalla_new/POI/'):
	answers = dict()
	ratio = float()
	count = int()
	with open(testing_path+'Gowalla_testing.txt','r') as fi:
		for line in fi:
			entry = line.strip().split('\t')
			user = entry[0]
			place = 'p'+entry[4]
			if answers.get(user, 0) == 0:
				answers[user] = list()
			answers[user].append(place)
	user_list = answers.keys()
	user_places_dict = pr.read_user_places2json(output_path, output_file)
	for user in user_list:
		candi_places = user_places_dict[user]
		answer_places = answers[user]
		for place in answer_places:
			if place in candi_places:
				count = count+1
	ratio = count / (3*len(user_list))
	print(ratio)
	with open(output_path+'statistic.txt', 'a') as fo:
		fo.write('The Ratio of Candidate Places in new places: '+ str(ratio))

get_answer_ratio('')


