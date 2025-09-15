import glob, pathlib
from pathlib import Path
import processing
from PyQt5.QtCore import QVariant

# subsetting yearly fires
path = r"D:\WORK June 2022\Z-scores\fires"

directory = Path(path)
firedirectory = Path(path).joinpath('Domain Fires')
fires = glob.glob(str(firedirectory) + '/*.shp')

gridpath = r"D:\WORK June 2022\Z-scores\fires\Country SHP\domain_grid.shp"
meanfrp = QgsVectorLayer(gridpath, '', 'ogr')

layer_provider = meanfrp.dataProvider()

for fire in fires: #for each fire file

    #firelayer
    firelayer = QgsVectorLayer(fire, '', 'ogr')
    
    # processing parameters for counting points in polygons
    parameters = {'INPUT': meanfrp,
                  'JOIN': firelayer,
                  'PREDICATE': 1,
                  'JOIN_FIELDS': 'FRP',
                  'SUMMARIES': 5,
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
    
    # count points in polygons
    meanfrpinapolygon = processing.run("qgis:joinbylocationsummary", parameters) 

    # retrieve counts layer from the processing result
    meanfrp = meanfrpinapolygon['OUTPUT']
    
# create spatial index    
meanfrp.dataProvider().createSpatialIndex()

# options for exporting weibull prbabilities shapefile
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"
filename = r"D:\WORK June 2022\Z-scores\fires\Gridded\griddedfrpsum.shp"

# write to destination
QgsVectorFileWriter.writeAsVectorFormatV2(meanfrp, filename, QgsCoordinateTransformContext(), options)
    
    