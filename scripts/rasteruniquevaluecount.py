import glob
import processing
import csv
from pathlib import Path
from qgis.core import QgsRasterLayer

rastersdir = r"D:\WORK March 2025\march 26 presentation\lossyears\count"
rasterspath = glob.glob(rastersdir + "/*.tif")

values = {}

for r in rasterspath:
    rlayer = QgsRasterLayer(r, '')

    # Ensure the raster layer is valid
    if not rlayer.isValid():
        print(f"Invalid raster layer: {r}")
        continue

    year = Path(r).stem  # Extract year from filename, e.g., 'loss_2001.tif'

    parameters = {
        'INPUT': rlayer,
        'BAND': 1,
        'OUTPUT_TABLE': 'TEMPORARY_OUTPUT'
    }

    try:
        uniquevalues = processing.run("native:rasterlayeruniquevaluesreport", parameters)
        report = uniquevalues['OUTPUT_TABLE']
        
        features = report.getFeatures()
        for i, f in enumerate(features):  
            if i == 1:  # Get the second unique value (index 1)
                attrs = f.attributes()
                value = attrs[1]  # Assuming second column holds the count
                values[year] = value
                break  # Only need the second value
    except Exception as e:
        print(f"Error processing {r}: {e}")

# Export dictionary to CSV
csv_filename = r"D:\WORK March 2025\march 26 presentation\lossyears\count\pixelvalues.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Year", "Value"])  # Header row
    for year in sorted(values.keys()):
        writer.writerow([year, values[year]])

print(f"CSV export completed: {csv_filename}")
