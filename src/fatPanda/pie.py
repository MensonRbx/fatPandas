# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

def getPiePlots(pandasObject, kwargs):
    
     if pandasObject.__class__.__name__ == "DataFrame":
         _getPiePlotsFromDataFrame(pandasObject, kwargs)
     elif pandasObject.__class__.__name__ == "Series":
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
    
    kwCopy = kwargs.copy()
    
    del kwCopy ["minProportion"]
     
    kwCopy["ax"] = axs
    kwCopy["autopct"] = "%.1f%%"
    kwCopy["ylabel"] = None
    
    if not "title" in kwCopy:
        axs.set_title(f'Pie Chart Showing {column.name} proportion')
    
    home_dir = os.getcwd() 
    fileName = f'{random_string(16)}.png'
    path = f"{home_dir}\\temp\\{fileName}"
    
    column.plot.pie(**kwCopy).get_figure().savefig(path)
         
        
        
if __name__ == "__main__":
    
    df = pd.DataFrame([[10, 1, 3], [9, 3, 1], [12, 2, 0]], ["Jojo", "One Piece", "NGE"], ["Number of Viewers", "Episides", "Rating"])
    getPiePlots(df, {"minProportion": 0.5})
    