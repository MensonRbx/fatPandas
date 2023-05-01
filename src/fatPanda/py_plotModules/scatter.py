# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getScatterPlots(dataFrame, kwargs):
    checkIfPandasObject.check(dataFrame)
        
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
            
    kwargs["x"] = colName
    kwargs["y"] = rowName
    kwargs["ax"] = axs
    
    dataFrame.plot.scatter(**kwargs)
            
    if not "title" in kwargs:
        axs.set_title(f'Scatter Plot Showing Correlation Between {colName} and {rowName}')
        