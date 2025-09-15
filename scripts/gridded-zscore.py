import glob, pathlib
from pathlib import Path
import processing
from PyQt5.QtCore import QVariant
from statistics import mean
from statistics import stdev

# subsetting yearly fires
path = r"C:\Users\aeaturu\Desktop\fires\Gridded\griddedfires.shp"
gridded = QgsVectorLayer(path, '', 'ogr')

# create spatial index    
gridded.dataProvider().createSpatialIndex()
layer_provider = gridded.dataProvider()
layer_provider.addAttributes([QgsField("2012-20 Mean", QVariant.Double)])
layer_provider.addAttributes([QgsField("2012-20 Stdev", QVariant.Double)])
layer_provider.addAttributes([QgsField("2020 Z score", QVariant.Double)])
gridded.updateFields()  

meanfire_idx = gridded.fields().lookupField('2012-20 Mean')
stdfire_idx = gridded.fields().lookupField('2012-20 Stdev')
z_idx = gridded.fields().lookupField('2012-20 Z score')

features = gridded.getFeatures()

def divide(n, d):
    
    return n/d if d else 9999

for f in features:
    
    fid = f.id()
    firecount = [f.attributes()[x] for x in range(4, 13)]
    meanfire = mean(firecount)
    stdfire = stdev(firecount)
    num = (f.attributes()[12] - meanfire)
    den = stdfire
    z = divide(num, den)
    attr_value={meanfire_idx:meanfire, stdfire_idx:stdfire, z_idx:z}
    layer_provider.changeAttributeValues({id:attr_value})
    
# options for exporting weibull prbabilities shapefile
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"
filename = r"C:\Users\aeaturu\Desktop\fires\Gridded\zscores.shp"

# write to destination
QgsVectorFileWriter.writeAsVectorFormatV2(gridded, filename, QgsCoordinateTransformContext(), options)
    
    