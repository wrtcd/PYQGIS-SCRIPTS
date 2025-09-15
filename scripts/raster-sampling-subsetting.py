import glob, pathlib
from pathlib import Path
import processing

directory = Path(r"D:\WORK September 2022\seag\data\modisag")
fires = glob.glob(str(directory)+"./*shp")

for fire in fires:
    
    layer = QgsVectorLayer(fire, '', 'ogr')

    layer.selectByExpression("\"SAMPLED1\">= 1")
    
    filename = Path(fire).stem
    names = filename.split("_")
    finalname = names[0] + "ag_" + names[3]
    
    destination = r"D:\WORK September 2022\seag\data\viirsag" + "\\" + finalname + ".shp"
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)         

