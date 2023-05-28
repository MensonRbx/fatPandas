# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:24:46 2023

@author: BigBoy
"""

import os
import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

def getBarPlots(dataFrame, kwargs):
        
    #what makes a plot meaningful?
        
    for index, column in dataFrame.iteritems():
            
        if column.name != kwargs["x"]:
            _plotBar(dataFrame, column.name, kwargs)
            
            
def _plotBar(dataFrame, yAxisName, kwargs):
        
    print("PLOTTING BAR")
    
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    kwargs["y"] = yAxisName
    kwargs["ax"] = axs
        
    x = kwargs["x"]
    
    if not "title" in kwargs:
        axs.set_title(f'Bar Plot Showing Relationship Between {x} and {yAxisName}')
    
    #path to saveto
    
    home_dir = os.getcwd()
    fileName = f'{random_string(16)}.png'
    path = f"{home_dir}\\temp\\{fileName}"

    dataFrame.plot.bar(**kwargs).get_figure().savefig(path)
    
