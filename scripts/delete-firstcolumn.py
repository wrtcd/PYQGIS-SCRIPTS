import glob, pathlib
from pathlib import Path
import processing
import pandas as pd

country = 'cambodia'

filepath = r"D:\WORK March 2023\monthly fire persistence\{}".format(country)
files = glob.glob(filepath+ '/*.csv')

for file in files:
    
    data = pd.read_csv(file, usecols = ['#year', 'month', 'day', 'lat', 'lon', 'ave(frp)', 'max(frp)', 'N'])
    data.to_csv(file, index=False)