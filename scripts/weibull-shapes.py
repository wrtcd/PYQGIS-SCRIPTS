import glob, pathlib
from pathlib import Path
import os

# global country directory
region = "SEA"
country = "vietnam"
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','FIRES', region, country, 'Yearly Grids')

Path(directory.joinpath('Weibull Shapes')).mkdir(parents=True, exist_ok=True)
source = str(directory.joinpath('Weibull'))
files = glob.glob(source + "/*.csv")

for file in files:
    
    fullname = file.replace('\\', '/')
    
    uri = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s' % (fullname, 'EPSG:4326', ',', 'X_COORD', 'Y_COORD', ',')
    layer = QgsVectorLayer(uri, '', 'delimitedtext')
    destination = str(directory.joinpath('Weibull Shapes')) + "\\" + Path(file).stem.replace('weibull', 'weibull_shp') + ".shp"
    
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    
    QgsVectorFileWriter.writeAsVectorFormatV2(layer, destination, QgsCoordinateTransformContext(), options)
    
    
