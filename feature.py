import math
import numpy as np

def social_feature(s_graph,n1,n2):

    n1_neightbor = s_graph.neighbors(n1)
    n2_neightbor = s_graph.neighbors(n2)
    common_n = set(n1_neightbor).intersection(n2_neightbor)
    
    neiNum1 = len(n1_neightbor)
    neiNum2 = len(n2_neightbor)
    
    if neiNum1+neiNum2 <=0:
        overlap_n = 0
    else:
        overlap_n = len(common_n)*1.0/(neiNum1+neiNum2-len(common_n))
        
    aa_n =0
    for cn in common_n:
        if len(s_graph.neighbors(cn))<=0:#
            continue#
        elif len(s_graph.neighbors(cn)) == 1:#
            aa_n += 100.0#for log 1
        else:
            aa_n = aa_n + 1.0/math.log(len(s_graph.neighbors(cn)))
    
    pa = len(n1_neightbor)*len(n2_neightbor)
    
    return len(common_n),overlap_n,aa_n,pa
    
def place_feature(p_graph,n1,n2):
    n1_place = p_graph.neighbors(n1)
    n2_place = p_graph.neighbors(n2)
    common_p= set(n1_place).intersection(n2_place)
    union_p = set(n1_place).union(n2_place)
    
    pNum1 =len(n1_place)
    pNum2 =len(n2_place)
    
    if pNum1+pNum2 <=0:
        overlap_p = 0
    else:
        overlap_p= len(common_p)*1.0/((pNum1+pNum2)-len(common_p))
    
    aa_ent = 0
    min_ent = 5.0
    aa_p =0
    min_p = 0.0
    
    for place in common_p:
#         compute min_ent
        if (min_ent == 0.0) or (p_graph.node[place]['entropy'] < min_ent):
            min_ent = p_graph.node[place]['entropy']
#         compute min_p
        if (min_p == 0.0) or (p_graph.node[place]['total_checkin'] < min_ent):
            min_p = p_graph.node[place]['total_checkin']
#         count aa_ent
        if p_graph.node[place]['entropy']<=0:
            continue
        else:
            aa_ent = aa_ent + 1.0/p_graph.node[place]['entropy']
#         count aa_p
        if p_graph.node[place]['total_checkin']<=0:
            continue
        else:
            aa_p = aa_p + 1.0/p_graph.node[place]['total_checkin']
    
# compute  w_common_p/w_overlap_p
    
    c1 = list()
    c2 = list()
    for place in union_p:
        if place in n1_place:
            c1.append(p_graph[n1][place]['num_checkin'])
        else:
            c1.append(0)
            
        if place in n2_place:
            c2.append(p_graph[n2][place]['num_checkin'])
        else:
            c2.append(0)
    
    c1 = np.array(c1)
    c2 = np.array(c2)
        
    w_common_p = np.dot(c1,c2)
    
    seDot = (np.dot(c1,c1)*np.dot(c2,c2))**(1/2.0)
    if seDot <= 0:
        w_overlap_p = 0
    else:
        w_overlap_p = np.dot(c1,c2)/seDot
    
    pp = len(n1_place)*len(n2_place)
    
    return len(common_p),overlap_p,w_common_p,w_overlap_p,aa_ent,min_ent,aa_p,min_p,pp
        
