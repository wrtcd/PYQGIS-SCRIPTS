import glob, pathlib
from pathlib import Path
import processing

firedir = r"D:\WORK October 2023\viirs nightfires domain and landcover wise\southeastasia\2019"
fires = glob.glob(firedir + '/*.shp')
fires.sort()

countriespath = r"D:\WORK November 2023\nightfires-landcover-fc-frp\countries\southeastasia"
countries = glob.glob(countriespath+"/*.shp")

for c in countries:
    
    countryname = Path(c).stem.split('_')[0]
        
    for f in fires:
        
        year = Path(f).stem.split('_')[0]
        classnumber = Path(f).stem.split('_')[1]
                        
        destination = r"D:\WORK November 2023\nightfires-landcover-fc-frp\2019 southeast asia\{}".format(countryname) + "\\" + "{}_{}.shp".format(countryname, classnumber)
                
        parameters = {'INPUT': f, 
                      'OVERLAY': c, 
                      'OUTPUT': 'TEMPORARY_OUTPUT'}

        # run the clip tool
        clipped = processing.run("native:clip", parameters)        
        # processing.run("native:clip", parameters)
        
        clippedlayer = clipped['OUTPUT']
        
        singleparts = processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': 'TEMPORARY_OUTPUT'})
        
        points = singleparts['OUTPUT']
        
        writer = QgsVectorFileWriter.writeAsVectorFormat(points, destination, 'utf-8', driverName='ESRI Shapefile')
        del(writer)


