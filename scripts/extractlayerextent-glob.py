import os
import processing
import glob
from qgis.PyQt.QtCore import QVariant

# Paths
# you need to define your local paths to the folders here
rasterdir = r"C:\Users\aeaturu\Desktop\SYRIA" #rasters folder
rasters = glob.glob(rasterdir + "/*.tif")
output_folder = r"C:\Users\aeaturu\Desktop\mergedcentroids" #output folder
os.makedirs(output_folder, exist_ok=True)

centroid_layers = []

for raster in rasters:
    raster_name = os.path.splitext(os.path.basename(raster))[0]

    # Run 'qgis:polygonfromlayerextent'
    extent_result = processing.run(
        "qgis:polygonfromlayerextent",
        {'INPUT': raster, 'OUTPUT': 'TEMPORARY_OUTPUT'}
    )

    # Assign CRS
    projected = processing.run(
        "native:assignprojection",
        {'INPUT': extent_result['OUTPUT'], 'CRS': 'EPSG:4326', 'OUTPUT': 'TEMPORARY_OUTPUT'}
    )

    # Create centroid
    centroid = processing.run(
        "qgis:centroids",
        {'INPUT': projected['OUTPUT'], 'ALL_PARTS': False, 'OUTPUT': 'memory:'}
    )

    # Remove existing fields
    layer = centroid['OUTPUT']
    provider = layer.dataProvider()

    existing_fields = provider.fields()
    provider.deleteAttributes([i for i in range(len(existing_fields))])

    # Add new 'filename' field
    provider.addAttributes([QgsField('filename', QVariant.String)])
    layer.updateFields()

    # Set raster_name as attribute value
    with edit(layer):
        for feature in layer.getFeatures():
            feature['filename'] = raster_name
            layer.updateFeature(feature)

    centroid_layers.append(layer)
    print(f"Processed centroid for: {raster_name}")

# Merge all centroid shapefiles
# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Full shapefile path (explicitly ensure this ends with .shp)
output_shapefile = os.path.join(output_folder, "mergedcentroids.shp")

# Merge all centroid shapefiles
processing.run(
    "qgis:mergevectorlayers",
    {'LAYERS': centroid_layers, 'CRS': 'EPSG:4326', 'OUTPUT': output_shapefile}
)

print(f"All centroids saved to: {output_shapefile}")

