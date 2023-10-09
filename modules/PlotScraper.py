import re
import matplotlib.pyplot as plt

MAX_ERROR_DEPTH = 5
VERTICAL_BOX_PLOTS = False
MAX_BAR_PLOT_X_AXIS_LABEL_LENGTH = 5
COLUMN_NAME_BLACKLIST = set([
    "id",
    "date",
    "agency_ids",
])
SAVE_PLOTS = False

recursion_count = 0

def normalizeString(inputString):
    words = re.split(r'_', inputString)
    return ' '.join(word.capitalize() if len(word) >= 2 else word for word in words)

def plotDist(df, dfname, colname):
    plotTitle = normalizeString(f"Distribution of {colname} in {dfname} data")
    
    binsToPlot = max(abs(round(len(df[colname])/2)), 30)
    
    #make histogram with title
    plt.figure()
    plt.hist(df[colname], bins = binsToPlot, density=True)
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

scatterPlotTypes = set(["int64", "float64"])

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

def checkForOtherNumberColumnForScatterPlots(df, dfname, xColumnName):
    for otherColumnName in df:
        if (otherColumnName == xColumnName) or (otherColumnName in COLUMN_NAME_BLACKLIST) or len(list(set(df[otherColumnName]))) < 10:
            continue
        dtype = str(df[otherColumnName].dtype)
        if dtype in scatterPlotTypes:
            plotTitle = normalizeString(f"Correlations between {xColumnName} and {otherColumnName} in {dfname}")
            df.plot(
                kind = "scatter",
                x = xColumnName,
                xlabel = normalizeString(xColumnName),
                y = otherColumnName,
                ylabel = normalizeString(otherColumnName),
                title = plotTitle
            )
    pass

def PlotScrape(df, dfname, fromGroupBy):
    global recursion_count
    
    print(f"scrapeDataFrameForPlots called with recusion count of {recursion_count}")
    
    recursion_count += 1
    
    df = df.ffill()
    for colname in df:
        if colname in COLUMN_NAME_BLACKLIST:
            continue
        
        dtype = str(df[colname].dtype)
        if dtype in dtypePlotMap.keys():
            dtypePlotMap[dtype](df, dfname, colname)
            if dtype in scatterPlotTypes:
                checkForOtherNumberColumnForScatterPlots(df, dfname, colname)
                
        elif dtype == "object" and not fromGroupBy:
            columnSeries = df[colname]
            if len(list(set(columnSeries))) < 10:
                columnGroupBy = df.groupby(colname)
                for _, group in columnGroupBy:
                    newName = f"{dfname}/{colname}/{group[colname].values[0]}" 
                    PlotScrape(group, newName, True)