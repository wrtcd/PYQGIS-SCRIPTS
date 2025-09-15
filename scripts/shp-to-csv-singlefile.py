import glob, pathlib
from pathlib import Path
import processing

country = 'vietnam'

# gridfire directory
fire = r"D:\WORK September 2022\fire-persistence\himawari-daily\{}\{}_merged.shp".format(country, country)

firelayer = QgsVectorLayer(fire, '', 'ogr')
filename = Path(fire).stem

output = r"D:\WORK September 2022\fire-persistence\himawari-daily\{}".format(country) + "\\" + filename + '.csv'
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "CSV"

QgsVectorFileWriter.writeAsVectorFormatV2(firelayer, output, QgsCoordinateTransformContext(), options)