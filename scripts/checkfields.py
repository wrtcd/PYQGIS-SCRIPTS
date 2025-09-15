import glob
import processing
from pathlib import Path

files = glob.glob(r"D:\WORK 2025 January\adityaeaturu - forestpopulationcover\gwr_input_files" + "/*.shp")

for f in files:
    
    layer = QgsVectorLayer(f, '', 'ogr')
    fieldnames = [f.name() for f in layer.fields()]
    print(fieldnames)