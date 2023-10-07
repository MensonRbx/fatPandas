import re
import json
import uuid
import openai
import logging
import concurrent.futures

import pandas as pd
import matplotlib.pyplot as plt

from json import JSONDecodeError
from rich.console import Console
from rich.theme import Theme

console = Console()
theme = Theme()

requestString = """

Request from Python prog 'Pandas++.' Data tool, uses AI for meaningful data plots. 
Send sample Pandas DF in .json, look for plot data. 
Use Pandas DF plot methods (e.g., df.plot(kind='Bar', x='Year')). 

Response: JSON dict of dicts, each with plot args.

EXAMPLE:
{
     "p1": {
        "kind": "bar",
        "x": "Year",
        "xlabel": "Years"
        },
}

No comments.
Meaningful Plots. 
Prefer Box Plots and Scatter Plots to Histograms. 
Include titles in plot kwargs to describe the plot (add "AI" at the end of title). 
Aim for 10+ subDicts. 
No unclosed brackets/errors. 
Understand the task?

"""

importErrorString = """

The response you have sent contains an import statement.
Assume that all imports needed are already done
and don't include them in your code, please and thanks!

"""

syntaxErrorString = """

The response you have sent contains an syntax error. Please refer to the guidelines
of how to format your response and attempt again, please and thanks!

"""

undefinedErrorString = """ 
Previous reponse, when run with eval, resulted in an error, please generate code again.
"""

MAX_DEPTH = 5
MODEL_NAME = "gpt-3.5-turbo-16k"
VERTICAL_BOX_PLOTS = False
MAX_BAR_PLOT_X_AXIS_LABEL_LENGTH = 5
COLUMN_NAME_BLACKLIST = set([
    "id",
    "date",
    "agency_ids",
    "latitude",
    "longitude"
])

recursion_count = 0

#START OF AI FUNCTIONS
def generateGUID():
    return uuid.uuid4().hex

def sendGPTRequest(conversation, text):
    messageToSend = {"role": "system", "content": text}
    conversation.append(messageToSend)
    return openai.ChatCompletion.create(model=MODEL_NAME, messages=conversation)

def getMessageFromGPTResponse(response):
    return response.choices[0].message.content.strip()

def runCommand(kwargDict, conversation, atErrorDepth):
    
    try:
        plt.figure()
        df.plot(**kwargDict)
        currentPlot = plt.gcf()
        plotName = generateGUID()+".png"
        currentPlot.savefig("generated_images//"+plotName)
        
    except Exception as error:
        plt.figure()
        logging.warning(f"Plot function failed for dict {kwargDict}\n")
        logging.warning(f"Error When Plotting: {error}\n")
        
        """
        TODO: 
            Error Handling
            
        """

def plotGPTCommand(textToSend, conversation, depth):
    assert depth <= MAX_DEPTH, "Maximum depth reaced for recursive plot function! Halting!"
    
    logging.debug(f"Current plot func depth: {depth}")
    
    depth = depth or 0
    conversation = conversation or []
    
    logging.debug("Sending request to GPT...")
    GPT_response = sendGPTRequest(conversation, textToSend)
    GPT_message = getMessageFromGPTResponse(GPT_response)
    logging.debug("Received GPT Response")
    
    logging.debug(GPT_message)
    
    dictList = json.loads(GPT_message)
    
    for _, kwargDict in dictList.items():
        logging.debug(f"kwargDict: {str(kwargDict)}")
        runCommand(kwargDict, conversation, False)
        
    """
    Commented out part is for concurrent execution, not needed currently but keeping in case needed.
    """
   
    # with concurrent.futures.ThreadPoolExecutor(max_workers=len(dictList)) as executor:
    #     logging.debug("Starting Thread Pool Executor")
    #     for _, kwargDict in dictList.items():
    #         logging.debug(f"kwargDict: {str(kwargDict)}")
    #         executor.submit(runCommand, kwargDict, conversation, False)
    
    
def beginAIPlotProcess():
    
    logging.info("Pandas++ Starting")
    
    conversation = []
    sendGPTRequest(conversation, requestString)
    dfSample = df.sample(30).to_json() + "\n\n" + str(df.dtypes)
    
    logging.info("Initial prompt finished. Starting plotting function")
    
    plotGPTCommand(dfSample, conversation, 0)   
#END OF AI FUNCTIONS

#START OF NON-AI FUNCTIONS

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

def scrapeDataFrameForPlots(df, dfname, fromGroupBy):
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
                
        elif dtype == "object" and not fromGroupBy:
            
            columnSeries = df[colname]
            
            if len(list(set(columnSeries))) < 10:
                columnGroupBy = df.groupby(colname)
                for _, group in columnGroupBy:
                    newName = f"{dfname}/{colname}/{group[colname].values[0]}" 
                    scrapeDataFrameForPlots(group, newName, True)
                    

#END OF NON-AI FUNCTIONS

df = pd.read_csv("datasets/fatal-police-shootings-data.csv")
dfname = "Fatal Police Shootings in America"
openai.api_key = "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"

def main():
    
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%m:%S",
        # filename="log.log"
    )
    
    logging.info("\nStarting AI Plots\n")
    logging.info("\n",df.dtypes,"\n")
    
    beginAIPlotProcess()
    
    logging.info("\nAI Plots Finished! Starting Plot Scrapper\n")
    
    scrapeDataFrameForPlots(df, dfname, False)
    
    logging.info("Execution Completed!\n")
 
if __name__ == "__main__":
    main()


