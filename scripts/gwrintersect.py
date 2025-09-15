import glob
from pathlib import Path
import processing
from qgis.core import QgsVectorLayer

filepath = r"F:\WORK February 2025\adityaeaturu-forestpopulationcovernepal\shapefiles\results"
files = glob.glob(filepath + "/*result.shp")

# Ensure the files are sorted correctly (Optional)
files.sort()

# Load the 2000 layer
layer_2000 = files[0]  # Modify if needed

# Calculate centroids
centroids = processing.run("native:centroids", {
    'INPUT': layer_2000,
    'ALL_PARTS': True,
    'OUTPUT': 'memory:'
})['OUTPUT']

# Create spatial index
processing.run("native:createspatialindex", {'INPUT': centroids})

# Join attributes by location (2000)
joined_2000 = processing.run("native:joinattributesbylocation", {
    'INPUT': centroids,
    'JOIN': files[0],  # Should this be files[1] instead?
    'PREDICATE': [0, 1, 2, 3, 4, 5], 
    'JOIN_FIELDS': ['LOCALR2'],
    'METHOD': 1,
    'DISCARD_NONMATCHING': True,
    'PREFIX': '2000_',
    'OUTPUT': 'memory:'
})['OUTPUT']

processing.run("native:createspatialindex", {'INPUT': joined_2000})

# Join attributes by location (2005)
joined_2005 = processing.run("native:joinattributesbylocation", {
    'INPUT': joined_2000,
    'JOIN': files[1],  # Should be the 2005 file
    'PREDICATE': [0],
    'JOIN_FIELDS': ['LOCALR2'],
    'METHOD': 1,
    'DISCARD_NONMATCHING': True,
    'PREFIX': '2005_',
    'OUTPUT': 'memory:'
})['OUTPUT']

processing.run("native:createspatialindex", {'INPUT': joined_2005})

# Join attributes by location (2010)
joined_2010 = processing.run("native:joinattributesbylocation", {
    'INPUT': joined_2005,
    'JOIN': files[2],  # Should be the 2010 file
    'PREDICATE': [0],
    'JOIN_FIELDS': ['LOCALR2'],
    'METHOD': 1,
    'DISCARD_NONMATCHING': True,
    'PREFIX': '2010_',
    'OUTPUT': 'memory:'
})['OUTPUT']

processing.run("native:createspatialindex", {'INPUT': joined_2010})

# Join attributes by location (2015)
joined_2015 = processing.run("native:joinattributesbylocation", {
    'INPUT': joined_2010,
    'JOIN': files[3],  # Should be the 2015 file
    'PREDICATE': [0],
    'JOIN_FIELDS': ['LOCALR2'],
    'METHOD': 1,
    'DISCARD_NONMATCHING': True,
    'PREFIX': '2015_',
    'OUTPUT': 'memory:'
})['OUTPUT']

processing.run("native:createspatialindex", {'INPUT': joined_2015})

# Join attributes by location (2020)
joined_2020 = processing.run("native:joinattributesbylocation", {
    'INPUT': joined_2015,
    'JOIN': files[4],  # Should be the 2020 file
    'PREDICATE': [0],
    'JOIN_FIELDS': ['LOCALR2'],
    'METHOD': 1,
    'DISCARD_NONMATCHING': True,
    'PREFIX': '2020_',
    'OUTPUT': 'memory:'
})['OUTPUT']

# Create a list of the fieldnames you want to delete:
fieldnames_to_delete = ['field_a','field_c']
# Enter Edit mode
with edit(joined_2020):
    # Create empty list we will fill with the fieldindexes
    fields_to_delete = []
    # Iterate over the list of fieldnames and get the indexes
    for fieldname_to_delete in fieldnames_to_delete:
        # Get the field index by its name:
        fieldindex_to_delete = my_vectorlayer.fields().indexFromName(fieldname_to_delete)
        # You can also check if the field exists
        if fieldindex_to_delete == -1:
            # If it does not exist, just skip it and go to the next one. This may prevent a crash or error :)
            continue
        # Append the index to the list
        fields_to_delete.append(fieldindex_to_delete)
    # Delete the fields by their indexes, note that it has to be a list:
    my_vectorlayer.dataProvider().deleteAttributes(fields_to_delete)
# Update the fields, so the changes are recognized:
my_vectorlayer.updateFields()
