import glob, pathlib
from pathlib import Path
import processing

# csv directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','FIRES')

files = glob.glob(str(directory) + '/*weibull_shp.shp')
file = files[0]

# country grid
domaingridsrc = glob.glob(str(directory) + '/*merged.shp')
domaingrid = QgsVectorLayer(domaingridsrc[1], '', 'ogr')

# create spatial index
domaingrid.dataProvider().createSpatialIndex()
     
destination = str(directory) + "\\" + Path(file).stem.replace('shp', 'grid') + ".shp" 

parameters = {'INPUT': domaingrid,
              'JOIN': file,
              'JOIN_FIELDS': 'Weibull',
              'OUTPUT': destination}

processing.run("native:joinattributesbylocation", parameters)
    
    
    
    
