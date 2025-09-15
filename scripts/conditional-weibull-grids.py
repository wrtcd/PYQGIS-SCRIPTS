import glob, pathlib
from pathlib import Path
import os

# global country directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022', 'FIRES', 'testgrids')

source = str(directory)
files = glob.glob(source + "/*.shp")

uri = r"C:\Users\aeaturu\Desktop\January 2022\FIRES\SA\india\india_grid.shp"
countrygrid = QgsVectorLayer(uri, '', 'ogr')

for file in files:
    
    shape = QgsVectorLayer(file, '', 'ogr')
    shape.dataProvider().createSpatialIndex()
    
    destination = str(directory) + "\\" + Path(file).stem.replace('weibull_shp', 'weibull_grid') + ".shp"
    
    parameters = {'INPUT': countrygrid,
                  'JOIN': shape,
                  'JOIN_FIELDS': 'Weibull',
                  'OUTPUT': destination}
    
    processing.run("native:joinattributesbylocation", parameters)
    
    
