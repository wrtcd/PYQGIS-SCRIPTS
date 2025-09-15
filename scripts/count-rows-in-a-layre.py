import glob, pathlib
from pathlib import Path
import processing

file1 = r"D:\WORK December 2023\indonesia fire stuff\viirs\fire_archive_SV-C2_410250.shp"
file2 = r"D:\WORK December 2023\indonesia fire stuff\viirs\fire_nrt_SV-C2_410250.shp"

file3 = r"D:\WORK December 2023\indonesia fire stuff\viirs\viirs_indonesia_fires.shp"

layer1 = QgsVectorLayer(file1, '', 'ogr')
layer2 = QgsVectorLayer(file2, '', 'ogr')

layer3 = QgsVectorLayer(file3, '', 'ogr')

count1 = layer1.featureCount()
count2 = layer2.featureCount()

count3 = layer3.featureCount()

print(count1 + count2)
print(count3)