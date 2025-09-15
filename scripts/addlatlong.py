import glob, pathlib
from pathlib import Path
import processing

dir = r"E:\WORK 2024 JULY\my paper - ccdc\zones\all zone test points"
files = glob.glob(dir + "\*.shp")

for file in files:
    
    layer = QgsVectorLayer(file, '','ogr')
    filename = Path(file).stem + '_with_lat_long'
    
    destination = r"E:\WORK 2024 JULY\my paper - ccdc\zones\all zone test points with lat lon" + "\\" +filename + ".shp"

    parameters = {
                'INPUT': layer,
                'CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
                'OUTPUT': destination
                                                }
    processing.run("native:addxyfields", parameters)