import glob, pathlib
from pathlib import Path
import processing
from PyQt5.QtCore import QVariant

# subsetting yearly fires
path = r"C:\Users\aeaturu\Desktop\fires"

directory = Path(path)
firedirectory = Path(path).joinpath('Domain Fires')
fires = glob.glob(str(firedirectory) + '/*.shp')

gridpath = r"C:\Users\aeaturu\Desktop\fires\Country SHP\domain_grid.shp"
countlayer = QgsVectorLayer(gridpath, '', 'ogr')

layer_provider = countlayer.dataProvider()

for fire in fires: #for each fire file

    #firelayer
    firelayer = QgsVectorLayer(fire, '', 'ogr')
    
    #create a new field
    year = Path(fire).stem[-4:]
    layer_provider = countlayer.dataProvider()
    layer_provider.addAttributes([QgsField("{}".format(year), QVariant.Double)])
    countlayer.updateFields()
    
    # processing parameters for counting points in polygons
    parameters = {'POLYGONS': countlayer,
                  'POINTS': firelayer,
                  'FIELD': '{}'.format(year),  
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
    
    # count points in polygons
    countpointsinpolygon = processing.run("native:countpointsinpolygon", parameters) 

    # retrieve counts layer from the processing result
    countlayer = countpointsinpolygon['OUTPUT']
    
# create spatial index    
countlayer.dataProvider().createSpatialIndex()

# options for exporting weibull prbabilities shapefile
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"
filename = r"C:\Users\aeaturu\Desktop\fires\Gridded\griddedfires.shp"

# write to destination
QgsVectorFileWriter.writeAsVectorFormatV2(countlayer, filename, QgsCoordinateTransformContext(), options)
    
    