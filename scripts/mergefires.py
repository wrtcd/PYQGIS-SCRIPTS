import glob, pathlib
from pathlib import Path
import processing

# merging archived and nrt fires

directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','protected-areas-project', 'yearly-forest-fires')

vlayers = glob.glob(str(directory) + '/*.shp')

for layer in vlayers:
    
    source = Path(layer)
    filename = source.name
    
    if 'nrt' in filename:
        vlayer = QgsVectorLayer(layer, '' ,'ogr')
        
        features = vlayer.getFeatures()
               
        for f in features:
            fid = f.id()
            vlayer.startEditing()
            vlayer.changeAttributeValue(fid, 10, '1')
        
        vlayer.commitChanges()

parameters = {'LAYERS': vlayers, 
              'CRS': 'EPSG:4326', 
              'OUTPUT': str(vlayersource.joinpath("{}_fires.shp".format(country)))}

processing.run("qgis:mergevectorlayers", parameters)         



        