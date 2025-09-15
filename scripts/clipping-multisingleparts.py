import glob, pathlib
from pathlib import Path
import processing

directory = Path(r"D:\WORK September 2022\hvm-fc-frp\viirs")

firepath = r"D:\WORK September 2022\seag\data\countries\myanmar_shape.shp"
fire = QgsVectorLayer(firepath,'','ogr')

countriespath = r"D:\WORK September 2022\seag\data\countries"
countries = glob.glob(countriespath+"/*.shp")

for c in countries:
    
    country = QgsVectorLayer(c,'','ogr')
    countryname = Path(c).stem.split('_')[0]
    # filename = Path(country).stem[:-6]
    
    
    destination = str(directory.joinpath("{}_viirs_2021.shp".format(countryname)))
            
    parameters = {'INPUT': fire, 
                  'OVERLAY': country, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}

    # run the clip tool
    clipped = processing.run("native:clip", parameters)        
    
    clippedlayer = clipped['OUTPUT']
    
    processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': destination})



        