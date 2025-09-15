import glob, pathlib
from pathlib import Path
import processing

# merging archived and nrt fires
region = "SA"
country = "afghanistan"
directory = pathlib.Path.home().joinpath('Desktop','January 2022', 'FIRES')

vlayersource = directory.joinpath(region, country)
vlayers = glob.glob(str(vlayersource) + '/*.shp')

for layer in vlayers:
    
    source = Path(layer)
    filename = source.name
    
    if 'SV' in filename:
        
        fires = QgsVectorLayer(layer,'','ogr')
        
    else:
        
        country = QgsVectorLayer(layer, '', 'ogr')
        
fires.dataProvider().createSpatialIndex()

destination = str(vlayersource.joinpath("{}_fires.shp".format(country)))
        
parameters = {'INPUT': fires, 
              'OVERLAY': country, 
              'OUTPUT': countrygrid}

# run the clip tool
processing.run("native:clip", parameters)        



        