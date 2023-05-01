# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:54:22 2023
@author: mensonrbx
Description: Module created with purpose of 
automating Data Analytics with pandas.

TODO: 
    
    
    
"""

#Base imports
import pandas as pd

from py_plotModules import scatter, pie, bar, line, hist, box, area

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
    def getPlots(self, pandasObject, *, kind, kwargs):
       # print(*args)
        
        if not kind:
            return
        
        plotDict[kind](pandasObject, kwargs)

instance = FatPanda()
df = pd.read_csv("py_testdata/ibis-product-group-sales-report.csv")

instance.getPlots(
    df,
    kind = "hist",
    kwargs = {
        #"title": "Test","
        #"orientation": "horizontal"
    }
)
