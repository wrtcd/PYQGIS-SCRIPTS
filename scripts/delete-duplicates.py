import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = pathlib.Path.home().joinpath('Desktop', 'join', 'yearly-protected-fires')

monthlyfires = glob.glob(str(directory.joinpath('Protected Monthly Fires'))+ '/*.shp')

Path(directory.joinpath('Protected Monthly Fires Clean')).mkdir(parents=True, exist_ok=True)

for fire in monthlyfires:

    vlayer = QgsVectorLayer(fire, '', 'ogr')
    
    destination = Path(fire).stem.replace('fires', 'fires_clean') + '.shp'

    parameters = {'INPUT': vlayer,
                  'OUTPUT': str(directory.joinpath('Protected Monthly Fires Clean', destination))}

    processing.run("native:deleteduplicategeometries", parameters)