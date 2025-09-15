import os
import csv
import processing

# Paths
csv_path = r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\raster_paths.csv"
output_folder = r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\uniqueextents"
os.makedirs(output_folder, exist_ok=True)

# Read CSV and loop through rasters
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        raster_path = row["raster_path"]
        if not os.path.exists(raster_path):
            print(f"File not found: {raster_path}")
            continue

        raster_name = os.path.splitext(os.path.basename(raster_path))[0]
        output_shapefile = os.path.join(output_folder, f"{raster_name}_extent.shp")

        # Run 'qgis:polygonfromlayerextent'
        try:
            result = processing.run(
                "qgis:polygonfromlayerextent",
                {
                    'INPUT': raster_path,
                    'OUTPUT': output_shapefile
                }
            )
            print(f"Saved extent: {output_shapefile}")
        except Exception as e:
            print(f"Failed to process {raster_path}: {e}")
