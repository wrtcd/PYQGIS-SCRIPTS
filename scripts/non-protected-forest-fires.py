import glob, pathlib
from pathlib import Path
import processing

directory = Path.home().joinpath('Desktop', 'forestfires')
fires = glob.glob(str(directory.joinpath('yearly-fires-sampled'))+"./*shp")

directory.joinpath('yearly-forest-fires').mkdir(parents=True, exist_ok=True)

for fire in fires:
    
    layer = QgsVectorLayer(fire, '', 'ogr')

    layer.selectByExpression("\"SAMPLED1\">= 1")
    
    destination = str(directory.joinpath('yearly-forest-fires')) + "\\" + Path(fire).stem.replace('fires_sampled', 'forest_fires') + ".shp"
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)         

