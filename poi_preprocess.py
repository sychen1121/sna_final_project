import poi_graph as poi
input_path='../input/Gowalla_new/POI/'
output_path='../output/poi_recommendation/'
poi_graph, user_list, place_list = poi.create_poi_graph_from_file(input_path)

# revise the poi_places to the unvisited place
with open('output_path')