# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:54:32 2023

@author: BigBoy
"""
import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

def getAreaPlots(pandasObject, kwargs):
    
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
    
    if not "title" in kwargs:
        axs.set_title('Area Plot')    
    
    series.plot.area(**kwargs).get_figure().savefig(f'temp/{random_string(16)}.png')
