# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:25:54 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getBoxPlots(pandasObject, kwargs):
    assert checkIfPandasObject.check(pandasObject) == "DataFrame", "PandasObject passed must be DataFrame!"
    
    for _, column in pandasObject.iteritems():
        
        if column.dtype != "object" and ["int64", "float64"].index(column.dtype) != None:
            _plotBoxPlotsFromSeries(column, kwargs)
    
    
def _plotBoxPlotsFromSeries(series, kwargs):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    kwargs["ylabel"] = None
    kwargs["ax"] = axs
    
    series.plot.box(**kwargs)
    
    if not "title" in kwargs:
        axs.set_title(f'Box Plot Showing Distribution of {series.name}')
