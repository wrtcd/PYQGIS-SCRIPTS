import glob, pathlib
from pathlib import Path
import processing

countriespath = r"D:\WORK March 2023\daily fire persistence maps\countries"
countries = glob.glob(countriespath + "/*.shp")

gridpath = r"D:\WORK March 2023\daily fire persistence maps\hc_grid10m.shp"
grid = QgsVectorLayer(gridpath, '', 'ogr')

for c in countries:
    
    clipped = r"D:\WORK March 2023\daily fire persistence maps\countries-10m" + "\\" + Path(c).stem.split('_')[0] + "_10m.shp"
        
    parameters = {'INPUT': grid, 
                  'OVERLAY': c, 
                  'OUTPUT': clipped}

    # run the clip tool
    processing.run("native:clip", parameters)
    
    
    
    