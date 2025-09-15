import glob, pathlib
from pathlib import Path
import processing

path = r"F:\WORK September 2022\spatialjoins"
directory = Path(path)

fires = QgsProject.instance().mapLayers().values()

Path(directory.joinpath('VIIRS MODIS SHP')).mkdir(parents=True, exist_ok=True)

for fire in fires:
    
    outputdirectory = directory.joinpath('VIIRS MODIS SHP')
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    
    QgsVectorFileWriter.writeAsVectorFormatV2(fire, str(outputdirectory) + "\\" + fire.name() + ".shp", QgsCoordinateTransformContext(), options)
    
    