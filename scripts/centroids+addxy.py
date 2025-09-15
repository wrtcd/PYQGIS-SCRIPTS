import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = Path(r"D:\WORK September 2022\fire-persistence\grids")
grids = glob.glob(str(directory) + '/*.shp')

for g in grids:
    
    parameters = {
                'INPUT': g,
                'ALL_PARTS': False,
                'OUTPUT': 'TEMPORARY_OUTPUT'
                                                }

    centroids = processing.run("native:centroids", parameters)['OUTPUT']

    destination = r"D:\WORK September 2022\fire-persistence\grids-xy" + "\\" + Path(g).stem + '.shp'

    parameters = {
                'INPUT': centroids,
                'CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
                'OUTPUT': 'TEMPORARY_OUTPUT'
                                                }

    xy = processing.run("native:addxyfields", parameters)['OUTPUT']

    parameters = {
                'INPUT': xy,
                'FIELDS_MAPPING': [{'expression': '"id"','length': 6,'name': 'id','precision': 0,'type': 2},
                {'expression': '"lat"','length': 3,'name': 'lat','precision': 2,'type': 6},
                {'expression': '"lon"','length': 3,'name': 'lon','precision': 2,'type': 6},
                {'expression': '"x"','length': 20,'name': 'x','precision': 2,'type': 6},
                {'expression': '"y"','length': 20,'name': 'y','precision': 2,'type': 6}],
                'OUTPUT': 'TEMPORARY_OUTPUT'
                                                }

    xyadded = processing.run("native:refactorfields", parameters)['OUTPUT']

    xyadded.dataProvider().deleteAttributes([1, 2])
    xyadded.updateFields()
    
    grid = QgsVectorLayer(g, '', 'ogr')
    
    parameters = {
                    'INPUT': grid,
                    'FIELD':'id',
                    'INPUT_2': xyadded,
                    'FIELD_2':'id',
                    'FIELDS_TO_COPY': ['x','y'],
                    'METHOD':1,
                    'DISCARD_NONMATCHING':False,
                    'PREFIX':'',
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                                    }
                                                                    
    joinlayer = processing.run("native:joinattributestable", parameters)['OUTPUT']
    
    joinlayer.dataProvider().deleteAttributes([1, 2])
    joinlayer.updateFields()
    
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"

    QgsVectorFileWriter.writeAsVectorFormatV2(joinlayer, destination, QgsCoordinateTransformContext(), options)





