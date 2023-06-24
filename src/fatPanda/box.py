# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:25:54 2023

@author: BigBoy
"""

import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

def getBoxPlots(pandasObject, kwargs):
    
    for _, column in pandasObject.iteritems():
        
        if column.dtype != "object" and ["int64", "float64"].index(column.dtype) != None:
            _plotBoxPlotsFromSeries(column, kwargs)
    
    
def _plotBoxPlotsFromSeries(series, kwargs):
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    kwargs["ylabel"] = None
    kwargs["ax"] = axs
    
    if not "title" in kwargs:
        axs.set_title(f'Box Plot Showing Distribution of {series.name}')

    series.plot.box(**kwargs).get_figure().savefig(f'{random_string(16)}.png')
    