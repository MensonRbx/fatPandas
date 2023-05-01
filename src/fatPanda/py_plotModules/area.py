# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:54:32 2023

@author: BigBoy
"""
import matplotlib.pyplot as plt
import checkIfPandasObject

def getAreaPlots(pandasObject, kwargs):
    assert checkIfPandasObject.check(pandasObject) == "DataFrame", "PandasObject passed must be DataFrame!"
    
    axs = None
    
    if kwargs["stacked"]:
        _, axs = plt.subplots(1, 1, figsize = (5, 5))
        
    for index, column in pandasObject.iteritems():
            
        if column.name != kwargs["x"]:
            _plotAreaPlotsFromSeries(pandasObject, column, axs, kwargs)
    
    
def _plotAreaPlotsFromSeries(pandasObject, series, axs, kwargs):
    
    if axs:
        kwargs["ax"] = axs 
    else:
        _, axs = plt.subplots(1, 1, figsize = (5, 5))
        kwargs["ax"] = axs
        
    series.plot.area(**kwargs)
    
    if not "title" in kwargs:
        axs.set_title('Area Plot')