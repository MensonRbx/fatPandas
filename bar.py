# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getBarPlots(dataFrame, xAxisColumnName = "Year"):
    checkIfPandasObject.check(dataFrame)
        
    #what makes a plot meaningful?
        
    for index, column in dataFrame.iteritems():
            
        if column.name != xAxisColumnName:
            _plotBar(dataFrame, xAxisColumnName, column.name)
            
            
def _plotBar(dataFrame, xAxisName, yAxisName):
        
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
        
    dataFrame.plot.bar(
        x = xAxisName,
        y = yAxisName,
        ax=axs
    )
        
    axs.set_title(f'Bar Plot Showing Relationship Between {xAxisName} and {yAxisName}')
