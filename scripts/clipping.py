import glob, pathlib
from pathlib import Path
import processing

directory = Path(r"D:\WORK February 2023\monthlydroughtindices\{}\{} Monthly Fires".format(year, year))
fires = glob.glob(str(directory)+"/*.shp")

countriespath = r"D:\WORK March 2023\monthly fire persistence\countries\myanmar_shape.shp"
country = QgsVectorLayer(countriespath, '', 'ogr')

for f in fires:
    
    fire = QgsVectorLayer(f,'','ogr')
    fire.dataProvider().createSpatialIndex()
    firename = Path(f).stem
    
    destination = r"D:\WORK June 2023\univariate\myanmar\myanmar-monthly-fire-subsets\myanmar_{}.shp".format(firename)
            
    parameters = {'INPUT': fire, 
                  'OVERLAY': country, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
                  
    clipped = processing.run("native:clip", parameters)
    
    clippedlayer = clipped['OUTPUT']
                  
    processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': destination})
        