import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = Path(r"D:\WORK September 2022\fire-persistence\country-hourly-csv")
fires = glob.glob(str(directory) + '/*.csv')

for fire in fires:
    
    uri = 'file:///{}?delimiter=,&yField=lat&xField=lon'.format(fire)
    output = r"D:\WORK September 2022\fire-persistence\country-hourly-shp\{}.shp".format(Path(fire).stem)
    
    layer = QgsVectorLayer(uri, '', 'delimitedtext')
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"

    QgsVectorFileWriter.writeAsVectorFormatV2(layer, output, QgsCoordinateTransformContext(), options)
    

