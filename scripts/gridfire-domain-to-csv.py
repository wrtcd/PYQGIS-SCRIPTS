import glob, pathlib
from pathlib import Path
import processing

# gridfire directory
directory = pathlib.Path.home().joinpath('Desktop', 'January 2022','FIRES')

domaingrid = glob.glob(str(directory)+ '/*refactored.shp')
   
gridlayer = QgsVectorLayer(domaingrid[0], '', 'ogr')

output = directory.joinpath(str(Path(domaingrid[0]).stem)+'_csv.csv')
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "CSV"

QgsVectorFileWriter.writeAsVectorFormatV2(gridlayer, str(output), QgsCoordinateTransformContext(), options)
    
    