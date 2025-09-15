import glob, pathlib
from pathlib import Path
import processing

rasterpath = r"C:\Users\aeaturu\Desktop\lc"
rasters = glob.glob(str(rasterpath)+"./*tif")

firepath = r"D:\WORK May 2023\interns\Aayushi\DBSCAN\mmr_2021_030405.shp"
fire = QgsVectorLayer(firepath, '', 'ogr')

for raster in rasters:

    destination = r"C:\Users\aeaturu\Desktop\sampledlc" + "\\" + Path(raster).stem + ".shp"
        
    parameters = {'INPUT': fire, 
                  'RASTERCOPY': raster, 
                  'COLUMN_PREFIX': 'SAMPLED',
                  'OUTPUT': destination}

    processing.run("qgis:rastersampling", parameters)         

