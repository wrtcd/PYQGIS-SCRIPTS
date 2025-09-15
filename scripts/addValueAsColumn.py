import glob, pathlib
from pathlib import Path
import processing

# yearly fire directory
directory = Path(r"E:\WORK January 2024\yearlycountriesmerged\sa")
fires = glob.glob(str(directory) + '/*.shp')

for fire in fires: 
    
    layer = QgsVectorLayer(fire, '', 'ogr')
        
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField("FRE", QVariant.Double, 'double', 15, 2)])

    layer.updateFields()

    for f in layer.getFeatures():
        
        m = f.attributes()[4]
        n = f.attributes()[1]
        value = m * n * 10 * 60
        layer_provider.changeAttributeValues({f.id(): {5: value}})
        
            


