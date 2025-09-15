import os
import csv

def get_unique_and_common_tif_files(dir1, dir2):
    # Get .tif files from dir1 (non-recursive)
    files1 = {
        f for f in os.listdir(dir1)
        if os.path.isfile(os.path.join(dir1, f)) and f.endswith('.tif')
    }

    # Recursively get all .tif files from dir2
    files2 = set()
    for root, _, files in os.walk(dir2):
        for f in files:
            if f.endswith('.tif'):
                files2.add(f)

    # Compare sets
    common_files = sorted(files1 & files2)
    unique_to_dir1 = sorted(files1 - files2)

    print(f"Common files: {len(common_files)}")
    print(f"Unique to {dir1}: {len(unique_to_dir1)}")

    # Save to CSV
    with open('common_files.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Common_Files'])
        for item in common_files:
            writer.writerow([item])

    with open('unique_to_dir1.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Unique_Files_Dir1'])
        for item in unique_to_dir1:
            writer.writerow([item])

    return unique_to_dir1, common_files

# Example usage
dir1 = r"C:\Users\aeaturu\Desktop\WORK April 2025\planet data download status\Downloaded_AnalyticMS_SR_Files"
dir2 = r"E:\Planet Data"

unique_files, common_files = get_unique_and_common_tif_files(dir1, dir2)
