import pathlib
from pathlib import Path
import processing
import os, fnmatch

directory = r"C:\Users\aeaturu\Desktop\January 2022\FIRES\SEA"
years = [*range(2012, 2022, 1)]
exclude = ['brunei', 'indonesia', 'malaysia', 'phillipines', 'singapore', 'timorleste']

def findfires(folder):
    
    matches = []
    
    for root, dirnames, filenames in os.walk(folder):
        dirnames[:] = [dn for dn in dirnames if dn not in exclude]
        for file in suffix:
            for filename in fnmatch.filter(filenames, '*' + file):
                matches.append(os.path.join(root, filename))
    
    return matches
    
for year in years:
    
    suffix = ['fires_' + str(year) + '.shp']

    peninsularfires = findfires(directory)
    print(*peninsularfires, sep='\n')
    print(len(peninsularfires))

    destination = r"C:\Users\aeaturu\Desktop\January 2022\protected-areas-project\yearly-fires"
        
    parameters = {'LAYERS': peninsularfires, 
                  'CRS': 'EPSG:4326', 
                  'OUTPUT': destination + "\\" + 'peninsular_fires_{}.shp'.format(year)}

    processing.run("qgis:mergevectorlayers", parameters)         