import glob, pathlib
from pathlib import Path
import processing

directory = Path(r"D:\WORK August 2022\himawari\himawari-sea-ag\z-daily-updated-shp")
fires  = glob.glob(str(directory)+"\\"+'/*.shp')

c = 'philippines'

countriespath = r"D:\WORK September 2022\seag\data\countries\{}_shape.shp".format(c)
country = QgsVectorLayer(countriespath,'','ogr')

for f in fires:
    
    fire = QgsVectorLayer(f, '', 'ogr')
    date = Path(f).stem.split('_')[1]
    countryname = Path(countriespath).stem.split('_')[0]
    
    destination = str(Path(r"D:\WORK September 2022\fire-persistence\himawari-daily\{}".format(c)).joinpath("{}_{}.shp".format(countryname, date)))
            
    parameters = {'INPUT': fire, 
                  'OVERLAY': country, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
     
    clipped = processing.run("native:clip", parameters)
    
    clippedlayer = clipped['OUTPUT']
    
    processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': destination})


        