import os
from qgis.core import (
    QgsVectorLayer, QgsField, QgsVectorFileWriter
)
import processing

# === USER INPUTS ===
grid_path = r"C:\Users\aeaturu\Desktop\USA Datasets\California Gridded Fires\grid.shp"
fire_data_base_path = r"C:\Users\aeaturu\Desktop\USA Datasets\California Gridded Fires\fires"
output_path = r"C:\Users\aeaturu\Desktop\USA Datasets\California Gridded Fires\2012_2024_CALIFORNIA_VIIRS_GRIDDED.shp"

# === Load Base Grid ===
grid_layer = QgsVectorLayer(grid_path, "grid", "ogr")
if not grid_layer.isValid():
    raise Exception("Grid layer failed to load.")

# === Add Output Fields to Grid Layer ===
grid_provider = grid_layer.dataProvider()
for year in range(2012, 2025):
    grid_provider.addAttributes([
        QgsField(f"{year}_FC", 6),                # Fire Count
        QgsField(f"{year}_FRP_S", 6, 'double'),   # FRP Sum
        QgsField(f"{year}_FRP_M", 6, 'double')    # FRP Mean
    ])
grid_layer.updateFields()

# === Loop Through Fire Data by Year ===
for year in range(2012, 2025):
    print(f"Processing {year}...")

    fire_folder = os.path.join(fire_data_base_path, str(year))
    fire_files = [f for f in os.listdir(fire_data_base_path) if f.endswith(f"{year}.shp") or f.endswith(f"{year}.gpkg")]
    if not fire_files:
        print(f" - No fire shapefile found for {year}, skipping.")
        continue

    fire_path = os.path.join(fire_data_base_path, fire_files[0])
    fire_layer = QgsVectorLayer(fire_path, f"fire_{year}", "ogr")
    if not fire_layer.isValid():
        print(f" - Failed to load fire layer for {year}, skipping.")
        continue

    # === Run Join by Location Summary (No PREFIX)
    result = processing.run("qgis:joinbylocationsummary", {
        'INPUT': grid_layer,
        'JOIN': fire_layer,
        'PREDICATE': [0, 1, 2, 3, 4, 5],  # are within
        'JOIN_FIELDS': ['FRP'],
        'SUMMARIES': [0, 5, 6],  # count, sum, mean
        'DISCARD_NONMATCHING': False,
        'OUTPUT': 'memory:'  # No prefix here
    })

    summary_layer = result['OUTPUT']

    # Standard QGIS field names
    count_field = "FRP_count"
    sum_field   = "FRP_sum"
    mean_field  = "FRP_mean"

    # Custom fields to write into
    fc_field        = f"{year}_FC"
    frp_sum_field   = f"{year}_FRP_S"
    frp_mean_field  = f"{year}_FRP_M"

    # === Write Attributes Back to Grid ===
    grid_layer.startEditing()
    for feat in summary_layer.getFeatures():
        fid = feat.id()
        grid_layer.changeAttributeValue(fid, grid_layer.fields().indexOf(fc_field), feat[count_field])
        grid_layer.changeAttributeValue(fid, grid_layer.fields().indexOf(frp_sum_field), feat[sum_field])
        grid_layer.changeAttributeValue(fid, grid_layer.fields().indexOf(frp_mean_field), feat[mean_field])
    grid_layer.commitChanges()

# === Save Final Output ===
QgsVectorFileWriter.writeAsVectorFormat(grid_layer, output_path, "utf-8", driverName="ESRI Shapefile")

print("✅ Done! Final joined grid saved to:")
print(output_path)
