from qgis.core import QgsRasterLayer, QgsProcessingFeedback, QgsProject
from qgis import processing
import glob
import os
import numpy as np
from osgeo import gdal

# Input and output paths
input_dir = r"C:\Users\aeaturu\Desktop\brunei_test\output"  # Directory containing the 12 rasters
aligned_dir = os.path.join(input_dir, "aligned")  # Temporary directory for aligned rasters
output_path = r"C:\Users\aeaturu\Desktop\brunei_test\output\test.tif"  # Output raster path

# Ensure output directories exist
os.makedirs(aligned_dir, exist_ok=True)

# Get all raster file paths
raster_paths = glob.glob(os.path.join(input_dir, "*.tif"))
if len(raster_paths) != 12:
    print(f"Expected 12 rasters, found {len(raster_paths)}. Check input directory.")
    exit()

# Align rasters to the first raster as reference
reference_raster = raster_paths[0]
aligned_raster_paths = []

for raster_path in raster_paths:
    aligned_raster_path = os.path.join(aligned_dir, os.path.basename(raster_path))
    params = {
        'INPUT': raster_path,
        'TARGET_CRS': None,  # Use original CRS
        'RESAMPLING': 0,  # Nearest neighbor
        'NODATA': None,
        'TARGET_EXTENT': reference_raster,  # Align to the extent of the first raster
        'TARGET_EXTENT_CRS': None,
        'TARGET_RESOLUTION': None,
        'OUTPUT': aligned_raster_path
    }
    processing.run("gdal:warpreproject", params)
    aligned_raster_paths.append(aligned_raster_path)

# Function to load raster as NumPy array
def load_raster_as_array(raster_path):
    raster = gdal.Open(raster_path)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    raster = None  # Close raster
    return array

# Initialize the valid mask with ones (1: valid, 0: invalid)
valid_mask = None

# Process each aligned raster
for raster_path in aligned_raster_paths:
    raster_array = load_raster_as_array(raster_path)
    # Create a binary mask where values > 0 are valid
    raster_mask = (raster_array > 0).astype(np.uint8)
    if valid_mask is None:
        valid_mask = raster_mask
    else:
        # Perform a logical AND operation to combine masks
        valid_mask = valid_mask & raster_mask

# Save the valid mask as a new raster
reference_raster = gdal.Open(aligned_raster_paths[0])  # Use the first aligned raster as reference
driver = gdal.GetDriverByName("GTiff")
rows, cols = valid_mask.shape
out_raster = driver.Create(output_path, cols, rows, 1, gdal.GDT_Byte)
out_raster.SetGeoTransform(reference_raster.GetGeoTransform())
out_raster.SetProjection(reference_raster.GetProjection())
out_band = out_raster.GetRasterBand(1)
out_band.WriteArray(valid_mask)
out_band.SetNoDataValue(0)
out_raster.FlushCache()
out_raster = None  # Close the raster file

# Add the output raster to QGIS
output_layer = QgsRasterLayer(output_path, "Common Valid Pixels")
if output_layer.isValid():
    QgsProject.instance().addMapLayer(output_layer)
    print("Valid pixels raster added to QGIS successfully.")
else:
    print("Failed to load the output raster.")
