import glob, pathlib
from pathlib import Path

filepath = r"C:\Users\aeaturu\Desktop\sampledlc"
files = glob.glob(str(layerpath)+"./*shp")

for f in files:
    
    layer = QgsVectorLayer(f, '', 'ogr')

    with edit(layer):
            for feat in layer.getFeatures():
                    if feat[field] == None:
                        layer.deleteFeature(feat.id())
