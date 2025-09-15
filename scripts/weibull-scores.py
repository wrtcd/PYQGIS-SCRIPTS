import glob, pathlib
from pathlib import Path
import pandas as pd

path = r"D:\WORK February 2022\FIRES"

region = "SA"
country = "afghanistan"
directory = Path(path).joinpath(region, country, 'Yearly Grids')

csvsource = directory.joinpath('CSV')
files = glob.glob(str(csvsource) + '/*.csv')

for file in files:
    
    data = pd.read_csv(file)
    data["Rank (Dense)"] = data["Fires"].rank(ascending = False, method='dense')
    data.sort_values("Fires", ascending = False, inplace = True)
    
    n = len(data)
    
    def weibull(r):
        return (r/(n+1))*100
    
    data["Weibull"] = data["Rank (Dense)"].apply(weibull)
    
    Path(directory.joinpath('Weibull')).mkdir(parents=True, exist_ok=True)
    destination = str(directory.joinpath('Weibull')) + "\\" + Path(file).stem.replace('grid', 'weibull') + ".csv"
    
    data.to_csv(destination, encoding='utf-8', index=False)
    
    
    
    
