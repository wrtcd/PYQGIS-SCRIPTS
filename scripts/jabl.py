import glob, pathlib
from pathlib import Path
import processing

firepath = r"D:\WORK March 2023\monthly fire persistence\country_monthly_persistence_shp"
gridpath = r"D:\WORK March 2023\monthly fire persistence\10mgrid"

fires = glob.glob(str(firepath)+"/*shp")
grids = glob.glob(str(gridpath)+"/*shp")

fires.sort()
grids.sort()

pairs = [[fires[i], grids[i]] for i in range(9)]

for pair in pairs:

    fire = QgsVectorLayer(pair[0], '', 'ogr')
    grid = QgsVectorLayer(pair[1], '', 'ogr')
    
    destination = r"D:\WORK March 2023\monthly fire persistence\monthly_persistence_10m" + "\\" + Path(pair[0]).stem.split('_')[0] + "_persistence_10m.shp" 

    parameters = {'INPUT': grid,
                  'JOIN': fire,
                  'PREDICATE': [0, 1, 2, 3, 4, 5, 6],
                  'DISCARD_NONMATCHING':False,
                  'JOIN_FIELDS':['N', 'S ave(frp)'],
                  'SUMMARIES':[5],
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
    
    run1 = processing.run("qgis:joinbylocationsummary", parameters)['OUTPUT']
    
    parameters = {'INPUT': run1,
                  'JOIN': fire,
                  'PREDICATE': [0, 1, 2, 3, 4, 5, 6],
                  'DISCARD_NONMATCHING':False,
                  'JOIN_FIELDS':['day', 'M ave(frp)'],
                  'SUMMARIES':[6],
                  'OUTPUT': destination}
                  
    processing.run("qgis:joinbylocationsummary", parameters)
                  
    
    
    
