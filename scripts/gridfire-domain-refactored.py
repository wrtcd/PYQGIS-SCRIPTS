import glob, pathlib
from pathlib import Path
import processing

# global directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022', 'FIRES')

layers = glob.glob(str(directory) + '/*merged.shp')

fire = layers[0]
grid = layers[1]
    
gridlayer = QgsVectorLayer(grid, '', 'ogr')

destination = str(directory) + "\\" + Path(grid).stem + "_refactored.shp" 

parameters = {'INPUT': gridlayer,
              'FIELDS_MAPPING':[
                  {
                     "expression":"\"X_COORD\"",
                     "length":17,
                     "name":"X_COORD",
                     "precision":6,
                     "type":6
                  },
                  {
                     "expression":"\"Y_COORD\"",
                     "length":17,
                     "name":"Y_COORD",
                     "precision":6,
                     "type":6
                  },
                  {
                     "expression":"\"Fires\"",
                     "length":8,
                     "name":"Fires",
                     "precision":0,
                     "type":2
                  }
               ],
              'OUTPUT': destination}


processing.run("native:refactorfields", parameters)
    
    
    
    
