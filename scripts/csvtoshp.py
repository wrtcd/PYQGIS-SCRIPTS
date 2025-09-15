import glob, pathlib
from pathlib import Path
import processing

filepath = r"D:\WORK December 2023\indonesia fire stuff\himawari\daily datasets\daily"
files = glob.glob(filepath+ '/*.csv')

for file in files:
    
    uri = 'file:///{}?crs={}&delimiter={}&xField={}&yField={}'.format(file, 'EPSG:4326', ',', 'lon', 'lat')
    layer = QgsVectorLayer(uri, "", "delimitedtext")
    
    fn = r"D:\WORK December 2023\indonesia fire stuff\himawari\daily datasets\daily\himawari-global-yearly-shape" + "\\" + Path(file).stem+ ".shp"
    
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile')
    del(writer)