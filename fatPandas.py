import openai
# import asyncio
# import json
import uuid
# import time
# import nest_asyncio
# nest_asyncio.apply()

import pandas as pd
import matplotlib.pyplot as plt

from rich.console import Console
from rich.theme import Theme

console = Console()
theme = Theme()

requestString = """

Hello! This is a request from a Python program called "FatPandas". 
It is a data analytics tool that uses AI in order to come up with meaningful plots of data. 
Uou will be sent a sample of a Pandas Dataframe in .json format, which you will look at and look for 
data to plot. Look for data that can be plotted using all of the plotting methods build into
pandas DataFrames (i.e. df.plot(kind = "Bar", x = "Year")).

Do not import any modules or define any new variables! Importing will result in an error so make the
code assuming pandas has already been imported as pd. Only use methods of plotting which are methods of pandas
DataFrames. The DataFrame you'll use to plot from is called df, and it has already been defined in this program.

Please Include no comments.

Prefer Box Plots to Histograms.

Your response will be run using the built-in eval function in python. Please do not include any characters
that would cause the code to fail!

Please include titles when creating plots, and include it in the df.plot!

Split each command using a semicolon (;) so that I can split each command and run each of them separately.

The dataframe sample will be sent to you after your reponse to this message is processed. Include no commands in this
message, only in the next. Do you understand the task?

"""

# requestString = """
#     MESSAGE IN TELEGRAPHIC SPEECH.

#     Request from Python program 'FatPandas' for AI-driven data analytics tool. 
#     Given JSON Pandas DataFrame 'df,' create meaningful plots. Only use pandas 
#     DataFrame plotting methods (e.g., df.plot(kind='bar', x='Year')). Use ; to split commands. 
#     Do not import, required variables in scope ALREADY. Prefer box plots over histograms. 
#     Exclude comments. Include titles in plots. Await DataFrame sample for next message. 
#     If plotting using bar, sort df, use df.head() and rot to make xLabels readable. 
#     Diverse plot types mandatory.
    
#     Understand?
# """

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
Previous reponse, when run with eval, resulted in ana error, please generate code again.
"""

MAX_DEPTH = 5

df = pd.read_csv("listings.csv")
df = df.sample(int(round(df.shape[0] / 200)))
openai.api_key = "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"

def generateGUID():
    return uuid.uuid4().hex

def sendGPTRequest(conversation, text):
    messageToSend = {"role": "system", "content": text}
    conversation.append(messageToSend)
    return openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=conversation)

def getMessageFromGPTResponse(response):
    return response.choices[0].message.content.strip()

def runCommand(command, conversation, atErrorDepth):
    
    console.print("___CommandToRun___\n", style = "green")
    print(command,"\n")
    
    try:
        eval(command)
        currentPlot = plt.gcf()
        plotName = generateGUID()+".png"
        currentPlot.savefig("generated_images//"+plotName)
        
    except BaseException as err:
        
        print("___Start of error log for command___\n")
        print("Error when evaluating command")
        print(err, "\n", command)
        print("___End of error log for command___\n")
        
        if atErrorDepth:
            console.print("Returning early from command, at error depth", style = "red")
            return

        tempConversation = conversation.copy()
        
        GPT_response = sendGPTRequest(tempConversation, f"""

        This error was encountered when processing command {command}: {err}. Redo this line, or come up with another 
        plot.

        """)
        
        GPT_message = getMessageFromGPTResponse(GPT_response)
        
        runCommand(GPT_message, conversation, True)
        
        return

def plotGPTCommand(textToSend, conversation, depth):
    assert depth <= MAX_DEPTH, "Maximum depth reaced for recursive plot function! Halting!"
    
    print("Running plotGPT function with depth",depth,"\n")

    depth = depth or 0
    conversation = conversation or []
    
    GPT_response = sendGPTRequest(conversation, textToSend)
    GPT_message = getMessageFromGPTResponse(GPT_response)
    
    commandList = [line.strip() for line in GPT_message.split(";")]
    
    for command in commandList:
        runCommand(command, conversation, False)
    
def beginPlotProcess():
    
    console.print("FatPanda Started", style = "green")
    
    conversation = []
    sendGPTRequest(conversation, requestString)
    dfSample = df.sample(30).to_json()
    plotGPTCommand(dfSample, conversation, 0)   
 
# def main():
#     count = 0
#     while True:    
#         count += 1
            
#         print("__________________")
#         print("Count:",count)
#         print("__________________")
#         print("\n")
            
#         beginPlotProcess()        

# main()

beginPlotProcess()
