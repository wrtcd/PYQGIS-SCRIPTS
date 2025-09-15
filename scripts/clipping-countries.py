import glob, pathlib
from pathlib import Path
import processing

gridpath = r"C:\Users\aeaturu\Desktop\WORK May 2025\gridded fires\grid"
grid  = QgsVectorLayer(gridpath, '', 'ogr')

countriespath = r"C:\Users\aeaturu\Desktop\WORK May 2025\gridded fires\shapefiles - gridded fires"
countries = glob.glob(countriespath+"/*.shp")

for c in countries:
    
    country = QgsVectorLayer(c,'','ogr')
    countryname = Path(c).stem.split('_')[0]
    
    destination = r"C:\Users\aeaturu\Desktop\WORK May 2025\gridded fires\countriesclipped" + "\\" + "{}_grid.shp".format(countryname)
            
    parameters = {'INPUT': grid, 
                  'OVERLAY': country, 
                  'OUTPUT': destination}

    # run the clip tool
    clipped = processing.run("native:clip", parameters)        
    # processing.run("native:clip", parameters)
    
    
