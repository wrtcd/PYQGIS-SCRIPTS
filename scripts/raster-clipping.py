import glob, pathlib
from pathlib import Path
import processing

rasterdir = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\GOES-ANIMATIONS\rasters_4326")
rasters = glob.glob(str(rasterdir)+"/*.tif")

statesdir = r"C:\Users\aeaturu\Desktop\WORK April 2025\GOES-ANIMATIONS\boundaries"
states = glob.glob(statesdir+"/*.shp")


for state in states:

    for raster in rasters:
        
        file = QgsRasterLayer(raster,'')
        year = Path(raster).stem.split('_')[0]
        
        statename = Path(state).stem.split('_')[0]
        
        outputname = r"{}_{}.tif".format(statename, year)
        print(outputname)
        
        destination = r"C:\Users\aeaturu\Desktop\WORK April 2025\GOES-ANIMATIONS\rasterclipped\{}".format(outputname)
                
        parameters = {  'INPUT': file,
                        'MASK': state,
                        'ALPHA_BAND': False,
                        'CROP_TO_CUTLINE': True,
                        'KEEP_RESOLUTION': True,
                        'OPTIONS': None,
                        'DATA_TYPE': 0,
                        'OUTPUT': destination
                    }
                      
        processing.run('gdal:cliprasterbymasklayer', parameters)
            