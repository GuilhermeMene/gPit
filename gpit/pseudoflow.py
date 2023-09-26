
import numpy as np
import networkx as NetX
import pseudoflow as pf
import pandas as pd

def CreateExtArcs(BM, nx, ny, nz, Graph, Var):
    Sink = np.int64(nx*ny*nz + 1)
    for t_z in range(nz):
        pos_z = nz - t_z - 1
        for t_y in range(t_z, ny-t_z):
            for t_x in range(t_z,nx-t_z):
                p_i = 1 + t_x + nx*t_y + ny*nx*pos_z 
                Capacity = np.absolute(np.around(BM[p_i-1,Var], decimals=2))
                if BM[p_i-1,Var] < 0: #Negative local Economic Value
                    Graph.add_edge(p_i, Sink, const=Capacity, mult=-1)
                else:
                    Graph.add_edge(0, p_i, const=Capacity, mult=1)
    return Graph


class Pseudoflow:

    def __init__(self, bmpath:str):

        #Read the blockmodel
        try: 
            self.blockmodel = pd.read_csv(bmpath, delimiter=',')
        except:
            try: 
                self.blockmodel = pd.read_csv(bmpath, delimiter=';')
            except Exception as e: print(e)

    def setBMParms(self, nx:int, ny:int, nz:int, xorg:float, yorg:float, zorg:float, xs:int, ys:int, zs:int):
        self.bmparms = {
            'nx': nx,
            'ny': ny,
            'nz': nz,
            'xorg': xorg,
            'yorg': yorg,
            'zorg': zorg,
            'xs': xs,
            'ys': ys,
            'zs': zs
        }
        return self   

    def setEPVParms(self):

        #Function to save the economic parameters for the pit optimisation 
        print("Enter the economic parameters for pit optimisation")
        mprice = float(input("Enter the Metal Price (USD/lb): "))
        sel_cost = float(input("Enter the Selling Cost (USD/lb): "))
        min_cost = float(input("Enter the Mining Cost (USD/Ton): "))
        proc_cost = float(input("Enter the Processing Cost (USD/Ton): "))

        self.EPVparms = {
            'mprice': mprice ,
            'sel_cost': sel_cost ,
            'min_cost': min_cost ,
            'proc_cost': proc_cost
        }
        return self

        
    def calculateEPV(self, OreGrade:str, Density:str):

        #TODO




def Pseudoflow_UPL(blockmodel, nx, ny, nz, input, output): 
    source = 0
    sink = np.int64(nx*ny*nz + 1)
    
    # Graph creation
    Graph = NetX.DiGraph()
    
    # External arcs creation by external function. Source - Nodes, Nodes - Sink
    Graph = CreateExternalArcs(blockmodel, nx, ny, nz, Graph=Graph, Var=input)
    
    # Internal arcs creation by external function. 
    for ind_z in range(nz - 1):
        pos_z = nz - ind_z - 2
        for pos_y in range(ind_z + 1, ny - ind_z - 1):
            for pos_x in range(ind_z + 1, nx - ind_z - 1):
                # Precedence of 5 blocks
                Graph = CreateInternalArcs1x5(pos_x, pos_y, pos_z, nx, ny, Graph=Graph)
                # Precedence of 9 blocks
                #Graph = CreateInternalArcs1x9(pos_x, pos_y, pos_z, nx, ny, Graph=Graph)
    
    # Solving the minimum cut problem via pf.hpf solver
    RangeLambda = [0]
    breakpoints, cuts, info = pf.hpf(Graph, source, sink, const_cap="const", mult_cap="mult", lambdaRange=RangeLambda, roundNegativeCapacity=False)
    
    #Going over the cuts.items finding the nodes inside the resulting UPL.
    B = {x:y for x, y in cuts.items() if y == [1] and x!=0}
    InsideList = list(B.keys())
    
    # Set all blocks as zero
    blockmodel[:,output] = 0 

    for indUPL in range(len(InsideList)):         
        # Set blocks inside UPL as one
        blockmodel[np.int64(InsideList[indUPL] -1),output] = 1    
 

    return blockmodel

def CreateExternalArcs(BM, nx, ny, nz, Graph, Var):
    Sink = np.int64(nx*ny*nz + 1)
    for t_z in range(nz):
        pos_z = nz - t_z - 1
        for t_y in range(t_z, ny-t_z):
            for t_x in range(t_z,nx-t_z):
                p_i = 1 + t_x + nx*t_y + ny*nx*pos_z 
                Capacity = np.absolute(np.around(BM[p_i-1,Var], decimals=2))
                if BM[p_i-1,Var] < 0: #Negative local Economic Value
                    Graph.add_edge(p_i, Sink, const=Capacity, mult=-1)
                else:
                    Graph.add_edge(0, p_i, const=Capacity, mult=1)
    return Graph

def CreateInternalArcs1x9(pos_x, pos_y, pos_z, nx, ny, Graph):

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

def CreateInternalArcs1x5(pos_x, pos_y, pos_z, nx, ny, Graph):
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



def main():    
    print("Start")
    start_time = time.time() 
    nx, xmn, xsiz = 44, 24300, 16
    ny, ymn, ysiz = 62, 24800, 16
    nz, zmn, zsiz = 26, 3600, 16

    filein = input("Provide the block model file: ")
    BlockModel = np.loadtxt(filein) # Import Block Model
    BlockModel = Pseudoflow_UPL(BM=BlockModel, nx=nx, ny=ny, nz=nz, input=4, VarOut=5)
    
    '''Save Block Model'''
    fileout = input("Provide a name for block model file: ")
    np.savetxt(fname=fileout, X=BlockModel, fmt='%.3f', delimiter='\t')	

    return print("--%s seconds of the whole process-" % (np.around((time.time() - start_time), decimals=2)))  


if __name__ == "__main__":
    main()