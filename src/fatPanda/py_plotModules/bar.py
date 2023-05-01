# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getBarPlots(dataFrame, kwargs):
    checkIfPandasObject.check(dataFrame)
        
    #what makes a plot meaningful?
    print(kwargs)
        
    for index, column in dataFrame.iteritems():
            
        if column.name != kwargs["x"]:
            _plotBar(dataFrame, column.name, kwargs)
            
            
def _plotBar(dataFrame, yAxisName, kwargs):
        
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    kwargs["y"] = yAxisName
    kwargs["ax"] = axs
        
    dataFrame.plot.bar(**kwargs)
        
    x = kwargs["x"]
    
    if not "title" in kwargs:
        axs.set_title(f'Bar Plot Showing Relationship Between {x} and {yAxisName}')
