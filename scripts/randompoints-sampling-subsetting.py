import glob, pathlib
from pathlib import Path
import processing

zones = [x for x in range(1, 9)]
rasterpath = r"E:\WORK 2024 JULY\my paper - ccdc\uttarakhand-ba-count-over-time-rasters\countimagegt8.tif"
raster = QgsRasterLayer(rasterpath)

for zone in zones:
    
    print("zone:", zone)
    directory = Path(r"E:\WORK 2024 JULY\my paper - ccdc\zones")
    polygonpath = str(directory) + "\\" + "zone{}".format(zone) +  "\\" + r"zone{}.shp".format(zone) 
    layer = QgsVectorLayer(polygonpath, '', 'ogr')
    
    # generating 500 points
    parameters = {'INPUT': layer, 
                  'STRATEGY': 0, 
                  'VALUE': '100',
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
                  
    randompoints = processing.run("qgis:randompointsinsidepolygons", parameters)
    print("random points:", randompoints['OUTPUT'].featureCount())
    #sampling
    parameters = {'INPUT': randompoints['OUTPUT'], 
                  'RASTERCOPY': raster, 
                  'COLUMN_PREFIX': 'SAMPLED',
                  'OUTPUT': 'TEMPORARY_OUTPUT'}

    samplinglayer = processing.run("qgis:rastersampling", parameters)['OUTPUT']
        
    #selecting
    samplinglayer.selectByExpression("\"SAMPLED1\">= 1")
    print("samplinglayer points:", samplinglayer.featureCount())
    
    #destination
    destination = str(directory) + "\\" + "zone{}".format(zone) +  "\\" + "zone{}_testpoints".format(zone)
    
    writer = QgsVectorFileWriter.writeAsVectorFormat(samplinglayer, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)         

