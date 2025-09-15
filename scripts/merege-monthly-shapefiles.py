import os
from collections import defaultdict
from qgis.core import QgsVectorLayer, QgsProcessingFeatureSourceDefinition
import processing

# 📁 Set your folder paths
input_folder = r"C:\Users\aeaturu\Desktop\HMS"
output_folder = r"C:\Users\aeaturu\Desktop\HMSFIRES"

# 🧠 Group files by year-month (e.g., "202201")
grouped_files = defaultdict(list)

for filename in os.listdir(input_folder):
    if filename.endswith(".shp") and filename.startswith("hms_fire"):
        date_part = filename.replace("hms_fire", "").replace(".shp", "")  # e.g., 20220104
        year_month = date_part[:6]  # Take YYYYMM
        full_path = os.path.join(input_folder, filename)
        grouped_files[year_month].append(full_path)

# 🔄 Merge shapefiles for each month
for year_month, shapefiles in grouped_files.items():
    print(f"Merging {len(shapefiles)} shapefiles for {year_month}...")

    # Set output path
    output_path = os.path.join(output_folder, f"hms_fire_{year_month}.shp")

    # Merge using QGIS native:mergevectorlayers
    processing.run("native:mergevectorlayers", {
        'LAYERS': shapefiles,
        'CRS': 'EPSG:4326',  # Change CRS if needed
        'OUTPUT': output_path
    })

    print(f"✅ Saved: {output_path}")
