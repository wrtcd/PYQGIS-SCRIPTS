import glob, pathlib
from pathlib import Path

country = 'vietnam'

# subsetting yearly fires
directory = Path(r"E:\WORK January 2024\yearlycountryfires\sea\{}".format(country))
layers = glob.glob(str(directory) + '/*.shp')

destination = str(directory.joinpath("{}_2012-2023.shp".format(country)))

parameters = {'LAYERS': layers, 
              'CRS': 'EPSG:4326', 
              'OUTPUT': 'TEMPORARY_OUTPUT'
              }

merged = processing.run("qgis:mergevectorlayers", parameters)

mergedlayer = merged['OUTPUT']

singleparts = processing.run('qgis:multiparttosingleparts', {'INPUT': mergedlayer, 'OUTPUT': 'TEMPORARY_OUTPUT'})

points = singleparts['OUTPUT']

writer = QgsVectorFileWriter.writeAsVectorFormat(points, destination, 'utf-8', driverName='ESRI Shapefile')
del(writer)


