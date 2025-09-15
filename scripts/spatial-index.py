from pathlib import Path
import processing

# Root directory with subfolders
root_dir = Path(r"C:\Users\aeaturu\Desktop\WORK May 2025\gridded fires\fires")

# Find all .shp files recursively
shapefiles = list(root_dir.rglob("*.shp"))

for shp_path in shapefiles:
    layer = QgsVectorLayer(str(shp_path), '', 'ogr')

    if layer.isValid():
        layer.dataProvider().createSpatialIndex()
        print(f"Spatial index created for: {shp_path.name}")
    else:
        print(f"Invalid layer: {shp_path.name}")
