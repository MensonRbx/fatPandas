# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:44:29 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

def getHistograms(pandasObject, kwargs):
    
    for _, column in pandasObject.iteritems():
        
        if column.dtype != "object" and ["int64", "float64"].index(column.dtype) != None:
            _plotHistogramFromSeries(column, kwargs)
    
    
def _plotHistogramFromSeries(series, kwargs):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    kwargs["ax"] = axs
    kwargs["ylabel"] = None
    
    if not "bins" in kwargs:
        kwargs["bins"] = round(len(series)/1.33)
    
    if not "title" in kwargs:
        axs.set_title(f'Histogram Showing Distribution of {series.name}')
        
    series.plot.hist(**kwargs).get_figure().savefig(f'{random_string(16)}.png')