import glob, pathlib
from pathlib import Path
import processing

firedir = r"E:\WORK January 2024\all fires 2012 2023"
fires = glob.glob(firedir + '/*.shp')
fires.sort()

countriespath = r"E:\WORK January 2024\onecountry"
countries = glob.glob(countriespath+"/*.shp")

for c in countries:
    
    print()
    country = Path(c).stem.split('_')[0]
    print(country)
    
    for f in fires:
        
        year = Path(f).stem.split('_')[1]
        print(year)
        
        destination = r"E:\WORK January 2024\yearlycountryfires\sea\{}\{}_{}".format(country, country, year)
                
        parameters = {'INPUT': f, 
                      'OVERLAY': c, 
                      'OUTPUT': 'TEMPORARY_OUTPUT'}

        # run the clip tool
        clipped = processing.run("native:clip", parameters)        
        # processing.run("native:clip", parameters)
        
        clippedlayer = clipped['OUTPUT']
        
        singleparts = processing.run('qgis:multiparttosingleparts', {'INPUT': clippedlayer, 'OUTPUT': 'TEMPORARY_OUTPUT'})
        
        points = singleparts['OUTPUT']
        
        # points.selectByExpression("\"DAYNIGHT\"= 'D'")

        writer = QgsVectorFileWriter.writeAsVectorFormat(points, destination, 'utf-8', driverName='ESRI Shapefile')
        del(writer)


