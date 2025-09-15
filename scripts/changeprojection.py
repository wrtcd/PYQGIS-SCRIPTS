import os
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsProcessingFeedback,
    QgsApplication,
    QgsProcessing
)
import processing

# === Set Paths ===
input_folder = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\preppedcropscape"
output_folder = r"C:\Users\aeaturu\Desktop\WORK April 2025\GOES-ANIMATIONS\rasterclipped"
target_crs = 'EPSG:4326'  # Change to your desired CRS

os.makedirs(output_folder, exist_ok=True)

# === Initialize Feedback ===
feedback = QgsProcessingFeedback()

# === Loop Through Rasters ===
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".tif"):
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{base_name}_4326.tif")

        print(f"📂 Reprojecting: {filename}")

        processing.run("gdal:warpreproject", {
            'INPUT': input_path,
            'SOURCE_CRS': None,  # autodetect
            'TARGET_CRS': QgsCoordinateReferenceSystem(target_crs),
            'RESAMPLING': 0,
            'NODATA': None,
            'TARGET_RESOLUTION': None,
            'OPTIONS': '',
            'DATA_TYPE': 0,  # use original data type
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'MULTITHREADING': True,
            'EXTRA': '',
            'OUTPUT': output_path
        }, feedback=feedback)

        print(f"✅ Saved: {output_path}")
