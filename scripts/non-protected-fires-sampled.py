import glob, pathlib
from pathlib import Path
import processing

rasterpath = r"C:\Users\aeaturu\Desktop\January 2022\protected-areas-project\landcover product\LC_peninsular_non_protected_forest_areas.tif"
forestareas = QgsRasterLayer(rasterpath, '')

directory = Path.home().joinpath('Desktop', 'forestfires')
fires = glob.glob(str(directory)+"./*shp")

directory.joinpath('yearly-fires-sampled').mkdir(parents=True, exist_ok=True)

for fire in fires:

    destination = str(directory.joinpath('yearly-fires-sampled')) + "\\" + Path(fire).stem.replace('fires', 'fires_sampled') + ".shp"
        
    parameters = {'INPUT': fire, 
                  'RASTERCOPY': forestareas, 
                  'COLUMN_PREFIX': 'SAMPLED',
                  'OUTPUT': destination}

    processing.run("qgis:rastersampling", parameters)         

