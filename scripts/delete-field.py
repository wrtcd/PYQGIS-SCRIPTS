import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = Path(r"E:\WORK January 2024\yearlycountryfires\sea\philippines")
fires = glob.glob(str(directory) + '/*.shp')

for fire in fires:
    
    # Get a layer object and enter edit mode:
    my_vectorlayer = QgsVectorLayer(fire, '', 'ogr')
    with edit(my_vectorlayer):
        # Get the field index by its name:
        field1 = my_vectorlayer.fields().indexFromName('layer')
        field2 = my_vectorlayer.fields().indexFromName('path')
        field3= my_vectorlayer.fields().indexFromName('VERSION')
        fields = [field1, field2, field3]
        # Delete the field by its index, note that it has to be in a list:
        my_vectorlayer.dataProvider().deleteAttributes(fields)
    # Update the fields, so the changes are recognized:
    my_vectorlayer.updateFields()