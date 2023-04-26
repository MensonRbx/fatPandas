
import matplotlib.pyplot as plt
import checkIfPandasObject    

#todo
def getLinePlots(pandasObject, xAxisColumnName):
    checkIfPandasObject.check(pandasObject)
        
    #seems exactly the same as the bar plot, must investigate
        
    for index, column in pandasObject.iteritems():
            
        if column.name != xAxisColumnName:
            _plotLine(pandasObject, xAxisColumnName, column.name)
            
def _plotLine(pandasObject, xAxisName, yAxisName):
        
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
        
    pandasObject.plot.line(
        x = xAxisName,
        y = yAxisName,
        ax=axs            
        )
        
    axs.set_title(f'Line Plot Showing Relationship Between {xAxisName} and {yAxisName}')
     