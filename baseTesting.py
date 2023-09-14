import pandas as pd

df = pd.read_csv("WHR_2023.csv")
df.sort_values(by = "gdp_per_capita", ascending = False, inplace = True)

newDf = pd.Series(index = df["country"], data = df["gdp_per_capita"].values)

newDf.head().plot(kind = "bar", x = "country", y = "gdp_per_capita")

print(newDf["Ireland"])

# newDf.tail(10).plot(kind = "bar", x = "country", y = "generosity")
