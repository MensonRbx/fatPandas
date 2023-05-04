
import matplotlib.pyplot as plt

import string
import random

def random_string(length):
    letters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choice(letters) for i in range(length))

#todo
def getLinePlots(pandasObject, kwargs):
        
    #seems exactly the same as the bar plot, must investigate
        
    for index, column in pandasObject.iteritems():
            
        if column.name != kwargs["x"]:
            _plotLine(pandasObject, column.name, kwargs)
            
def _plotLine(pandasObject, yAxisName, kwargs):
        
    fig, axs = plt.subplots(1, 1, figsize = (5, 5))
    
    kwargs["y"] = yAxisName
    kwargs["ax"] = axs
        
    if not "title" in kwargs:
        axs.set_title(f'Line Plot Showing Relationship Between {kwargs["x"]} and {yAxisName}')
     
    pandasObject.plot.line(**kwargs).get_figure().savefig("temp", f'{random_string(16)}.png')
        