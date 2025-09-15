import glob
import processing
from pathlib import Path

from qgis.core import (
    QgsRasterLayer,
    QgsVectorLayer,
    QgsRasterFileWriter,
    QgsRasterPipe,
    QgsRasterProjector,
    QgsRasterResampler,
    QgsRasterDataProvider
)
from qgis.analysis import QgsRasterCalculatorEntry, QgsRasterCalculator
from qgis.PyQt.QtCore import QVariant

# Set paths to your rasters and mask layer
raster_paths = glob.glob(r"D:\WORK 2024 JULY\BA Forest Mask\2019 bandipur images\all images" + "/*.tif")# List of raster file paths
mask_layer_path = r"D:\WORK 2024 JULY\BA Forest Mask\landcover\forestmask_vectorized_dissolved.shp"  # Path to the mask layer (vector)

# Load the mask layer
mask_layer = QgsVectorLayer(mask_layer_path, "Mask Layer", "ogr")
if not mask_layer.isValid():
    print("Mask layer failed to load!")
    exit(1)

# Loop through raster files and clip each
for raster_path in raster_paths:
    # Load the raster layer
    raster_layer = QgsRasterLayer(raster_path, "Raster Layer")
    if not raster_layer.isValid():
        print(f"Raster layer {raster_path} failed to load!")
        continue
    
    # Define the output file path
    output_path = raster_path.replace(".tif", "_forestmask_clipped.tif")
    
    # Perform the clipping operation
    processing.run("gdal:cliprasterbymasklayer", {
        'INPUT': raster_layer,
        'MASK': mask_layer,
        'OUTPUT': output_path
    })
    
    print(f"Raster {raster_path} clipped successfully to {output_path}")
