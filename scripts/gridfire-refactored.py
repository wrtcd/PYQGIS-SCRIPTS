import glob, pathlib
from pathlib import Path
import processing

# grids directory
path = r"D:\WORK February 2022\FIRES"

region = "SA"
country = "afghanistan"
directory = Path(path)

gridsource = directory.joinpath(region, country, 'Yearly Grids')
yearlygrids = glob.glob(str(gridsource) + '/*.shp')

Path(gridsource.joinpath('Refactored')).mkdir(parents=True, exist_ok=True)

for grid in yearlygrids:
    
    gridlayer = QgsVectorLayer(grid, '', 'ogr')
    
    gridlayer.startEditing()
    gridlayer.dataProvider().deleteAttributes([0, 1])
    gridlayer.updateFields()
    gridlayer.commitChanges()
    
    
    destination = str(gridsource.joinpath('Refactored')) + "\\" + Path(grid).stem + ".shp" 
    
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
    
    
    
    
