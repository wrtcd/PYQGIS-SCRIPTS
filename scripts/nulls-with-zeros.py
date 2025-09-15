def replace_nulls(layer):
    with edit(layer):
        for feat in layer.getFeatures():
            for field in feat.fields().names():
                if feat[field] == None:
                    feat[field] = '1'
            layer.updateFeature(feat)
            
import glob, pathlib
from pathlib import Path
import processing

dir = r"D:\WORK December 2023\indonesia fire stuff\maps\himawari\gridded"
files = glob.glob(dir + "/*.shp")

for f in files:
    
    layer = QgsVectorLayer(f, '', 'ogr')
    print(Path(f).stem.split('_')[0])
    replace_nulls(layer)