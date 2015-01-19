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
		fo.write('The Ratio of Visited Places in new places: '+ str(ratio)+'\n')



# get_place_visited_ratio()

def get_answer_ratio(output_file, output_path='../output/poi_recommendation/', testing_path='../input/Gowalla_new/POI/'):
	answers = dict()
	ratio = float()
	count = int()
	avg_candis = int()
	total_candis = int()
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
		total_candis = total_candis+len(candi_places)
		answer_places = answers[user]
		for place in answer_places:
			if place in candi_places:
				count = count+1
	ratio = count / (3*len(user_list))
	avg_candis = total_candis/float(len(user_list))
	print(str(ratio)+' '+str(avg_candis))
	with open(output_path+'statistic.txt', 'a') as fo:
		fo.write('The Ratio of Candidate Places in new places: '+ str(ratio)+' with avg num candis: '+str(avg_candis)+'\n')

# this function just for ken
def get_friend_candi_ratio(output_path='../output/poi_recommendation/', testing_path='../input/Gowalla_new/POI/'):
	answers = dict()
	ratio = float()
	count = int()
	user_friend_places_dict = dict()

	avg_friend_places_num = float()
	avg_friend_candi_visited_ratio = float()
	avg_friend_candi_unvisited_ratio = float()
	file_path = '../input/Gowalla_new/POI/'
	social_graph = poi.create_social_graph(file_path)
	user_cosine_matrix = pr.read_vectors2json(output_path, 'user_cosine_matrix.txt')
	user_norm_vector = pr.read_vectors2json(output_path, 'user_norm_vector.txt')
	print('over reading cosine')
	with open(testing_path+'Gowalla_testing.txt','r') as fi:
		for line in fi:
			entry = line.strip().split('\t')
			user = entry[0]
			place = 'p'+entry[4]
			if answers.get(user, 0) == 0:
				answers[user] = list()
			answers[user].append(place)
	user_list = answers.keys()
	for user in user_list:
		user_place = user_norm_vector[user].keys()
		friends = user_cosine_matrix[user].keys()
		friend_place_visited = list()
		friend_place_unvisited = list()
		for friend in friends:
			friend_place = user_norm_vector[friend].keys()
			for place in friend_place:
				if place in user_place:
					friend_place_visited.append(place)
				else:
					friend_place_unvisited.append(place)
		avg_friend_places_num = avg_friend_places_num+ len(friend_place_unvisited)+len(friend_place_visited)
		for answer_place in answers[user]:
			if answer_place in friend_place_visited:
				avg_friend_candi_visited_ratio = avg_friend_candi_visited_ratio+1
			if answer_place in friend_place_unvisited:
				avg_friend_candi_unvisited_ratio = avg_friend_candi_unvisited_ratio+1
	avg_friend_candi_visited_ratio = avg_friend_candi_visited_ratio/ (3*len(user_list))
	avg_friend_candi_unvisited_ratio = avg_friend_candi_unvisited_ratio/ (3*len(user_list))
	avg_friend_places_num = avg_friend_places_num/(3*len(user_list))

	print(str(avg_friend_places_num)+' '+str(avg_friend_candi_unvisited_ratio)+' '+str(avg_friend_candi_visited_ratio))
	with open(output_path+'statistic.txt', 'a') as fo:
		fo.write('The Ratio of New Visite Places in Friend Visited Places: '+ str(avg_friend_candi_unvisited_ratio)+' '+str(avg_friend_candi_visited_ratio)+' with avg visited places of friends: '+str(avg_friend_places_num)+'\n')

get_friend_candi_ratio()
# get_answer_ratio('user_candidate_places_list.txt')


