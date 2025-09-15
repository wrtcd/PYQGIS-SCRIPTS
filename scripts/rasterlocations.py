import os
from qgis.core import (
    QgsRasterLayer, 
    QgsPointXY, 
    QgsFeature, 
    QgsGeometry, 
    QgsVectorLayer, 
    QgsField, 
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsProject
)
from PyQt5.QtCore import QVariant
import processing
from datetime import datetime

# INPUTS
input_folder = r"E:\Planet Data"
output_shapefile = r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\allplanetdata.shp"

# Step 1: Gather all .tif raster files recursively
raster_files = []
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".tif") or file.endswith(".tiff"):
            raster_files.append(os.path.join(root, file))

# Temp list of centroid layers
centroid_layers = []

# Step 2: Create centroid point layers for each raster
for raster_path in raster_files:
    basename = os.path.basename(raster_path)
    name = os.path.splitext(basename)[0]

    # Parse date from filename (first 8 characters = YYYYMMDD)
    try:
        acq_date = datetime.strptime(name[:8], "%Y%m%d").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Could not parse date for {basename}, setting as 'unknown'")
        acq_date = "unknown"

    layer = QgsRasterLayer(raster_path, name)
    if not layer.isValid():
        print(f"Invalid raster skipped: {raster_path}")
        continue

    extent = layer.extent()
    centroid = extent.center()

    # Create memory layer with attributes: filename, acq_date
    point_layer = QgsVectorLayer("Point?crs=" + layer.crs().authid(), name + "_centroid", "memory")
    prov = point_layer.dataProvider()
    prov.addAttributes([
        QgsField("filename", QVariant.String),
        QgsField("acq_date", QVariant.String)
    ])
    point_layer.updateFields()

    # Add the centroid point
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(centroid)))
    feat.setAttributes([name, acq_date])
    prov.addFeatures([feat])
    point_layer.updateExtents()

    centroid_layers.append(point_layer)

# Step 3: Save all centroid layers to disk and merge
saved_layers = []
for lyr in centroid_layers:
    out_path = os.path.join(QgsProject.instance().homePath(), lyr.name() + ".gpkg")
    QgsVectorFileWriter.writeAsVectorFormat(lyr, out_path, "UTF-8", lyr.crs(), "GPKG")
    saved_layers.append(out_path + "|layername=" + lyr.name())

processing.run("native:mergevectorlayers", {
    'LAYERS': saved_layers,
    'CRS': centroid_layers[0].crs(),
    'OUTPUT': output_shapefile
})

print(f"✅ Done! Centroids with acquisition dates saved to: {output_shapefile}")
