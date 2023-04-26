# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:54:22 2023
@author: mensonrbx
Description: Module created with purpose of 
automating Data Analytics with pandas.
"""

#Base imports
import pandas as pd

import scatter
import pie
import bar
import line

plotDict = {
    "pie": pie.getPiePlots,
    "scatter": scatter.getScatterPlots,
    "bar": bar.getBarPlots,
    "line": line.getLinePlots 
}

class FatPanda:    
    def getPlots(self, pandasObject, kind = "bar", *args):
        print(kind)
        plotDict[kind](pandasObject, *args)

instance = FatPanda()
df = pd.read_csv("ibis-product-group-sales-report.csv")

instance.getPlots(
    df,
    "line",
    "Year/Month"
)
