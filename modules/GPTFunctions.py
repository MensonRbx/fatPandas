import logging
import openai
import uuid
import json

import matplotlib.pyplot as plt

from json import JSONDecodeError

def generateGUID():
    return uuid.uuid4().hex

def deepCopyArray(arr):
    newArray = []
    for item in arr:
        newArray.append(item)
    return newArray


#START OF AI FUNCTIONS
def sendGPTRequest(conversation, text, modelName):
    modelName = modelName or "gpt-3.5"
    messageToSend = {"role": "system", "content": text}
    conversation.append(messageToSend)
    return openai.ChatCompletion.create(model=modelName, messages=conversation)

def getMessageFromGPTResponse(response):
    return response.choices[0].message.content.strip()

def runCommand(df, kwargDict, conversation, atErrorDepth, savePlots, modelName):
    
    try:
        plt.figure()
        df.plot(**kwargDict)
        
        if savePlots:
            currentPlot = plt.gcf()
            plotName = generateGUID()+".png"
            currentPlot.savefig("generated_images//"+plotName)
        
    except Exception as err:
        plt.figure()
        logging.warning(f"Plot function failed for dict {kwargDict}\n")
        logging.warning(f"Error When Plotting: {err}\n")
        
        if atErrorDepth:
            return
        
        newConvo = deepCopyArray(conversation)
        
        messageToSend = f"""
            The error {err} was encountered when processing 
            command list {kwargDict}. Please adjust commands.
        """
        
        GPT_response = sendGPTRequest(newConvo, messageToSend, modelName)
        GPT_message = getMessageFromGPTResponse(GPT_response)
        newKwargDict = json.loads(GPT_message)
        runCommand(df, newKwargDict, conversation, True, False, modelName)

def plotGPTCommand(textToSend, conversation, depth, modelName, df):
    
    
    logging.debug(f"Current plot func depth: {depth}")
    
    depth = depth or 0
    conversation = conversation or []
    
    logging.debug("Sending request to GPT...")
    GPT_response = sendGPTRequest(conversation, textToSend, modelName)
    GPT_message = getMessageFromGPTResponse(GPT_response)
    logging.debug("Received GPT Response")
    
    dictMap = None
    try:
        dictMap  = json.loads(GPT_message)    
        for key, kwargDict in dictMap.items():
            logging.debug(key)
            logging.debug(f"kwargDict: {str(kwargDict)}\n")
            runCommand(df, kwargDict, conversation, False, False, modelName)
    except JSONDecodeError as err:
        errorLogToSend = f"""
            Error when decoding dictionary {dictMap}: {err}
        """
        plotGPTCommand(errorLogToSend , conversation, depth + 1, modelName, df)
        
        
    """
    Commented out part is for concurrent execution, not needed currently but keeping in case needed.
    """
   
    # with concurrent.futures.ThreadPoolExecutor(max_workers=len(dictList)) as executor:
    #     logging.debug("Starting Thread Pool Executor")
    #     for _, kwargDict in dictList.items():
    #         logging.debug(f"kwargDict: {str(kwargDict)}")
    #         executor.submit(runCommand, kwargDict, conversation, False)
    
    
def beginAIPlotProcess(df, requestString, modelName):
    
    print(df, requestString, modelName)
    
    logging.info("Pandas++ Starting")
    
    conversation = []
    sendGPTRequest(conversation, requestString, modelName)
    dfSample = df.sample(30).to_json() + "\n\n" + str(df.dtypes)
    
    logging.info("Initial prompt finished. Starting plotting function")
    
    plotGPTCommand(dfSample, conversation, 0, modelName, df)   