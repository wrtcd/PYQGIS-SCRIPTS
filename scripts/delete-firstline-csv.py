import glob, pathlib
from pathlib import Path
import processing
import pandas as pd

country = 'vietnam'

filepath = r"D:\WORK March 2023\monthly fire persistence\{}".format(country)
files = glob.glob(filepath+ '/*.csv')

for file in files:
    
    data = pd.read_csv(file, skiprows = 1)
    data.to_csv(file)