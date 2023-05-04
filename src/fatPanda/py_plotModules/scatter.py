# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import sys

import pandas as pd
import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

def getScatterPlots(dataFrame, kwargs):
    
    kwargs = kwargs.copy()
        
    minCorrelation = kwargs["minCorrelation"] or 0.9
    del kwargs["minCorrelation"]
    
    correlation = dataFrame.corr()
        
    for colName, column in correlation.iteritems():
        for rowName, value in column.iteritems():
            if value > minCorrelation and value != 1:
                _plotScatter(dataFrame, colName, rowName, kwargs)
                    
                #remove opposite value in dataFrame so multiple scatter plots aren't made
                correlation.loc[:, (rowName, colName)] = 0

def _plotScatter(dataFrame, colName, rowName, kwargs):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
            
    print("ERE")
    
    kwargs["x"] = colName
    kwargs["y"] = rowName
    kwargs["ax"] = axs
    
            
    if not "title" in kwargs:
        axs.set_title(f'Scatter Plot Showing Correlation Between {colName} and {rowName}')
        
    dataFrame.plot.scatter(**kwargs).get_figure().savefig(f'{random_string(16)}.png')
        
if __name__ == "__main__":
    
    df = pd.DataFrame([[10, 1, 3], [9, 3, 1], [12, 2, 0]], ["Jojo", "One Piece", "NGE"], ["Number of Viewers", "Episides", "Rating"])
    getScatterPlots(df, {"minCorrelation": 0.9})