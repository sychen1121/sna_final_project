import networkx as nx
from math import log    

def common_neighbors(graph, x, y):
    """compute common neighbors of node x and node y"""
    x_neighbors = set(graph.neighbors(x))
    y_neighbors = set(graph.neighbors(y))

    return float(len(x_neighbors & y_neighbors))


def jaccard(graph, x, y):
    """compute jacaard coefficient of node x, and node y"""
    x_neighbors = set(graph.neighbors(x))
    y_neighbors = set(graph.neighbors(y))

    if len(x_neighbors) == 0 or len(y_neighbors) == 0:        
        score = 0.0
    else:
        score = len(x_neighbors & y_neighbors)/len(x_neighbors | y_neighbors)
    return score

def adamic(graph, x, y):
    """compute adamic value of x and y"""
    x_neighbors = set(graph.neighbors(x))
    y_neighbors = set(graph.neighbors(y))

    score = 0.0
    for z in (x_neighbors & y_neighbors):
        z_neighbors = graph.neighbors(z)
        if len(z_neighbors) == 0:
            continue
        elif len(z_neighbors) == 1:
            score += 10.0
        else:
            score += 1/log(len(z_neighbors))
    return score

def preferential(graph, x, y):
    """compute preferential attachment of x, and y"""
    x_neighbors = graph.neighbors(x)
    y_neighbors = graph.neighbors(y)

    score = len(x_neighbors) * len(y_neighbors)
    return score

def sim_rank(graph, x, y, gamma=0.5, similarity=jaccard):
    """compute similarity rank of x and y"""
    x_neighbors = graph.neighbors(x)
    y_neighbors = graph.neighbors(y)

    if len(x_neighbors) == 0 or len(y_neighbors) == 0:
        score = 0.0
    else:
        sum = 0.0
        for a in x_neighbors:
            for b in y_neighbors:
                sum += similarity(graph, a, b)
        score = gamma * sum / len(x_neighbors) /len(y_neighbors)
    return score

def attr_score(graph, x, y, attribute, datatype):
    a1 = graph.node[x][attribute]
    a2 = graph.node[y][attribute]    
    if a1=='' or a2=='':
        return 0.0
    score = float()
    try:
        if datatype == 'numerical':
            num1 = int(a1)
            num2 = int(a2)
            if num1>num2:
                score = float(num2)/num1
            else:
                score = float(num1)/num2
        else:
            a1_set = set(a1.split(' '))
            a2_set = set(a2.split(' '))
            score = float(len(a1_set.intersection(a2_set)))/len(a1_set.union(a2_set))
#            print(attribute, 'a1',a1_set, 'a2', a2_set)
            # print('a1 is '+a1+', a2 is '+a2)
            # print(score)
#        print(attribute, score, sep=':')
        return score
    except:
        return 0.0

def common_attribute_similarity(graph, x, y):
    region   = attr_score(graph, x, y, 'column_4', 'categorical') 
    language = attr_score(graph, x, y, 'column_5', 'categorical')
    hobby    = attr_score(graph, x, y, 'column_7', 'categorical') 
    education = attr_score(graph, x, y, 'column_8', 'categorical')
    music1   = attr_score(graph, x, y, 'column_21', 'categorical')
    music2   = attr_score(graph, x, y, 'column_34', 'categorical')
    movie1   = attr_score(graph, x, y, 'column_37', 'categorical')
    movie2   = attr_score(graph, x, y, 'column_50', 'categorical')
    com_neig = common_neighbors(graph, x, y)
#    print(com_neig, end=' ')
#    print(region   ,end=' ') 
#    print(language ,end=' ')
#    print(education,end=' ')
#    print(hobby    ,end=' ')
#    print(music1   ,end=' ')
#    print(music2   ,end=' ')
#    print(movie1   ,end=' ')
#    print(movie2           )
    if com_neig <= 5:
        com_neig = com_neig*4/25
    elif com_neig <= 100:
        com_neig = 0.8+(com_neig-5.0)*0.2/95.0
    else:
        com_neig = 1+(com_neig-100.0)/99900.0
    weight = 0.6
    score = weight*(region+language+education+com_neig)+\
            (1-weight)*(hobby+music1+music2+movie1+movie2)            
    return score
