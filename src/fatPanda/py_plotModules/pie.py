# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getPiePlots(pandasObject, kwargs):
     pandasObjectType = checkIfPandasObject.check(pandasObject)
     
     if pandasObjectType == "DataFrame":
         _getPiePlotsFromDataFrame(pandasObject, kwargs)
     elif pandasObjectType == "Series":
         _checkColumnToPiePlot(pandasObject, kwargs)
             
def _getPiePlotsFromDataFrame(dataFrame, kwargs):
     for _, column in dataFrame.iteritems():
         if column.dtype != "object" and (["int64", "float64"].index(column.dtype)) != None:
             _checkColumnToPiePlot(column, kwargs)
                      
def _checkColumnToPiePlot(column, kwargs):
     
    minProportion = ("minProportion" in kwargs and kwargs["minProportion"]) or 0.5
    
    quickComp = [True for value in column if value/column.sum() >= minProportion]
    
    if len(quickComp) > 0:
         _plotPie(column, kwargs)
     

def _plotPie(column, kwargs): #works for series too
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    del kwargs["minProportion"]
     
    kwargs["ax"] = axs
    kwargs["autopct"] = "%.1f%%"
    kwargs["ylabel"] = None
    
    column.plot.pie(**kwargs)
         
    if not "title" in kwargs:
        axs.set_title(f'Pie Chart Showing {column.name} proportion')