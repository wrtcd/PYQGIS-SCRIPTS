import glob, pathlib
from pathlib import Path
import processing

hourlypath = r"D:\WORK March 2023\monthly fire persistence\merged"
countrypath = r"D:\WORK March 2023\monthly fire persistence\countries"

hourly = glob.glob(str(hourlypath)+"/*shp")
countries = glob.glob(str(countrypath)+"/*shp")

hourly.sort()
countries.sort()

pairs = [[hourly[i], countries[i]] for i in range(9)]

for p in pairs:
    
    destination = str(Path(r"D:\WORK March 2023\monthly fire persistence\mergedclipped").joinpath("{}_clipped.shp".format(Path(p[0]).stem.split('_')[0])))
            
    parameters = {'INPUT': p[0], 
                  'OVERLAY': p[1], 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
     
    clipped = processing.run("native:clip", parameters)
    
    clippedlayer = clipped['OUTPUT']
    
    processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': destination})


        