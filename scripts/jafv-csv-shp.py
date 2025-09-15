import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = Path(r"F:\WORK January 2023\monthlydroughtindices")

years = [y for y in range(2012, 2023)]
years = [str(year) for year in years]
months = [m for m in range(12)]

for y in years: 
    
    currdir = directory.joinpath(y)
    droughtdir = currdir.joinpath('{} Drought Indices'.format(y))
    griddir = currdir.joinpath('{} Monthly Fire Grids'.format(y))

    currdir.joinpath(y + ' Monthly Subsets').mkdir(parents=True, exist_ok=True)

    droughts = glob.glob(str(droughtdir) + '/*.csv')
    grids = glob.glob(str(griddir) + '/*.shp')

    droughts.sort()
    grids.sort()
    
    for m in months:
        
        uri = 'file:///{}?delimiter=,&yField=y&xField=x&crs=EPSG:4326'.format(droughts[m])
        droughtlayer = QgsVectorLayer(uri, '', 'delimitedtext')
        gridlayer = QgsVectorLayer(grids[m], '', 'ogr')
        
        droughtlayer.dataProvider().createSpatialIndex()
        gridlayer.dataProvider().createSpatialIndex()
        
        fn = Path(grids[m]).stem
        destination = str(currdir.joinpath(y + ' Monthly Subsets', "{}.shp".format(fn)))
        
        parameters = {'INPUT': gridlayer, 
                      'FIELD': 'id',
                      'INPUT_2': droughtlayer, 
                      'FIELD_2': 'id',
                      'DISCARD_NONMATCHING' : False,
                      'FIELDS_TO_COPY':['TCI','VCI','VHI'],
                      'METHOD' : 1,
                      'OUTPUT': destination}
                      
        joined = processing.run("native:joinattributestable", parameters)
    
    
    
    