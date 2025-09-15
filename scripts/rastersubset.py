import glob
from pathlib import Path
import processing

years = [x for x in range(1, 24)]

rasterpath = r"C:\Users\aeaturu\Downloads\hansenAligned.tif"
rasterlayer = QgsRasterLayer(rasterpath,'hansenAligned')

for year in years:
    
    destination = r"C:\Users\aeaturu\Downloads\hansen\lossyear_{}.tif".format(year)
    
    #I find it nice to create parameters as a dictionary
    parameters = {'INPUT_A' : rasterlayer,
            'BAND_A' : 4,
            'FORMULA' : '(A == {})'.format(year),   
            'OUTPUT' : destination}

    processing.run('gdal:rastercalculator', parameters)