#Utils module is part of the gPit software  (https://github.com/GuilhermeMene/gPit)
#Copyright (c) 2023 gPit Developers 
#Distributed under the terms of MIT License (https://github.com/GuilhermeMene/gPit/blob/main/LICENSE)


import pandas as pd
import numpy as np 
from gpit import logger as log

def mergeNP(blockmodel, PitNames):

    #Function to merge differents nested pits into one column 
    #Prepare the list of pits for correct interations 
    PitNames.sort(reverse=True)

    if isinstance(PitNames, list): 
        if isinstance(blockmodel, pd.DataFrame):
            #Create a numpy array of zeros 
            mergedPit = np.zeros(len(blockmodel))
            try:
                for pn in range(0, len(PitNames)):
                    for idx, row in blockmodel.iterrows():   
                        if row[PitNames[pn]] == 1:
                            mergedPit[idx] = pn+1

                blockmodel['Pits'] = mergedPit
            except Exception as e: log.datalogger(e)            
        else: 
            log.datalogger("The Blockmodel must be a pandas dataframe. ")
    else: 
        log.datalogger("The Pit Names must be a list of nested pits. ")

    return blockmodel

def calcNPStats(blockmodel, PitNames, epvCol, blockTonnes):

    #Function to calculate the statistics from nested pits
    #This function return a table with NPV, ore tonnes, and waste tonnes of nested pits 

    #Prepare the list of pits for correct interations 
    PitNames.sort()

    if isinstance(PitNames, list) and isinstance(epvCol, list): 

        if len(PitNames) == len(epvCol): 
            #Create the variables 
            orevolume = np.zeros(len(PitNames))
            wastevolume = np.zeros(len(PitNames))
            npv = np.zeros(len(PitNames))

            if isinstance(blockmodel, pd.DataFrame):
                try:
                    for pn in range(0, len(PitNames)):

                        pitbm = blockmodel[blockmodel[PitNames[pn]] == 1]

                        orevolume[pn] = (pitbm[epvCol[pn]][pitbm[epvCol[pn]] > 0].count() * blockTonnes)
                        wastevolume[pn] = (pitbm[epvCol[pn]][pitbm[epvCol[pn]] < 0].count() * blockTonnes)
                        npv[pn] = (pitbm[epvCol[pn]].sum())
                except Exception as e: log.datalogger(e)

            else: 
                log.datalogger("The blockmodel must be a pandas dataframe. ")

        else: 
            log.datalogger("The length of Pitnames must be equal to the length of the epvCol")

    else: 
        log.datalogger("The PitNames and epvCol must be a list. ")


    #Create a pandas dataframe 
    d = {
        'Pit': PitNames, 
        'OreVolume': orevolume,
        'WasteVolume': wastevolume,
        'NPV': npv
    }
    stats = pd.DataFrame(data=d)

    return stats

def calcStat(blockmodel, PitCol:str, epvCol:str, blockTonnes):

    #Function to calculate a single column statistics
    if isinstance(blockmodel, pd.DataFrame):
        if isinstance(epvCol, str):

            pitbm = blockmodel[blockmodel[PitCol] == 1]

            orevolume = (pitbm[epvCol][pitbm[epvCol] > 0].count() * blockTonnes)
            wastevolume = (pitbm[epvCol][pitbm[epvCol] < 0].count() * blockTonnes)
            npv = pitbm[epvCol].sum()

        else: 
            log("The epvCol must be a string with the colume name to calculate the stats. ")
    else: 
        log("the blockmodel must be a padans dataframe. ")


    return orevolume, wastevolume, npv













