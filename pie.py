# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getPiePlots(pandasObject, argumentDict = {}, minProportion = 0.4):
     pandasObjectType = checkIfPandasObject.check(pandasObject)
     
     if pandasObjectType == "DataFrame":
         _getPiePlotsFromDataFrame(pandasObject, minProportion, argumentDict)
     elif pandasObjectType == "Series":
         _checkColumnToPiePlot(pandasObject, minProportion, argumentDict)
             
def _getPiePlotsFromDataFrame(dataFrame, minProportion, argumentDict):
     for _, column in dataFrame.iteritems():
         if column.dtype != "object" and (["int64", "float64"].index(column.dtype)) != None:
             _checkColumnToPiePlot(column, minProportion, argumentDict)
                      
def _checkColumnToPiePlot(column, minProportion, argumentDict):
     
     quickComp = [True for value in column if value/column.sum() >= minProportion]
     
     if len(quickComp) > 0:
         _plotPie(column, argumentDict)
     

def _plotPie(column, argumentDict): #works for series too
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
     
    argumentDict["ax"] = axs
    argumentDict["autopct"] = "%.1f%%"#
    argumentDict["shadow"] = True
    argumentDict["ylabel"] = None
         
    column.plot.pie(
        ax=axs,
        ylabel = None,
        autopct = "%.1f%%",
        shadow = True,
        #labels = None
        )
         
    axs.set_title(f'Pie Chart Showing {column.name} proportion')