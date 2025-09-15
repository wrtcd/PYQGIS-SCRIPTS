import glob, pathlib
from pathlib import Path

# subsetting yearly fires
path = r"F:\WORK August 2022\drought-fires-spatial\sea fires"
directory = Path(path)

dest = Path(r"F:\WORK August 2022\drought-fires-spatial\sea grids")

yearlyfires = glob.glob(str(directory) + '/*.shp')
gridpath = r"F:\WORK August 2022\drought-fires-spatial\sea-grid.shp"
grid = QgsVectorLayer(str(gridpath), '', 'ogr')

for fire in yearlyfires:
    
    year = Path(fire).stem[-4:]
    destination = Path(fire).stem.replace('fires', 'grid') + '.shp'
    
    parameters = {'POLYGONS': grid,
                  'POINTS': fire,
                  'WEIGHT': 'VERSION',
                  'FIELD': year+'_fires',  
                  'OUTPUT': str(dest.joinpath(destination))}

    processing.run("native:countpointsinpolygon", parameters) 