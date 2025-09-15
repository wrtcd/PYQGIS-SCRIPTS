import glob
import processing
from pathlib import Path

files = []
folderpath = r"E:\WORK December 2023\indonesia fire stuff"

for path in Path(folderpath).rglob('*.shp'):
    files.append(str(path))

invalidpaths = []

for f in files:
    
    layer = QgsVectorLayer(f, '', 'ogr')
    
    if not layer.isValid():
        invalidpaths.append(f)
