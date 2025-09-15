import glob, pathlib
from pathlib import Path
import processing

directory = Path.home().joinpath('Desktop', 'clip')
fires = glob.glob(str(directory)+"./*shp")

clippath = r"C:\Users\aeaturu\Desktop\January 2022\protected-areas-project\shapes\protected_areas.shp"
cliplayer = QgsVectorLayer(clippath, '', 'ogr')

directory.joinpath('yearly-protected-fires').mkdir(parents=True, exist_ok=True)

for fire in fires:
    
    clipped = str(directory.joinpath('yearly-protected-fires')) + "\\" + Path(fire).stem.replace('peninsular', 'protected') + ".shp"
    
    layer = QgsVectorLayer(fire, '', 'ogr')
    
    parameters = {'INPUT': layer, 
                  'OVERLAY': cliplayer, 
                  'OUTPUT': clipped}

    # run the clip tool
    processing.run("native:clip", parameters)
    
    
    
    