import pandas as pd
import matplotlib.pyplot as plt
import re

"""
SETTINGS:
    VERTICAL_BOX_PLOTS: 
        Used to change box plots to horizontal
    
    MAX_BAR_PLOT_X_AXIS_LABEL_LENGTH: 
        Used to determine if to plot bar chart verically or horizontally based on
        average length of string in column
        
    COLUMN_NAME_BLACKLIST:
        List of names of columns to always ignore
        
"""

#START_OF_SETTINGS

VERTICAL_BOX_PLOTS = False
MAX_BAR_PLOT_X_AXIS_LABEL_LENGTH = 5
COLUMN_NAME_BLACKLIST = set([
    "id",
    "date",
    "agency_ids",
    "latitude",
    "longitude"
])

#END_OF_SETTINGS

recursion_count = 0

df = pd.read_csv("datasets/fatal-police-shootings-data.csv")

"""
Function purpose:
    Converts strings of "technical" formats (i.e type_of_food) 
    to plain English ("Type of Food")
"""
def normalizeString(inputString):
    words = re.split(r'_', inputString)
    return ' '.join(word.capitalize() if len(word) >= 2 else word for word in words)

def plotDist(df, dfname, colname):
    plotTitle = normalizeString(f"Distribution of {colname} in {dfname} data")
    
    binsToPlot = 20 #max(abs(round(len(df[colname])/2)), 30)
    
    #make histogram with title
    plt.figure()
    plt.hist(df[colname], bins = binsToPlot)
    plt.title(plotTitle)
    
    #clear
    plt.figure()
    
    #make box plot with title
    df[colname].plot.box(
        title = plotTitle, 
        vert = VERTICAL_BOX_PLOTS
    )
    
def plotPie(df, dfname, colname):
    
    plt.figure()
    
    df[colname].value_counts().plot.pie(
        title = normalizeString(f"Proportion of values in {colname} in {dfname} data"),
        autopct = "%.1f%%",
    )
    
def plotBarChartWithTopValues(df, xAxisColumnName, yAxisColumnName):
    #df: pandas DataFrame
    #xAxisColumnName: columnName with object (assumed to be string) type values
    #yAxisColumnName: columnName with number type values
    
    plotTitle = normalizeString(f"{xAxisColumnName} and {yAxisColumnName}")
    plotType = "bar"
    dfToPlot = df.sort_values(by = yAxisColumnName, ascending = False).head(10)
    averageStringLength = round(df[xAxisColumnName].str.len().value_counts().mean())
    
    if averageStringLength > MAX_BAR_PLOT_X_AXIS_LABEL_LENGTH:
        plotType = "barh"
        dfToPlot = dfToPlot.sort_values(by = xAxisColumnName, ascending = True)
        
    dfToPlot.plot(
        kind = plotType,
        title = plotTitle, 
        x = xAxisColumnName, 
        y = yAxisColumnName
    ).legend(
        bbox_to_anchor = (1.0, 1.0),
        #fontsize = 'small',
    )
        
#Plot functions linked to the data type of a column
dtypePlotMap = {
    "bool": plotPie,
    "int64": plotDist,
    "float64": plotDist
    }

#Plot functions liked to data type of column: checked when object column found, compares object columns with datatypes
objectPlotMap = {
    "int64": plotBarChartWithTopValues,
    "float64": plotBarChartWithTopValues
}

def createPlotsWithObjectDtype(df, objectColumnName):
    for colname in df:
        if colname == objectColumnName or colname in COLUMN_NAME_BLACKLIST:
            continue
        dtype = str(df[colname].dtype)
        if dtype in objectPlotMap.keys():
            objectPlotMap[dtype](df, objectColumnName, colname)

def checkForOtherNumberColumnForScatterPlots(df, xColumnName):
    pass

def main(df, dfname, fromGroupBy):
    global recursion_count
    
    print(f"main called with recusion count of {recursion_count}")
    
    recursion_count += 1
    
    df = df.ffill()
    for colname in df:
        if colname in COLUMN_NAME_BLACKLIST:
            continue
        
        dtype = str(df[colname].dtype)
        if dtype in dtypePlotMap.keys():
            dtypePlotMap[dtype](df, dfname, colname)
                
        elif dtype == "object" and not fromGroupBy:
            
            columnSeries = df[colname]
            
            #Create group
            if len(list(set(columnSeries))) < 10:
                columnGroupBy = df.groupby(colname)
                for _, group in columnGroupBy:
                    newName = f"{dfname}/{colname}/{group[colname].values[0]}" 
                    main(group, newName, True)
                    
            
            # _tempDf = df.groupby(colname)
            
            # createPlotsWithObjectDtype(df, colname)
                
         
main(df, "Fatal Police Shootings", False)

