def percent(train, test):
    """compute ans in test occupy how many percent of train"""
    import networkx as nx
    graph = nx.Graph()
    edge_list = list()
    visited_place = 0
    for line in train:
        entry = line.strip().split()
        user = entry[0]
        place = entry[1]
        edge_list.append((user,place))
    graph.add_edges_from(edge_list)

    lines = test.readlines()
    for line in lines:
        entry = line.strip().split('\t')
        user = entry[0]
        place = 'p'+entry[4]
        if graph.has_edge(user, place):
            visited_place += 1  
    return float(visited_place/len(lines))
    
if __name__ == '__main__':
    train = open('input/Gowalla_new/POI/processing_Gowalla_train.txt', 'r')
    test = open('input/Gowalla_new/POI/Gowalla_testing.txt', 'r')
    percent_file = open('output/poi_recommendation/percent.txt', 'w')
    p = percent(train, test)
    print('percent of places user visited', p*100, file=percent_file)
    print('percent of places user never visit', (1-p)*100, file=percent_file)
