# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:54:22 2023

@author: mensonrbx

Description: Module created with purpose of 
automating Data Analytics with pandas.
"""

import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass

@dataclass(frozen=True)
class FatPanda:
    
    def getScatterPlots(self, dataFrame, minCorrelation = 0.9):
        self._verifyIfDataFrame(dataFrame)
        
        correlation = dataFrame.corr()
        
        for colName, column in correlation.iteritems():
            for rowName, value in column.iteritems():
                if value > minCorrelation and value != 1:
                    self._plotScatter(dataFrame, colName, rowName)
                    
                    #remove opposite value in dataFrame so multiple scatter plots aren't made
                    correlation.loc[:, (rowName, colName)] = 0

    def _plotScatter(self, dataFrame, colName, rowName):
        fig, axs = plt.subplots(1, 1, figsize = (5, 5))
            
        dataFrame.plot.scatter(
            x = colName,
            y = rowName,
            ax=axs
        )
            
        axs.set_title(f'Scatter Plot Showing Correlation Between {colName} and {rowName}')
        
    def getPiePlots(self, dataFrame, minProportion = 0.4):
        self._verifyIfDataFrame(dataFrame)
        
        for _, column in dataFrame.iteritems():
            if (["int64", "float64"].index(column.dtype)) != None:
                self._checkColumnToPiePlot(column, minProportion)
                         
    def _checkColumnToPiePlot(self, column, minProportion):
        
        #see if anything is greater than 0.4
        quickComp = [value/column.sum() for value in column if value/column.sum() >= minProportion]
        
        if len(quickComp) > 0:
            self._plotPie(column)
        

    def _plotPie(self, column):
        fig, axs = plt.subplots(1, 1, figsize = (5, 5))
            
        column.plot.pie(
            ax=axs,
            ylabel = None,
            autopct = "%.1f%%",
            shadow = True,
            labels = None
            ).legend(column.index)
            
        axs.set_title(f'Pie Chart Showing {column.name} proportion')
        
    def _verifyIfDataFrame(self, dataFrame):
        assert isinstance(dataFrame, pd.DataFrame), "Object is not a Dataframe!"
            
            
instance = FatPanda()

df = pd.DataFrame(
    [[9.1, 173, 3], [9.3, 96, 4], [8.2, 106, 1]],           #data
    ["Spongebob", "Ben 10", "Family Guy"]                   #row index
)
df.columns = ["Show Rating", "Episodes", "Shows Per Week"]  #columns

instance.getPiePlots(df)
