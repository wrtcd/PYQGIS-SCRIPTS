import glob
from pathlib import Path

rasterspath = r"C:\Users\aeaturu\Desktop\brunei_test"
rasters = glob.glob(rasterspath + "/*.tif")

for raster in rasters:
    
    input_raster = QgsRasterLayer(raster,'' )
    
    filename = Path(raster).stem
    
    destination = r"C:\Users\aeaturu\Desktop\brunei_test\output\{}_gt0.tif".format(filename)
    
    #I find it nice to create parameters as a dictionary
    parameters = {'INPUT_A' : input_raster,
            'BAND_A' : 1,
            'FORMULA' : '(A > 0)',   
            'OUTPUT' : destination}

    processing.run('gdal:rastercalculator', parameters) 
    