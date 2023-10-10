#Blockmodel module is part of the gPit software  (https://github.com/GuilhermeMene/gPit)
#Copyright (c) 2023 gPit Developers 
#Distributed under the terms of MIT License (https://github.com/GuilhermeMene/gPit/blob/main/LICENSE)

import numpy as np
import pandas as pd


class BlockModel:

    def __init__(self, bmpath:str):

        self.MinCost = 0
        self.ProcCost = 0

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
            'zs': zs, 
            'volume': xs*ys*zs
        }
        return self   

    def setEPVParms(self, metal:str, unit:str, mprice:float, sel_cost:float, recovery:float, dilution:float):        

        #Set the BM parameters 
        self.EPVparms = {}
        self.EPVparms[metal] = {
            'unit': unit,
            'mprice': mprice ,
            'sel_cost': sel_cost ,
            'recovery': recovery, 
            'dilution' : dilution
        }  

    def setCosts(self, mincost:float, proccost:float):

        #Check mine and proc costs 
        if self.MinCost == 0 and self.ProcCost == 0:
            self.MinCost = mincost
            self.ProcCost = proccost
        else: 
            pass

        return self      
    
    def calculateCutOff(self, metal:str, unit='percent'):

        #Check the unit of the calculation 
        if unit == 'percent':
            try: 
                self.CutOffGrade = ((self.MinCost + (self.ProcCost*(1 + self.EPVparms[metal]['dilution']))) / 
                                        (((self.EPVparms[metal]['mprice'] - self.EPVparms[metal]['sel_cost'])*22.046)*self.EPVparms[metal]['recovery']))
            except: 
                print("Set the economic parameters first")

        elif unit == 'ozt':
            try:
                self.CutOffGrade = (((self.MinCost + (self.ProcCost*(1 + self.EPVparms[metal]['dilution']))) / 
                                    ((self.EPVparms[metal]['mprice'] - self.EPVparms[metal]['sel_cost'])*self.EPVparms[metal]['recovery']))*31.1)
            except:
                print("Set the economic parameters first")

        else: 
            print("Set the correct unit for the Cut-Off grade calculation")

        return self

    def calcEPV(self, OreGrade, Unit, Density):

        mrecvalue = 0 
        block_value = []

        """
        #Check the OreGrade input and set 
        if isinstance(OreGrade, list):
            metal = OreGrade[0]
        else:
            metal = OreGrade
        """

        #Check and calculate the density of each block 
        if isinstance(Density, str):
            self.tonnes = [self.bmparms['volume'] * self.blockmodel[Density] for self.blockmodel[Density] in self.blockmodel[Density]]
        if isinstance(Density, float):
            bmlen = [0] * len(self.blockmodel) 
            self.tonnes = [self.bmparms['volume'] * Density for bmlen in bmlen]

        for ind in self.blockmodel.index:
            if self.blockmodel[OreGrade][ind] < self.CutOffGrade:
                block_value.append(-self.MinCost * self.tonnes[ind])
            else: 
                #Check if one or more metals 
                #Only one metal passed as string 
                if isinstance(OreGrade, str) and isinstance(Unit, str):

                    if Unit == "ozt":
                        #Block value for process calculation
                        block_value.append(((self.blockmodel[OreGrade][ind] * self.EPVparms[OreGrade]['recovery'] * self.tonnes[ind] *  
                                            (self.EPVparms[OreGrade]['mprice'] - self.EPVparms[OreGrade]['sel_cost'])) - ((self.MinCost + self.ProcCost) * self.tonnes[ind])))
                    if Unit == "percent":
                        #Block value for process calculation
                        block_value.append((((self.blockmodel[OreGrade][ind]/100) * self.EPVparms[OreGrade]['recovery'] * self.tonnes[ind] *  
                                            ((self.EPVparms[OreGrade]['mprice'] - self.EPVparms[OreGrade]['sel_cost']) * 2204)) - ((self.MinCost + self.ProcCost) * self.tonnes[ind])))

                #More than one metal passed by list 
                if isinstance(OreGrade, list) and isinstance(Unit, list):

                    for m in OreGrade:
                        if Unit[m] == "ozt":
                            #Calculate the Troy ounce value 
                            mrecvalue += (self.tonnes[ind] * self.blockmodel[OreGrade][ind] * self.EPVparms[OreGrade[m]]['recovery'] * 
                                            (self.EPVparms[OreGrade[m]]['mprice'] - self.EPVparms[OreGrade[m]]['sel_cost']))
                        if Unit[m] == "percent":
                            #Calculate the Percent value
                            mrecvalue += ((self.tonnes[ind] * (self.blockmodel[OreGrade][ind])/100) * self.EPVparms[OreGrade[m]]['recovery'] * 
                                            (self.EPVparms[OreGrade[m]]['mprice'] - self.EPVparms[OreGrade[m]]['sel_cost']))
                        else:
                            print("The Unit must be 'ozt' or 'percent'")

                    #DEBUG
                    print(mrecvalue)


                    #Block value for process calculation
                    block_value.append(mrecvalue - (self.tonnes[ind] * (self.MinCost + self.ProcCost)))



        #Create the EPV into blockmodel dataframe 
        self.blockmodel['EPV'] = block_value

        return self
