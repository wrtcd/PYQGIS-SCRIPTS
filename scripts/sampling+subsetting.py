import glob, pathlib
from pathlib import Path
import processing

rasterpath = r"F:\WORK April 2022\Masks\ForestMask.tif"
raster = QgsRasterLayer(rasterpath, '')

firepath = r""
fire = QgsVectorLayer(firepath, '', 'ogr')
    
parameters = {'INPUT': fire, 
              'RASTERCOPY': raster, 
              'COLUMN_PREFIX': 'SAMPLED',
              'OUTPUT': 'TEMPORARY_OUTPUT'}

sampled = processing.run("qgis:rastersampling", parameters)['OUTPUT']

sampled.selectByExpression("\"SAMPLED1\">= 1")

destination = r"D:\WORK September 2022\seag\data\viirsag" + "\\" + finalname + ".shp"
writer = QgsVectorFileWriter.writeAsVectorFormat(layer, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
del(writer)


