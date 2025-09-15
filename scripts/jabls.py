import glob, pathlib
from pathlib import Path
import processing

firepath = r"D:\WORK December 2023\indonesia fire stuff\maps\himawari\himawari_indonesia_2019_09_fires.shp"
gridpath = r"D:\WORK December 2023\indonesia fire stuff\maps\indonesiagrids"

fire = QgsVectorLayer(firepath, '', 'ogr')
grids = glob.glob(gridpath+"/*.shp")

grids.sort()

for grid in grids:
    
    resolution = Path(grid).stem.split('_')[1]

    grid = QgsVectorLayer(grid, '', 'ogr')
    
    destination = r"D:\WORK December 2023\indonesia fire stuff\maps\himawari\gridded" + "\\" + "himawari_gridded_201909_{}.shp".format(resolution) 
    
    parameters = {'INPUT': grid,
                  'JOIN': fire,
                  'PREDICATE': [0, 1, 2, 3, 4, 5, 6],
                  'DISCARD_NONMATCHING':False,
                  'JOIN_FIELDS':['N', 'ave(frp)', 'max(frp)'],
                  'SUMMARIES':[5, 6],
                  'OUTPUT': destination}
    
    processing.run("qgis:joinbylocationsummary", parameters)