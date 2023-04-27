# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:25:54 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getBoxPlots(pandasObject):
    assert checkIfPandasObject.check(pandasObject) == "DataFrame", "PandasObject passed must be DataFrame!"
    
    for _, column in pandasObject.iteritems():
        
        if column.dtype != "object" and ["int64", "float64"].index(column.dtype) != None:
            _plotBoxPlotsFromSeries(column)
    
    
def _plotBoxPlotsFromSeries(series):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    series.plot.box(
        ax=axs,
        ylabel = None,
        )
    
    axs.set_title(f'Box Plot Showing Distribution of {series.name}')