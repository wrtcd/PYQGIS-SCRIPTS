import glob, pathlib
from pathlib import Path
import os

# csv directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','FIRES')

files = glob.glob(str(directory) + '/*weibull.csv')
file = files[0]
    
fullname = file.replace('\\', '/')

uri = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s' % (fullname, 'EPSG:4326', ',', 'X_COORD', 'Y_COORD', ',')
layer = QgsVectorLayer(uri, '', 'delimitedtext')
destination = str(directory) + "\\" + Path(file).stem.replace('weibull', 'weibull_shp') + ".shp"

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"

QgsVectorFileWriter.writeAsVectorFormatV2(layer, destination, QgsCoordinateTransformContext(), options)
    
    
