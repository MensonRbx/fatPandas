# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:44:29 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt
import checkIfPandasObject

def getHistograms(pandasObject):
    assert checkIfPandasObject.check(pandasObject) == "DataFrame", "PandasObject passed must be DataFrame!"
    
    for _, column in pandasObject.iteritems():
        
        if column.dtype != "object" and ["int64", "float64"].index(column.dtype) != None:
            _plotHistogramFromSeries(column)
    
    
def _plotHistogramFromSeries(series):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    series.plot.hist(
        ax=axs,
        ylabel = None,
        bins = round(len(series)/1.33)
        )
    
    axs.set_title(f'Histogram Showing Distribution of {series.name}')