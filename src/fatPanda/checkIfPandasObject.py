import pandas as pd

def check(pandasObject):
        
    if isinstance(pandasObject, pd.DataFrame):
        return "DataFrame"
    elif isinstance(pandasObject, pd.Series):
        return "Series"
    else:
        raise ValueError