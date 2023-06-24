# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:54:22 2023
@author: mensonrbx
Description: Module created with purpose of 
automating Data Analytics with pandas.

TODO: 
    
    
    
"""

#Base imports
import os 
import sys
import time

module_path = os.path.abspath(os.path.join(os.getcwd(), 'src/fatPanda/'))
sys.path.append(module_path)

time.sleep(1)

import scatter
import pie
import bar
import line
import hist
import box
import area
import checkIfPandasObject


plotDict = {
    "pie": pie.getPiePlots,
    "scatter": scatter.getScatterPlots,
    "bar": bar.getBarPlots,
    "line": line.getLinePlots,
    "hist": hist.getHistograms,
    "box": box.getBoxPlots,
    "area": area.getAreaPlots
}

class FatPanda:    
    
    def __init__(self):
        pass
    
    def getPlots(self, pandasObject, *, kind, kwargs):
       # print(*args)
        
        if not kind:
            return
            
        checkIfPandasObject.check(pandasObject)
        
        plotDict[kind](pandasObject, kwargs)
        
if __name__ == "__main__":
    pass
