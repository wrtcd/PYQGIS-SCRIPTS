import pathlib, glob
from pathlib import Path
import pandas as pd
import numpy as np

directory = pathlib.Path.home().joinpath('Desktop', 'January 2022', 'FIRES')
region = 'SA'
country = 'india'

weibullsource = directory.joinpath(region, country, 'Yearly Grids', 'Weibull')
weibull = glob.glob(str(weibullsource)+'./*.csv')
files = []

for file in weibull:
    
    year = Path(file).stem[-4:]
    
    if year in ['2012', '2019']:
        files.append(file)

probs = [0.70]

for file in files:

    df = pd.read_csv(file)

    for p in probs:
        
        new_df = df[df.Weibull >= p]
        
        destination = str(directory.joinpath('testgrids')) + "\\" + Path(file).stem + "_{}.csv".format(p) 
        
        new_df.to_csv(destination, encoding='utf-8', index=False)