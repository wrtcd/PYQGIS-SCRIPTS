import glob
from pathlib import Path
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem, QgsSpatialIndex
import processing
import os

# Define year and country
year = '2000'
country = 'nepal'

print(f"\n=== Starting Process for Year: {year}, Country: {country} ===\n")

# Define the directory path
directory = Path(r"D:\WORK March 2025\march 26 presentation\treecover-new")
files = glob.glob(str(directory) + "/*.tif")

# Identify the forest and population rasters
forestpath = [item for item in files if 'TreeCover_{}'.format(year) in item][0]
populationpath = [item for item in files if 'Population_{}'.format(year) in item][0]

# Debug: Print paths and check file existence
print(f"Forest Raster Path: {forestpath}")
print(f"Population Raster Path: {populationpath}")
print(f"Forest Exists: {os.path.exists(forestpath)}")
print(f"Population Exists: {os.path.exists(populationpath)}")

# Load the rasters as QgsRasterLayer objects
forest = QgsRasterLayer(forestpath, 'forest')
population = QgsRasterLayer(populationpath, 'population')

# Debug: Check raster validity
print(f"Forest Valid: {forest.isValid()}")
print(f"Population Valid: {population.isValid()}")

if not forest.isValid() or not population.isValid():
    raise Exception("One or both input rasters are invalid! Check file paths and formats.")

print("Successfully loaded input rasters.\n")

# Define raster calculator entries
fentry = QgsRasterCalculatorEntry()
fentry.ref = 'forest@1'
fentry.raster = forest
fentry.bandNumber = 1

pentry = QgsRasterCalculatorEntry()
pentry.ref = 'population@1'
pentry.raster = population
pentry.bandNumber = 1

# Define the raster calculator expression for valid pixels (exclude 0 as NoData)
expression = '(forest@1 > 0) AND (population@1 > 0)'

# Save the raster calculation to a temporary file
valid_pixels_raster_path = str(directory.joinpath(f"{country}_validpixels_{year}.tif"))
print(f"Temporary raster path for valid pixels: {valid_pixels_raster_path}\n")

calculator = QgsRasterCalculator(
    expression,
    valid_pixels_raster_path,  # Save as a temporary file
    'GTiff',
    forest.extent(),
    forest.width(),
    forest.height(),
    [fentry, pentry]
)

result = calculator.processCalculation()
if result != 0:
    raise Exception("Raster calculation failed.")

print("Raster calculation completed successfully.\n")

# Set 0 as NoData value in the output raster
print("=== Setting 0 as NoData Value ===\n")
nodata_raster = processing.run("gdal:translate", {
    'INPUT': valid_pixels_raster_path,
    'NODATA': 0,
    'COPY_SUBDATASETS': False,
    'OPTIONS': '',
    'DATA_TYPE': 0,
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

# Convert valid pixels raster to polygons
print("=== Converting Valid Pixels Raster to Polygons ===\n")
polygon_parameters = {
    'INPUT_RASTER': nodata_raster,  # Use the raster with NoData set to 0
    'RASTER_BAND': 1,
    'FIELD_NAME': 'VALUE',
    'OUTPUT': 'TEMPORARY_OUTPUT'
}

valid_pixels_polygon = processing.run("native:pixelstopolygons", polygon_parameters)
polygon_layer = valid_pixels_polygon['OUTPUT']

# Check if spatial index exists, create one if necessary
print("=== Checking/Creating Spatial Index for Polygon Layer ===\n")
polygon_layer.dataProvider().createSpatialIndex()
print("Spatial index created successfully for the polygon layer.")

# Create centroids from polygons
print("=== Creating Centroids from Polygons ===\n")
centroid_layer = processing.run("native:centroids", {
    'INPUT': polygon_layer,
    'ALL_PARTS': False,  # One centroid per polygon
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

# Add XY fields to centroids
print("=== Adding XY Fields to Centroids ===\n")
centroids_with_xy = processing.run("native:addxyfields", {
    'INPUT': centroid_layer,
    'CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
    'PREFIX': '',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

# Sample raster values at centroids
print("=== Sampling Raster Values ===\n")
forest_sampled = processing.run("native:rastersampling", {
    'INPUT': centroids_with_xy,   # Centroid layer with XY fields
    'RASTERCOPY': forestpath,  # Forest raster
    'COLUMN_PREFIX': 'forest',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

population_sampled = processing.run("native:rastersampling", {
    'INPUT': forest_sampled,      # Layer with forest values sampled
    'RASTERCOPY': populationpath, # Population raster
    'COLUMN_PREFIX': 'population',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

# Add spatial index to the `population_sampled` layer
print("=== Adding Spatial Index to Population Sampled Layer ===\n")
population_sampled.dataProvider().createSpatialIndex()
print("Spatial index created successfully for the population sampled layer.")

# Join attributes with the original polygon layer
print("=== Joining Attributes with Original Polygons ===\n")
joined_layer = processing.run("native:joinattributesbylocation", {
    'INPUT': polygon_layer,       # Sampled layer with raster values
    'JOIN': population_sampled,             # Original polygon layer
    'PREDICATE': [0, 1, 2, 3, 4, 5],                  # Intersect
    'JOIN_FIELDS': [],                 # Join all fields
    'METHOD': 1,                       # Keep all records
    'DISCARD_NONMATCHING': False,
    'PREFIX': '',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

# Clean up fields
print("=== Cleaning Fields ===\n")
final_layer = processing.run("qgis:deletecolumn", {
    'INPUT': joined_layer,
    'COLUMN': ['VALUE', 'VALUE_2'],  # Remove unnecessary fields
    'OUTPUT': 'TEMPORARY_OUTPUT'
})['OUTPUT']

# Refactor fields
print("=== Refactoring Fields ===\n")
output_path = str(directory.joinpath(f"{country}_gwr_{year}.shp"))

refactor_params = {
    'INPUT': final_layer,  # The cleaned layer
    'FIELDS_MAPPING': [
        {'expression': '"x"', 'length': 10, 'name': 'Longitude', 'precision': 6, 'type': 6},
        {'expression': '"y"', 'length': 10, 'name': 'Latitude', 'precision': 6, 'type': 6},
        {'expression': '"forest1"', 'length': 10, 'name': 'treecover%', 'precision': 2, 'type': 6},
        {'expression': '"population1"', 'length': 10, 'name': 'population', 'precision': 2, 'type': 6},
    ],
    'OUTPUT': output_path  # Save as shapefile in the specified directory
}

refactored_path = processing.run("native:refactorfields", refactor_params)['OUTPUT']

# Load the refactored layer from disk
refactored_layer = QgsProject.instance().addMapLayer(QgsVectorLayer(refactored_path, "{}_GWR_{}".format(country, year), "ogr"))

# Check if the layer is valid
if refactored_layer and refactored_layer.isValid():
    print(f"- Successfully added the refactored layer to the canvas.")
    print(f"- Saved output to: {output_path}")
    print("- Fields: Longitude, Latitude, ForestVal, PopulVal\n")
else:
    raise Exception(f"Failed to load the refactored layer from {output_path}")
