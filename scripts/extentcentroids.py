import os
import processing
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject

# Folder containing individual extent shapefiles
extent_folder = r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\uniqueextents"
output_centroids = r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\unique.shp"

# Collect all extent shapefile paths
extent_files = [
    os.path.join(extent_folder, f)
    for f in os.listdir(extent_folder)
    if f.endswith(".shp")
]

# Temporary list to hold centroid layer paths
centroid_layers = []

for extent_file in extent_files:
    centroid_temp = extent_file.replace("_extent.shp", "_centroid_temp.shp")

    try:
        processing.run(
            "qgis:centroids",
            {
                'INPUT': extent_file,
                'ALL_PARTS': False,
                'OUTPUT': centroid_temp
            }
        )
        centroid_layers.append(centroid_temp)
        print(f"Created centroid for: {os.path.basename(extent_file)}")
    except Exception as e:
        print(f"Failed to create centroid for {extent_file}: {e}")

# Merge all centroid shapefiles into a single one
try:
    processing.run(
        "qgis:mergevectorlayers",
        {
            'LAYERS': centroid_layers,
            'CRS': None,
            'OUTPUT': output_centroids
        }
    )
    print(f"All centroids saved to: {output_centroids}")
except Exception as e:
    print(f"Failed to merge centroid layers: {e}")
