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
Prefer Box Plots to Histograms. 
Include titles in plot kwargs. 
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

df = pd.read_csv("datasets/listings.csv")
df = df.sample(1000)
openai.api_key = "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"

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
        
    except JSONDecodeError:
        plt.figure()
        logging.warning(f"plot function failed for dict {kwargDict}")
        
        """
        TODO:
            
        """
        
        # if atErrorDepth:
        #     console.print("Returning early from command, at error depth", style = "red")
        #     return

        # tempConversation = conversation.copy()
        
        # GPT_response = sendGPTRequest(tempConversation, f"""

        # This error was encountered when processing command {command}: {err}. Redo this line, or come up with another 
        # plot.

        # """)
        
        # GPT_message = getMessageFromGPTResponse(GPT_response)
        
        # runCommand(GPT_message, conversation, True)
        
        # return

def plotGPTCommand(textToSend, conversation, depth):
    assert depth <= MAX_DEPTH, "Maximum depth reaced for recursive plot function! Halting!"
    
    logging.debug(f"Current plot func depth: {depth }")
    
    depth = depth or 0
    conversation = conversation or []
    
    GPT_response = sendGPTRequest(conversation, textToSend)
    GPT_message = getMessageFromGPTResponse(GPT_response)
    
    logging.debug(GPT_message)
    
    dictList = json.loads(GPT_message)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(dictList)) as executor:
        for _, kwargDict in dictList.items():
            logging.info(f"kwargDict: {str(kwargDict)}")
            executor.submit(runCommand, kwargDict, conversation, False)
    
def beginPlotProcess():
    
    logging.info("Pandas++ Starting")
    
    conversation = []
    sendGPTRequest(conversation, requestString)
    dfSample = df.sample(30).to_json() + "\n\n" + str(df.dtypes)
    
    logging.info("Initial prompt finished. Starting plotting function")
    
    plotGPTCommand(dfSample, conversation, 0)   

def main():
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%m:%S",
        # filename="log.log"
    )
    
    logging.info("\nPandas++ Starting from main!")
    
    beginPlotProcess()
    
    logging.info("Execution Completed!\n")
    
 
if __name__ == "__main__":
    main()
