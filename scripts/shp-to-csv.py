import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\fire app\data")
fires = glob.glob(str(directory) + '/*.shp')

for fire in fires:
    
    firelayer = QgsVectorLayer(fire, '', 'ogr')
    filename = Path(fire).stem
    
    output = r"C:\Users\aeaturu\Desktop\WORK April 2025\aayushi - data download\clipped2" + "\\" + filename + '.csv'
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "CSV"

    QgsVectorFileWriter.writeAsVectorFormatV2(firelayer, output, QgsCoordinateTransformContext(), options)