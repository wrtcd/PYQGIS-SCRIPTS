import glob
import pandas
import processing
from pathlib import Path

files = glob.glob(r"D:\WORK 2024 OCTOBER\adityaeaturu-deeplearninglandcovermapping\classes\individualclassfiles" + "/*.shp")

for file in files:
    
    layer = QgsVectorLayer(file, '', 'ogr')
    print(Path(file).stem)
    
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField("id", QVariant.Int, 'int', 3, 0)])

    layer.updateFields()
    
    value = 1
    
    for f in layer.getFeatures():

        layer_provider.changeAttributeValues({f.id(): {2: value}})
        value = value + 1
        
        
    print('\n')
        