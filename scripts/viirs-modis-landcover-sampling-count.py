import glob, pathlib
from pathlib import Path
import processing

firepath = r"D:\WORK October 2023\viirs nightfires domain and landcover wise\viirs night fires\ssea_2012_N.shp"
fire  = QgsVectorLayer(firepath, '','ogr') 

rasterpath = r"D:\WORK October 2023\viirs nightfires domain and landcover wise\2012SA\one.tif"
raster = QgsRasterLayer(rasterpath, '')

parameters = {'INPUT': fire, 
              'RASTERCOPY': raster, 
              'COLUMN_PREFIX': 'SAMPLED',
              'OUTPUT': 'TEMPORARY_OUTPUT'}

sampled = processing.run("qgis:rastersampling", parameters)['OUTPUT']
sampled.selectByExpression("\"SAMPLED1\">= 1")

destination = r"D:\WORK October 2023\viirs nightfires domain and landcover wise\2012SA" + "\\" + "onesampled.shp"
writer = QgsVectorFileWriter.writeAsVectorFormat(sampled, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
del(writer)