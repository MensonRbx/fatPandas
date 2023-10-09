import openai
import logging

import pandas as pd

from modules.GPTFunctions import beginAIPlotProcess
from modules.PlotScraper import PlotScrape

MAX_ERROR_DEPTH = 5
MODEL_NAME = "gpt-3.5-turbo-16k"
VERTICAL_BOX_PLOTS = False
MAX_BAR_PLOT_X_AXIS_LABEL_LENGTH = 5
COLUMN_NAME_BLACKLIST = set([
    "id",
    "date",
    "agency_ids",
])
SAVE_PLOTS = False

df = pd.read_csv("datasets/fatal-police-shootings-data.csv")
dfname = "Fatal Police Shootings in America"
openai.api_key = "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"
recursion_count = 0

df = df.sample(2000)

requestString = """
Request from Python prog 'Pandas++.' Data tool, uses AI for meaningful data plots. 
Send sample Pandas DF in .json, look for plot data. Use Pandas DF plot methods (e.g., df.plot(kind='Bar', x='Year')). 
Response: JSON dict of dicts, each with plot args.
EXAMPLE:
{
     "p1": {
        "kind": "bar",
        "x": "Year",
        "xlabel": "Years"
        },
}
No comments. Meaningful Plots. Prefer Box Plots/Scatter Plots to Histograms. 
Include titles in plot kwargs to describe the plot (add "AI" at the end of title). 
Aim for 10+ subDicts. No unclosed brackets/errors. Understand the task?
"""
                    
#END OF NON-AI FUNCTIONS

def main():
    logging.basicConfig(level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%m:%S"
    )
    logging.info("\nStarting Plot Scrapper\n")
    PlotScrape(df, dfname, False)
    logging.info("\nStarting AI Plots\n")
    beginAIPlotProcess(df, requestString, MODEL_NAME)
    logging.info("Execution Completed!\n")
 
if __name__ == "__main__":
    main()
