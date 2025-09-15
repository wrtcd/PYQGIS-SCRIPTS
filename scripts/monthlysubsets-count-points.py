import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = pathlib.Path.home().joinpath('Desktop', 'yearly-forest-fires', 'yearly-forest-fires')

# monthlyfires = glob.glob(str(directory.joinpath('Protected Monthly Fires Clean'))+ '/*.shp')
monthlyfires = glob.glob(str(directory.joinpath('Protected Monthly Fires'))+ '/*.shp')

directory.joinpath('Protected Monthly Fire Counts').mkdir(parents=True, exist_ok=True)

uri = r"C:\Users\aeaturu\Desktop\January 2022\protected-areas-project\shapes\peninsular_countries.shp"
peninsularcountries = QgsVectorLayer(uri, '', 'ogr')

for fire in monthlyfires:
    
    year = fire[-17:-13]
    
    if year in ['2019', '2021']:

        layer = QgsVectorLayer(fire, '', 'ogr')
        
        destination = Path(fire).stem.replace('fires', 'fire_counts') + '.shp'

        parameters = {'POLYGONS': peninsularcountries,
                      'POINTS': layer,
                      'WEIGHT': 'VERSION',
                      'FIELD': 'Fires',  
                      'OUTPUT': str(directory.joinpath('Protected Monthly Fire Counts', destination))}

        processing.run("native:countpointsinpolygon", parameters)