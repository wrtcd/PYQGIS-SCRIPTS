import glob, pathlib
from pathlib import Path
import processing

firepath = r"D:\WORK December 2023\indonesia fire stuff\landcoverpartitioning\modis\modis_indonesia_2018_allfires.shp"
fire  = QgsVectorLayer(firepath, '','ogr') 

rasterspath = r"D:\WORK December 2023\indonesia fire stuff\landcover"
rasters = glob.glob(rasterspath + "/*.tif")

for r in rasters: 
    
    raster = QgsRasterLayer(r, '')
    
    parameters = {'INPUT': fire, 
                  'RASTERCOPY': raster, 
                  'COLUMN_PREFIX': 'SAMPLED',
                  'OUTPUT': 'TEMPORARY_OUTPUT'}

    sampled = processing.run("qgis:rastersampling", parameters)['OUTPUT']
    sampled.selectByExpression("\"SAMPLED1\">= 1")
    
    fn = 'modis_2018_' + Path(r).stem + '_fires.shp'
    
    destination = r"D:\WORK December 2023\indonesia fire stuff\landcoverpartitioning\modis\subsetted" + "\\" + fn
    writer = QgsVectorFileWriter.writeAsVectorFormat(sampled, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)