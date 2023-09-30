#Pseudoflow module is part of the gPit software  (https://github.com/GuilhermeMene/gPit)
#Copyright (c) 2023 gPit Developers 
#Distributed under the terms of MIT License (https://github.com/GuilhermeMene/gPit/blob/main/LICENSE)

#Based on Sebastian Avalos code disributed under MIT License 
#https://github.com/geometatqueens/2020-Pseudoflow-Python



import numpy as np
import networkx as NetX
import pseudoflow as pf
import pandas as pd

import precedence as prec


class Pseudoflow:

    def __init__(self, blockmodel, bmParms):

        try: 
            #Create the inputs 
            if isinstance(blockmodel, pd.DataFrame):
                self.blockmodel = blockmodel
            else: 
                print("The blockmodel must be a pandas Dataframe")

            if len(bmParms) == 10: 
                self.bmParms = bmParms
            else: 
                print("The blockmodel Parameters must contain 10 parameters - Set the blockmodel parameters first")

        except Exception as e: print(e)

        #Set the EPV variable 
        self.EPV = self.blockmodel['EPV'].to_numpy

        #Set the Graph 
        self.Graph = NetX.DiGraph()

        #Create the Sink 
        self.sink = np.Int64(self.bmParms.nx * self.bmParms.ny * self.bmParms.nz + 1)

    def UPL(self, precedence:str):

        source = 0        
        
        #Create the external arcs 
        self.Graph = self.CreateExtArcs()

        #Create Internal arcs 
        for ind_z in range(self.bmParms.nz - 1):
            pos_z = self.bmParms.nz - ind_z - 2
            for pos_y in range(ind_z + 1, self.bmParms.ny - ind_z - 1):
                for pos_x in range(ind_z + 1, self.bmParms.nx - ind_z - 1):

                    if precedence == '1x5':
                        self.Graph = prec.IA1x5(pos_x, pos_y, pos_z, self.bmParms.nx, self.bmParms.ny, Graph=self.Graph)
                    if precedence == '1x9':
                        self.Graph = prec.IA1x9(pos_x, pos_y, pos_z, self.bmParms.nx, self.bmParms.ny, Graph=self.Graph)
                    else:
                        print("The precedence must be '5x1' or '9x1' ")
                        break

        #Solving the minimum cut problem via pf.hpf solver
        RngLambda = [0]
        breakpoints, cuts, info = pf.hpf(self.Graph, source, self.sink, const_cap="const", mult_cap="mult", lambdaRange=RngLambda, roundNegativeCapacity=False)

        #Get the UPL inside values 
        B = {x:y for x, y in cuts.items() if y == [1] and x!=0}
        InsideList = list(B.keys())

        #Create a numpy array with zeros 
        self.upl = np.zeros(len(self.EPV))

        for indUPL in range(len(InsideList)):         
            # Set blocks inside UPL as one
            self.upl[np.int64(InsideList[indUPL] -1)] = 1  

        return self 


    def CreateExtArcs(self):

        for t_z in range(self.bmParms.nz):
            pos_z = self.bmParms.nz - t_z - 1
            for t_y in range(t_z, self.bmParms.ny-t_z):
                for t_x in range(t_z,self.bmParms.nx-t_z):
                    p_i = 1 + t_x + self.bmParms.nx*t_y + self.bmParms.ny*self.bmParms.nx*pos_z 
                    Capacity = np.absolute(np.around(self.EPV[p_i-1], decimals=2))
                    if self.EPV[p_i-1] < 0: #Negative local Economic Value
                        self.Graph.add_edge(p_i, self.sink, const=Capacity, mult=-1)
                    else:
                        self.Graph.add_edge(0, p_i, const=Capacity, mult=1)

        return self

