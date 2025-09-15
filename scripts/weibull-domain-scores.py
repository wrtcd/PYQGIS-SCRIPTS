import glob, pathlib
from pathlib import Path
import pandas as pd

# csv directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','FIRES')

files = glob.glob(str(directory) + '/*.csv')
file = files[0]

   
data = pd.read_csv(file)
data["Rank"] = data["Fires"].rank(ascending = False)
data.sort_values("Fires", ascending = False, inplace = True)

n = len(data) - 1

def weibull(r):
    return (r/(n+1))*100

data["Weibull"] = data["Rank"].apply(weibull)

destination = str(directory) + "\\" + Path(file).stem.replace('merged_refactored_csv', 'weibull') + ".csv"

data.to_csv(destination, encoding='utf-8', index=False)
    
    
    
    
