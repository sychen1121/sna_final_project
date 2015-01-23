import networkx as nx

def get_social_graph_stat(graph, output_path):
	output_file_c = 'social_graph_closeness.csv'
	output_file_b = 'social_graph_betweenness.csv'
	output_file_d = 'social_graph_degree.csv'
	closeDict = nx.closeness_centrality(graph)
	beDict = nx.betweenness_centrality(graph)
	degreeDict = nx.degree_centrality(graph)
	node_list = sorted(closeDict.keys())
	# closeness_centrality
	with open(output_path+output_file_c) as foc:
		foc.write('user,closeness_centrality\n')
		for node in node_list:
			foc.write(str(node)+','+str(closeDict[node])+'\n')
	# betweenness_centrality
	with open(output_path+output_file_b) as fob:
		fob.write('user,betweenness_centrality\n')
		for node in node_list:
			fob.write(str(node)+','+str(beDict[node])+'\n')
	# degree distribution
	with open(output_path+output_file_d) as fod:
		fod.write('user,degree\n')
		for node in node_list:
			fod.write(str(node)+','+str(degreeDict[node])+'\n')


