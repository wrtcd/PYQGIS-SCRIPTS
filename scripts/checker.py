import glob
from pathlib import Path
import processing

years = list(range(2000, 2023))

for y in years:
    
    direc = r"C:\Users\aeaturu\Desktop\combined_variables\var_{}".format(y)

    files = glob.glob(direc + "\*.shp")
    print(len(files))
    for f in files:
        
        layer = QgsVectorLayer(f, '', 'ogr')
        name = Path(f).stem.split('_')[0]
        fieldnames = [field.name() for field in layer.fields()]
        fields = len(fieldnames)
        rows = layer.featureCount()
        
        print(y, name, fields, rows)
    
    
    print()
