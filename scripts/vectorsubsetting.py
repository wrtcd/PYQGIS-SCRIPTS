import glob, pathlib
from pathlib import Path
import processing

firespath = r"D:\WORK June 2023\all fires 2012 2022"
fires = glob.glob(firespath+ '/*.shp')

for f in fires:
    
    name = Path(f).stem + '_N'
    
    layer = QgsVectorLayer(f, '', 'ogr')
    
    layer.selectByExpression("\"DAYNIGHT\"= 'N'")
    
    destination = r"D:\WORK October 2023\viirs nightfires domain and landcover wise\viirs night fires" + "\\" + "{}.shp".format(name)
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)
    