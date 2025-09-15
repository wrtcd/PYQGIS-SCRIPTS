import os
from qgis.core import QgsVectorLayer, QgsProject, QgsFeatureRequest, QgsVectorFileWriter

# Define input shapefile path and output folder
input_shapefile = r'F:\WORK 2024 OCTOBER\adityaeaturu-deeplearninglandcovermapping\classes\trainingsamples.shp'  # Replace with your shapefile path
output_folder = r'F:\WORK 2024 OCTOBER\adityaeaturu-deeplearninglandcovermapping\classes\individualclassfiles'  # Replace with your desired output folder path

# Load the input shapefile
input_layer = QgsVectorLayer(input_shapefile, "input_layer", "ogr")

# Check if the input shapefile is valid
if not input_layer.isValid():
    print("Failed to load the input shapefile.")
else:
    print(f"Loaded shapefile: {input_layer.name()}")

    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the field with class values (replace 'LULC' with the correct field name)
    class_field_name = 'LULC'  # Replace with your class attribute name

    # Get unique class values from the input shapefile
    unique_values = set()
    for feature in input_layer.getFeatures():
        unique_values.add(feature[class_field_name])

    # Create a shapefile for each unique class
    for class_value in unique_values:
        # Set up the filter to get only the features with this class value
        request = QgsFeatureRequest().setFilterExpression(f'"{class_field_name}" = \'{class_value}\'')
        matching_features = input_layer.getFeatures(request)
        
        # Define the output path for this class
        output_path = os.path.join(output_folder, f"{input_layer.name()}_{class_value}.shp")
        
        # Create a new shapefile for this class value
        _writer = QgsVectorFileWriter.writeAsVectorFormat(
            input_layer,
            output_path,
            "utf-8",
            driverName="ESRI Shapefile",
            onlySelected=False,
            filter=QgsFeatureRequest().setFilterExpression(f'"{class_field_name}" = \'{class_value}\'')
        )
        
        # Check if the shapefile was created successfully
        if _writer == QgsVectorFileWriter.NoError:
            print(f"Shapefile created for class {class_value} at {output_path}")
        else:
            print(f"Error creating shapefile for class {class_value}")

