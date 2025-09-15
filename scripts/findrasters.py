import os
import csv

def find_rasters(root_dir, keyword="AnalyticMS_SR", extension=".tif", output_csv="raster_paths.csv"):
    raster_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(extension) and keyword in file:
                full_path = os.path.join(dirpath, file)
                raster_paths.append(full_path)

    # Save to CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["raster_path"])
        for path in raster_paths:
            writer.writerow([path])
    
    print(f"Saved {len(raster_paths)} raster paths to {output_csv}")

# Example usage
find_rasters(r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\unique", output_csv="raster_paths.csv")
