import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = pathlib.Path.home().joinpath('Desktop', 'yearly-forest-fires', 'yearly-forest-fires')

monthlyfirecounts = glob.glob(str(directory.joinpath('Protected Monthly Fire Counts'))+ '/*.shp')

directory.joinpath('Protected Monthly Fire Counts CSV').mkdir(parents=True, exist_ok=True)

for fire in monthlyfirecounts:
    
    year = fire[-23:-19]
    
    if year in ['2019', '2021']:
   
        firelayer = QgsVectorLayer(fire, '', 'ogr')

        output = str(directory.joinpath('Protected Monthly Fire Counts CSV'))+ "\\" + Path(fire).stem + '.csv'
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "CSV"

        QgsVectorFileWriter.writeAsVectorFormatV2(firelayer, output, QgsCoordinateTransformContext(), options)
    
    