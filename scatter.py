# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getScatterPlots(dataFrame, minCorrelation = 0.9):
    checkIfPandasObject.check(dataFrame)
        
    correlation = dataFrame.corr()
        
    for colName, column in correlation.iteritems():
        for rowName, value in column.iteritems():
            if value > minCorrelation and value != 1:
                _plotScatter(dataFrame, colName, rowName)
                    
                #remove opposite value in dataFrame so multiple scatter plots aren't made
                correlation.loc[:, (rowName, colName)] = 0

def _plotScatter(dataFrame, colName, rowName):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
            
    dataFrame.plot.scatter(
        x = colName,
        y = rowName,
        ax=axs
        )
            
    axs.set_title(f'Scatter Plot Showing Correlation Between {colName} and {rowName}')
        