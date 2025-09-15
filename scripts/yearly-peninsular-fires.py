import glob, pathlib
from pathlib import Path

# subsetting yearly fires
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','protected-areas-project')

vlayersource = directory.joinpath('shapes')
vlayer = glob.glob(str(vlayersource) + '/*fires.shp')
layer = QgsVectorLayer(vlayer[0], '', 'ogr')

years = list(range(2012, 2022))
stringyears = [str(int) for int in years]

for year in stringyears:
    
    startDate = year+'-01-01'
    endDate = year+'-12-31'
    
    layer.selectByExpression("\"ACQ_DATE\">='{}' and \"ACQ_DATE\"<='{}'".format(startDate, endDate))
    
    destination = str(directory.joinpath('yearly-peninsular-fires', 'peninsular_fires_'.format(year)))
    fn = destination+year+".shp"
    
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)