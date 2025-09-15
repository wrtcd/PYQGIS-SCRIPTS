import glob, pathlib
from pathlib import Path
from PyQt5.QtCore import QVariant

# subsetting yearly fires
path = r"D:\WORK April 2022\Fires"

# directory
directory = Path(path)

# yearly grid fires
gridsource = directory.joinpath('Yearly Ag Grids')
yearlygrids = glob.glob(str(gridsource) + '/*.shp')

# yearly grid original
domaingridpath = directory.joinpath('domain_grid.shp')
domaingrid = QgsVectorLayer(str(domaingridpath), '', 'ogr')

# save clone file parameters
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"
filename = gridsource.joinpath('domain_ag_grids.shp')

# write to destination
QgsVectorFileWriter.writeAsVectorFormatV2(domaingrid, str(filename), QgsCoordinateTransformContext(), options)

cloned = QgsVectorLayer(str(filename), '', 'ogr')
layer_provider=cloned.dataProvider()
layer_provider.createSpatialIndex()
cloned.startEditing()
fieldcounter = 0

# append each grid layer fires
for grid in yearlygrids:
    
    gridlayer = QgsVectorLayer(grid, '', 'ogr')
    features = gridlayer.getFeatures()
    
    year = Path(grid).stem[-4:]
    firefield = year+'_fires'
    print(firefield)
    fire_idx = gridlayer.fields().lookupField(firefield)
    
    layer_provider.addAttributes([QgsField(firefield,QVariant.Double, 'double', 7)])
    cloned.updateFields()
    
    # append features
    for f in features:
        
        id = f.id()
        firecount = f.attributes()[fire_idx]
        attr_value={fire_idx+fieldcounter:firecount}
        layer_provider.changeAttributeValues({id:attr_value})
        
    fieldcounter += 1
        
print(cloned.fields().names())
cloned.dataProvider().createSpatialIndex()
cloned.commitChanges()

# add result to project
iface.addVectorLayer(str(filename), Path(filename).stem, 'ogr')