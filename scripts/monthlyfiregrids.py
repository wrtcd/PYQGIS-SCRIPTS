from pathlib import Path
import glob
import processing

directory = Path(r"D:\WORK January 2023\monthlydroughtindices")
curryear = '2020'
destdir = curryear + " Monthly Fires"
fires = glob.glob(str(directory.joinpath(curryear, destdir)) + '/*.shp')

gridpath = r"D:\WORK January 2023\monthlydroughtindices\30mingrid.shp"
grid = QgsVectorLayer(gridpath, '', 'ogr')

directory.joinpath(curryear, curryear + ' Monthly Fire Grids').mkdir(parents=True, exist_ok=True)

for file in fires:
    
    fn = Path(file).stem
    fire = QgsVectorLayer(file, '', 'ogr')
    destination = str(directory.joinpath(curryear, curryear + ' Monthly Fire Grids', "{}.shp".format(fn)))
    
    parameters = {'INPUT': grid,
                  'JOIN': fire,
                  'PREDICATE': [0, 1, 2, 3, 4, 5, 6],
                  'JOIN_FIELDS':['FRP', 'FC'],
                  'SUMMARIES':[5,6],
                  'DISCARD_NONMATCHING':False,
                  'OUTPUT': destination
                                            }
    processing.run("qgis:joinbylocationsummary", parameters)