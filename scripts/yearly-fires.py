import glob, pathlib
from pathlib import Path

firepath = r"C:\Users\aeaturu\Desktop\Southeast USA Data Download\preppedfiredataset\seusa_allFires.shp"
firelayer = QgsVectorLayer(firepath, '', 'ogr')

years = list(range(2012, 2026))
stringyears = [str(int) for int in years]

for year in stringyears:
    
        startDate = year+'-01-01'
        endDate = year+'-12-31'
        
        firelayer.selectByExpression("\"ACQ_DATE\">='{}' and \"ACQ_DATE\"<='{}'".format(startDate, endDate))
        
        filename = "seusa_{}".format(year)
        destination = r"C:\Users\aeaturu\Desktop\Southeast USA Data Download\preppedfiredataset\yearlyfires\{}.shp".format(filename)
        
        writer = QgsVectorFileWriter.writeAsVectorFormat(firelayer, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
        del(writer)