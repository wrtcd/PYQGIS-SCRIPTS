import os
import glob
import re
from pathlib import Path
import processing
from qgis.core import QgsProcessingFeedback

# Input and output directories
rastersdir = r"D:\WORK March 2025\march 26 presentation\dataset-treecover-downscaled"
outputdir = r"D:\WORK March 2025\march 26 presentation\treecover-downscaled-pairedoutputs"
os.makedirs(outputdir, exist_ok=True)

# Collect all rasters and pair them by year
raster_files = glob.glob(os.path.join(rastersdir, "*.tif"))
raster_dict = {}

for r in raster_files:
    name = Path(r).stem
    year_search = re.search(r'(\d{4})', name)
    if not year_search:
        print(f"No year found in {name}")
        continue
    year = year_search.group(1)

    if "pop" in name.lower():
        raster_dict.setdefault(year, {})['pop'] = r
    elif "tree" in name.lower():
        raster_dict.setdefault(year, {})['tree'] = r

feedback = QgsProcessingFeedback()

# Now process years where both pop and tree exist
for year, rasters in raster_dict.items():
    if 'pop' in rasters and 'tree' in rasters:
        pop_raster = rasters['pop']
        tree_raster = rasters['tree']
        output_raster = os.path.join(outputdir, f'pair_{year}.tif')

        # Formula: If both > 0, assign 1, else 0
        processing.run("gdal:rastercalculator", {
            'INPUT_A': pop_raster,
            'BAND_A': 1,
            'INPUT_B': tree_raster,
            'BAND_B': 1,
            'INPUT_C': None,
            'BAND_C': -1,
            'INPUT_D': None,
            'BAND_D': -1,
            'INPUT_E': None,
            'BAND_E': -1,
            'INPUT_F': None,
            'BAND_F': -1,
            'FORMULA': '(A > 0) * (B > 0)',
            'OUTPUT': output_raster,
            'RTYPE': 5  # Int32 output
        }, feedback=feedback)

        print(f"Processed year {year}: Output -> {output_raster}")

print("All done!")
