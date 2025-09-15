import glob, pathlib
from pathlib import Path
import processing

firepath = r"D:\WORK JUNE 2024\fire forecasting\viirs_fire_data_from_2023_2024_May\merged.shp"
fire = QgsVectorLayer(firepath, '', 'ogr')
fire.dataProvider().createSpatialIndex()

directory = 'sea'
countriespath = r"D:\WORK JUNE 2024\fire forecasting\countries shapefile\{}".format(directory)
countries = glob.glob(countriespath+"/*.shp")

for c in countries:
    
    country = QgsVectorLayer(c,'','ogr')
    countryname = Path(c).stem.split('_')[0]
    
    destination = r"D:\WORK JUNE 2024\fire forecasting\viirs_fire_data_from_2023_2024_May\{}\{}_20230101to20240625.shp".format(directory, countryname)
            
    parameters = {'INPUT': fire, 
                  'OVERLAY': country, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
                  
    
    
    # run the clip tool
    clipped = processing.run("native:clip", parameters)        
    # processing.run("native:clip", parameters)
    
    clippedlayer = clipped['OUTPUT']
    
    processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': destination})