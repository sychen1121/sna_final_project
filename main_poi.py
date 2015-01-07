import poi_graph as poi
import poi_recommend as pr 
from sys import argv

# nprocs=int(argv[1])
# file_path = '../input/Gowalla_new/POI/'
# social_graph = poi.create_social_graph(file_path)
# poi_graph, user_list, place_list = poi.create_poi_graph_from_file(file_path)
# poi.update_user_hometown(social_graph, poi_graph)
# poi.update_hometown_geocode(social_graph, user_list)
#user_near_places = poi.spot_candidate2(social_graph, poi_graph, user_list, place_list,nprocs)

pr.run_method(pr.cf_user_mp)
# pr.run_method(pr.cf_user_mp_with_distance)
# pr.run_method(pr.time_weighted_most_visited_top_three_method)
# pr.run_method(pr.time_series_most_visited_one_method)
