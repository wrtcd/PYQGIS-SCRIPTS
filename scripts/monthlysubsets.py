import glob, pathlib
from pathlib import Path
import processing

# yearly fire directory
directory = Path(r"D:\WORK January 2023\monthlydroughtindices")
curryear = '2018'
files = glob.glob(str(directory.joinpath(curryear)) + '/*.shp')

months = ["%.2d" % i for i in range(1, 13)]
stringmonths = [str(int) for int in months]

lastday = {}
lastday['01'] = '31'
lastday['02'] = '28'
lastday['03'] = '31'
lastday['04'] = '30'
lastday['05'] = '31'
lastday['06'] = '30'
lastday['07'] = '31'
lastday['08'] = '31'
lastday['09'] = '30'
lastday['10'] = '31'
lastday['11'] = '30'
lastday['12'] = '31'

directory.joinpath(curryear, curryear + ' Monthly Fires').mkdir(parents=True, exist_ok=True)

for fire in files:
    
    year = fire[-8:-4]
    
    for month in stringmonths:
        
        # MONTHLY FIRE SUBSETS 
        lastday['02'] = '28'
        if year in ['2012', '2016', '2020']:
            lastday['02'] = '29'
        
        startDate = str(year)+'-{}-01'.format(month)
        endDate = str(year)+'-{}-{}'.format(month, lastday[month])
        
        print(startDate, endDate)
        
        layer = QgsVectorLayer(fire, '', 'ogr') 
        
        layer.selectByExpression("\"ACQ_DATE\">='{}' and \"ACQ_DATE\"<='{}'".format(startDate, endDate))
        
        destination = str(directory.joinpath(curryear, curryear + ' Monthly Fires', '{}_{}'.format(year, month)))
        fn = destination+".shp"
        
        writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
        del(writer)
            


