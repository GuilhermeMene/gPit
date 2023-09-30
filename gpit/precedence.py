#Precedence module is part of the gPit software  (https://github.com/GuilhermeMene/gPit)
#Copyright (c) 2023 gPit Developers 
#Distributed under the terms of MIT License (https://github.com/GuilhermeMene/gPit/blob/main/LICENSE)

#Based on Sebastian Avalos code disributed under MIT License 
#https://github.com/geometatqueens/2020-Pseudoflow-Python

import networkx as NetX



def IA1x9(pos_x, pos_y, pos_z, nx, ny, Graph):

    p_0 =  1 + pos_x + nx*pos_y + ny*nx*pos_z    
    p_1 =  1 + (pos_x-1) + nx*(pos_y-1) + ny*nx*(pos_z+1)
    p_2 =  1 + (pos_x) + nx*(pos_y-1) + ny*nx*(pos_z+1)
    p_3 =  1 + (pos_x+1) + nx*(pos_y-1) + ny*nx*(pos_z+1)
    p_4 =  1 + (pos_x-1) + nx*(pos_y) + ny*nx*(pos_z+1)
    p_5 =  1 + (pos_x) + nx*(pos_y) + ny*nx*(pos_z+1)
    p_6 =  1 + (pos_x+1) + nx*(pos_y) + ny*nx*(pos_z+1)
    p_7 =  1 + (pos_x-1) + nx*(pos_y+1) + ny*nx*(pos_z+1)
    p_8 =  1 + (pos_x) + nx*(pos_y+1) + ny*nx*(pos_z+1)
    p_9 =  1 + (pos_x+1) + nx*(pos_y+1) + ny*nx*(pos_z+1)
    
    Graph.add_edge(p_0, p_1, const=99e99, mult=1)
    Graph.add_edge(p_0, p_2, const=99e99, mult=1)
    Graph.add_edge(p_0, p_3, const=99e99, mult=1)
    Graph.add_edge(p_0, p_4, const=99e99, mult=1)
    Graph.add_edge(p_0, p_5, const=99e99, mult=1)
    Graph.add_edge(p_0, p_6, const=99e99, mult=1)
    Graph.add_edge(p_0, p_7, const=99e99, mult=1)
    Graph.add_edge(p_0, p_8, const=99e99, mult=1)
    Graph.add_edge(p_0, p_9, const=99e99, mult=1)
    
    return Graph

def IA1x5(pos_x, pos_y, pos_z, nx, ny, Graph):
    p_0 =  1 + pos_x + nx*pos_y + ny*nx*pos_z
    p_2 =  1 + (pos_x) + nx*(pos_y-1) + ny*nx*(pos_z+1)
    p_4 =  1 + (pos_x-1) + nx*(pos_y) + ny*nx*(pos_z+1)
    p_5 =  1 + (pos_x) + nx*(pos_y) + ny*nx*(pos_z+1)
    p_6 =  1 + (pos_x+1) + nx*(pos_y) + ny*nx*(pos_z+1)
    p_8 =  1 + (pos_x) + nx*(pos_y+1) + ny*nx*(pos_z+1)

    Graph.add_edge(p_0, p_2, const=99e99, mult=1)
    Graph.add_edge(p_0, p_4, const=99e99, mult=1)
    Graph.add_edge(p_0, p_5, const=99e99, mult=1)
    Graph.add_edge(p_0, p_6, const=99e99, mult=1)
    Graph.add_edge(p_0, p_8, const=99e99, mult=1)

    return Graph