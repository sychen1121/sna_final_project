import poi_graph
import networkx as nx



def cf_user(graph, user_list, place_list, output_path):
    print('hello')
	

def cf_item(graph, user_list, place_list, output_path):
    print('hello')


poi_graph, user_list, place_list = create_poi_graph('../input/Gowalla_new/POI/')
cf_user(poi_graph, user_list, place_list, '../output/poi_recommendation/')
cf_user(poi_graph, user_list, place_list, '../output/poi_recommendation/')
print(len(user_list), len(place_list))
