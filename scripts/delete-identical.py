import glob, pathlib
from pathlib import Path
import processing

directory = Path.home().joinpath('Desktop', 'January 2022', 'protected-areas-project')
clippedfires = glob.glob(str(directory.joinpath('yearly-forest-fires-clipped'))+"./*shp")
forestfires = glob.glob(str(directory.joinpath('yearly-forest-fires'))+"./*shp")

list = [*(range(0, 10))]

for l in list:
    
    clipped = clippedfires[l]
    forest = forestfires[l]
    
    clippedlayer = QgsVectorLayer(clipped, '', 'ogr')
    forestlayer = QgsVectorLayer(forest, '', 'ogr')
    
    