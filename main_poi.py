import poi_graph as poi
import poi_recommend as pr 


file_path = '../input/Gowalla_new/POI/'
social_graph = poi.create_social_graph(file_path)
poi_graph, user_list, place_list = poi.create_poi_graph_from_file(file_path)
poi.update_user_hometown(social_graph, poi_graph)
# poi.update_hometown_geocode(social_graph, user_list)
user_near_places = poi.spot_candidate2(social_graph, poi_graph, user_list, place_list,24)

pr.run_method(cf_user_mp)
