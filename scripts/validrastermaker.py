import os
from qgis.core import QgsProcessingFeedback
import processing

# Set input and output folder paths
input_folder = r'D:\WORK March 2025\march 26 presentation\treecover-new\validpixelcount'
output_folder = r'D:\WORK March 2025\march 26 presentation\treecover-new\validpixelcount\processed_datasets'

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.tif'):
        input_raster_path = os.path.join(input_folder, filename)
        output_raster_path = os.path.join(output_folder, f'gt0_{filename}')
        
        # Load the raster
        raster_layer = QgsRasterLayer(input_raster_path, filename)
        if not raster_layer.isValid():
            print(f"Invalid raster: {filename}")
            continue

        # Prepare raster calculator entry
        raster_entry = QgsRasterCalculatorEntry()
        raster_entry.ref = 'raster@1'
        raster_entry.raster = raster_layer
        raster_entry.bandNumber = 1
        
        entries = [raster_entry]

        # Raster Calculator Expression: if raster > 0, then 1, else 0
        expression = '(raster@1 > 0) * 1'

        # Create the Raster Calculator object
        calc = QgsRasterCalculator(
            expression,
            output_raster_path,
            'GTiff',
            raster_layer.extent(),
            raster_layer.width(),
            raster_layer.height(),
            entries
        )

        # Run the calculation
        result = calc.processCalculation()
        if result == 0:
            print(f"Processed: {filename}")
        else:
            print(f"Failed: {filename}")

print("All done.")
