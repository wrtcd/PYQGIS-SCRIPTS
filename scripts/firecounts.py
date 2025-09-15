import glob, pathlib
from pathlib import Path

# subsetting yearly fires
path = r"D:\WORK February 2022\FIRES"

region = "SEA"
country = "vietnam"
directory = Path(path).joinpath(region, country)

vlayer = glob.glob(str(directory) + '/*fires.shp')
layer = QgsVectorLayer(vlayer[0], '', 'ogr')
layer.dataProvider().createSpatialIndex()

years = list(range(2012, 2022))
stringyears = [str(int) for int in years]

Path(directory.joinpath('Yearly Fires')).mkdir(parents=True, exist_ok=True)

for year in stringyears:
    
    startDate = year+'-01-01'
    endDate = year+'-12-31'
    
    layer.selectByExpression("\"ACQ_DATE\">='{}' and \"ACQ_DATE\"<='{}'".format(startDate, endDate))
    
    destination = str(directory.joinpath('Yearly Fires', '{}_fires_'.format(country)))
    fn = destination+year+".shp"
    
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
    del(writer)