import glob, pathlib
from pathlib import Path

# subsetting yearly fires
path = r"F:\WORK August 2022\drought-fires-spatial\sea grids"
directory = Path(path)

yearlygrids = glob.glob(str(directory) + '/*.shp')
masterpath = r"F:\WORK August 2022\drought-fires-spatial\sea-grid.shp"
master = QgsVectorLayer(str(gridpath), '', 'ogr')

layer_provider=master.dataProvider()
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
    master.updateFields()
    
    # append features
    for f in features:
        
        id = f.id()
        firecount = f.attributes()[fire_idx]
        attr_value={fire_idx+fieldcounter:firecount}
        layer_provider.changeAttributeValues({id:attr_value})
        
    fieldcounter += 1
    
master.commitChanges()