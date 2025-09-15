import os, fnmatch
import pathlib
from pathlib import Path
import pandas as pd

years = [*range(2012, 2022)]
years = [str(year) for year in years]

suffixes = []

for year in years:
    
    suffixes.append('weibull_{}.csv'.format(year))

def findFiles(folder):
    
    matches = []
    
    for root, dirnames, filenames in os.walk(folder):
        for file in suffixes:
            for filename in fnmatch.filter(filenames, '*' + file):
                matches.append(os.path.join(root, filename))
    return matches
    
directory = r"C:\Users\aeaturu\Desktop\January 2022\FIRES"
grids = findFiles(directory)
                  
countries = []
totobs = []

maxrank = []

for grid in grids:
    
    year = grid[-8:-4:]
    
    country = Path(grid).stem[:len(Path(grid).stem)-13]
    countries.append(country)
    
    data = pd.read_csv(grid)
    
    ranker = 'maxrank'+str(year)
    ranker = []
    ranker.append(data['Rank (Dense)'].max())
    maxrank.append(ranker)
    totobs.append(len(data))
    
countries = [country.title() for country in countries]    
    
new_data = pd.DataFrame()

new_data['Country'] = countries
new_data['Max Rank (' + str(year) + ')'] = maxrank
new_data['Total Observations'] = totobs

new_data['Max Prob'] = (new_data['Max Rank (' + str(year) + ')']/(new_data['Total Observations']+1))*100

new_data.sort_values('Total Observations', axis=0 , ascending=False)              