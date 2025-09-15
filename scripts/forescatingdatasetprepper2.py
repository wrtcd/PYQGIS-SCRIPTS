import os
import geopandas as gpd

# === USER INPUT ===
SOURCE_DIR = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\VIIRS NASA FIRMS\preppedfiredataset\monthlyfires\alabama"
CLIP_SHAPEFILE = r"C:\Users\aeaturu\Desktop\USA Datasets\Temporal AI Model for South Alabama\southerndistrict.shp"
DEST_DIR = r"C:\Users\aeaturu\Desktop\USA Datasets\Temporal AI Model for South Alabama\southerndistrictfires"

# === Load Clip Geometry ===
clip_gdf = gpd.read_file(CLIP_SHAPEFILE)
clip_crs = clip_gdf.crs  # Store CRS to reproject fire points

# === Loop through years and months ===
for year in range(2012, 2025):
    src_year_folder = os.path.join(SOURCE_DIR, str(year))
    dest_year_folder = os.path.join(DEST_DIR, str(year))
    os.makedirs(dest_year_folder, exist_ok=True)

    for month in range(1, 13):
        filename = f"alabama_{year}_{month:02d}.shp"
        input_path = os.path.join(src_year_folder, filename)
        output_filename = f"southerndistrict_{year}_{month:02d}.shp"
        output_path = os.path.join(dest_year_folder, output_filename)

        if os.path.exists(input_path):
            try:
                gdf = gpd.read_file(input_path)
                gdf = gdf.to_crs(clip_crs)  # Match CRS
                clipped = gpd.clip(gdf, clip_gdf)

                if len(clipped) > 0:
                    clipped.to_file(output_path)
                    print(f"✅ Saved: {output_path} ({len(clipped)} points)")
                else:
                    print(f"⚠️ Empty after clip: {filename}")
            except Exception as e:
                print(f"❌ Error clipping {filename}: {e}")
        else:
            print(f"🚫 Missing: {input_path}")
