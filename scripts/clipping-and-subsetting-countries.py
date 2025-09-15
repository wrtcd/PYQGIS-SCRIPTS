import glob, pathlib
from pathlib import Path
import processing

gridpath = r"C:\Users\aeaturu\Desktop\WORK April 2025\aayushi - data download\fire_archive_SV-C2_599159.shp"
grid = QgsVectorLayer(gridpath, '', 'ogr')

countriespath = r"C:\Users\aeaturu\Desktop\WORK April 2025\aayushi - data download\shapefiles2"
countries = glob.glob(countriespath+"/*.shp")

for c in countries:
    
    name = Path(c).stem.split('_')[0]
    
    destination = r"C:\Users\aeaturu\Desktop\WORK April 2025\aayushi - data download\clipped2\{}_2024.shp".format(name)
            
    parameters = {'INPUT': grid, 
                  'OVERLAY': c, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}

    # run the clip tool
    clipped = processing.run("native:clip", parameters)        
    # processing.run("native:clip", parameters)
    
    clippedlayer = clipped['OUTPUT']
    
    # points.selectByExpression("\"DAYNIGHT\"= 'D'")

    writer = QgsVectorFileWriter.writeAsVectorFormat(clippedlayer, destination, 'utf-8', driverName='ESRI Shapefile')
    del(writer)


