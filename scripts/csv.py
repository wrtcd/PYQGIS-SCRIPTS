import glob, pathlib
from pathlib import Path
import processing

path = r"D:\WORK February 2022\FIRES"

region = "SEA"
country = "vietnam"
directory = Path(path).joinpath(region, country)

grids = glob.glob(str(directory) + "/*grids.shp")[0]

gridlayer = QgsVectorLayer(grids, '', 'ogr')

outputdirectory = directory
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "CSV"

QgsVectorFileWriter.writeAsVectorFormatV2(gridlayer, str(outputdirectory) + "\\" + Path(grids).stem + ".csv", QgsCoordinateTransformContext(), options)
    
    