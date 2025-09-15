import glob, pathlib
from pathlib import Path
import processing

direc = r"D:\WORK March 2023\daily fire persistence maps\countries-10m"
fires = glob.glob(str(direc)+"/*shp")

for fire in fires:
    
    layer = QgsVectorLayer(fire, '', 'ogr')
    
    layer.dataProvider().createSpatialIndex()