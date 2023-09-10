import openai
import json

import pandas as pd
import matplotlib.pyplot as plt

requestString = """

Hello! This is a request from a Python program called "FatPandas". 
It is a data analytics tool that uses AI (you!) in order to come up with potentially meaningful plots of data. 
To do so, you will be sent a sample of a Pandas Dataframe in .json format, which you will look at and look for 
data to plot. Look for any sort of data that could be plotted using all of the plotting methods build into
pandas DataFrames (i.e. df.plot(kind = "Bar", x = "Year")).

Your response must be multiple lines of code, each line plotting a unique plot using methods built into python
dataframes. Split each line using a semicolon (;).

Include no comments so that I can clearly look at the pure code to debug.

Do not create the dataframe, as it is already created and is called df. Refer it it as df in your code too.
    
Make sure to include labels and titles that accurately describe what the plot is.

Note: your response will be run using the built-in eval function in python. Please do not include any characters
that would cause the code to fail!

LEAVE NO INCOMPLETE LINES!
    
Try and find as many plots as possible, do you understand the task?

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


MAX_DEPTH = 5

df = pd.read_csv("listings.csv")
openai.api_key = "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"

currentConversation = []


def sendGPTRequest(text):
    messageToSend = {"role": "system", "content": text}
    currentConversation.append(messageToSend)
    return openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=currentConversation)

def getMessageFromGPTResponse(response):
    return response.choices[0].message.content.strip()

def plotGPTCommand(textToSend, depth):
    assert depth <= MAX_DEPTH, "Maximum depth reaced for recursive plot function! Halting!"
    
    print("Running plotGPT function with depth",depth)
    
    depth = depth or 0
    
    GPT_response = sendGPTRequest(textToSend)
    GPT_message = getMessageFromGPTResponse(GPT_response)
    
    command_list: list = [line.strip() for line in GPT_message.split(";")]
    
    print(len(command_list))
    
    for index, command in enumerate(command_list):
        
        try:
            eval(command)
            currentPlot = plt.gcf()
            
            plotName = "plot"+index+".png"
            
            currentPlot.savefig("generated_images//"+plotName)
            
        except BaseException as err:
            print("___Start of error log for command___\n")
            print("Error when evaluating command",index)
            print(err, "\n\n", command)
            print("___End of error log for command___\n")
    
    print("Finished execution!")
    
    # try:
    #     eval(GPT_message)
    # except BaseException as err:
        
    #     print(err)
        
    #     import_in_response = GPT_message.find("import")
    #     print(import_in_response)
    #     if import_in_response != -1:
    #         print("Error in eval run of code: import statement found!\n")
    #         plotGPTCommand(importErrorString, depth + 1)
    #     else:
    #         print("Syntax Error in eval run of code, retrying... \n")
    #         plotGPTCommand(syntaxErrorString, depth + 1)
    
def main():
    dfSample = df.sample(30)
    print("Sending primer prompt to GPT...\n")
    sendGPTRequest(requestString)
    print("Primer prompt finished, beinging recursive plot function call\n")
    plotGPTCommand(dfSample.to_json(), 0)
    
main()

   
            
