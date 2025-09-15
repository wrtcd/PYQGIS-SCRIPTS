import glob, pathlib
from pathlib import Path
import processing

# global country directory
region = "SEA"
country = "vietnam"
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','FIRES', region, country)

weibullshpsource = directory.joinpath('Yearly Grids', 'Weibull Shapes')
files = glob.glob(str(weibullshpsource) + '/*.shp')

# country grid

uri = str(directory) + "\\" + '{}_grid.shp'.format(country)
countrygrid = QgsVectorLayer(uri, '', 'ogr')

# create spatial index
countrygrid.dataProvider().createSpatialIndex()
Path(directory.joinpath('Yearly Grids', 'Weibull Grids')).mkdir(parents=True, exist_ok=True)

for file in files:
    
    # year = file[-8:-4]
    
    # if year in ['2012']:
      
    destination = str((directory.joinpath('Yearly Grids', 'Weibull Grids'))) + "\\" + Path(file).stem.replace('shp', 'grid') + ".shp" 
    
    parameters = {'INPUT': countrygrid,
                  'JOIN': file,
                  'JOIN_FIELDS': 'Weibull',
                  'OUTPUT': destination}
    
    processing.run("native:joinattributesbylocation", parameters)
    
    
    
    
