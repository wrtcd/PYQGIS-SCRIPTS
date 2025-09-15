import glob, pathlib
from pathlib import Path

# fires directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022', 'protected-areas-project')

firesource = directory.joinpath('yearly-forest-fires')
peninsularfires = glob.glob(str(firesource) + '/*.shp')

uri = r"C:\Users\aeaturu\Desktop\January 2022\protected-areas-project\shapes\peninsular_countries.shp"
protectedcountries = QgsVectorLayer(uri, '', 'ogr')

Path(directory.joinpath('Fire Counts')).mkdir(parents=True, exist_ok=True)

for fire in peninsularfires:
    
    destination = Path(fire).stem.replace('forest_fires', 'fire_counts') + '.shp'
    
    parameters = {'POLYGONS': protectedcountries,
                  'POINTS': fire,
                  'WEIGHT': 'VERSION',
                  'FIELD': 'Fires',  
                  'OUTPUT': str(directory.joinpath('Fire Counts', destination))}

    processing.run("native:countpointsinpolygon", parameters) 