import glob
import processing
from pathlib import Path

files = glob.glob(r"D:\WORK 2025 January\adityaeaturu - forestpopulationcover\gwr_input_files" + "/*.shp")
emptyfiles = []

for f in files:
    
    layer = QgsVectorLayer(f, '', 'ogr')
    fc = layer.featureCount()
    
    if (fc == 0):
        
        emptyfiles.append(f)
        