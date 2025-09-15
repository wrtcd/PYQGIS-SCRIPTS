import pandas as pd

file = r"C:\Users\aeaturu\Documents\for-testing\counts-csv-test.csv"

data = pd.read_csv(file)

data["Rank (Dense)"] = data["Count"].rank(ascending = False, method='dense')
data.sort_values("Count", ascending = False, inplace = True)

print(data)
