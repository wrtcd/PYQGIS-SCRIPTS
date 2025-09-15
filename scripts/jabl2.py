import glob, pathlib
from pathlib import Path
import processing

firepath = r"D:\WORK March 2023\monthly fire persistence\country_monthly_persistence_shp"
gridpath = r"D:\WORK March 2023\monthly fire persistence\2kmgrid"

fires = glob.glob(str(firepath)+"/*shp")
grids = glob.glob(str(gridpath)+"/*shp")

fires.sort()
grids.sort()

pairs = [[fires[i], grids[i]] for i in range(9)]

for pair in pairs:

    fire = QgsVectorLayer(pair[0], '', 'ogr')
    grid = QgsVectorLayer(pair[1], '', 'ogr')
    
    destination = r"D:\WORK March 2023\monthly fire persistence\monthly_persistence_2km" + "\\" + Path(pair[0]).stem.split('_')[0] + "_persistence_2km.shp" 

    parameters = {'INPUT': grid,
                  'JOIN': fire,
                  'PREDICATE': [0, 1, 2, 3, 4, 5, 6],
                  'DISCARD_NONMATCHING':False,
                  'JOIN_FIELDS':['day', 'N', 'M ave(frp)', 'S ave(frp)'],
                  'OUTPUT': destination}
    
    processing.run("qgis:joinattributesbylocation", parameters)
                  
    
    
    
