import pandas as pd
import glob, pathlib
from pathlib import Path

directory = pathlib.Path.home().joinpath('Desktop', 'yearly-forest-fires', 'yearly-forest-fires', 'Protected Monthly Fire Counts CSV')
files = glob.glob(str(directory) + './*csv')
fires = []

for file in files:
    
    year = file[-23:-19]
    
    if year in ['2019', '2021']:
    
        data = pd.read_csv(file)
        fires.append(data['Fires'])
    
df = pd.DataFrame(fires)
output = r"C:\Users\aeaturu\Desktop\yearly-forest-fires\yearly-forest-fires\nonprotectedforestfires.csv"
df.to_csv(output, index=False, header=None)