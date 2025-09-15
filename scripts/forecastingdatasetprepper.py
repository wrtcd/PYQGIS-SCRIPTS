import os
import geopandas as gpd
import pandas as pd
from calendar import monthrange

# === USER INPUT ===
CLIPPED_DIR = r"C:\Users\aeaturu\Desktop\USA Datasets\Temporal AI Model for South Alabama\southerndistrictfires"
OUTPUT_CSV = r"C:\Users\aeaturu\Desktop\USA Datasets\Temporal AI Model for South Alabama\southerndistrict_monthly_fire_fc.csv"

records = []

for year in range(2012, 2025):
    year_folder = os.path.join(CLIPPED_DIR, str(year))
    
    for month in range(1, 13):
        shapefile_name = f"southerndistrict_{year}_{month:02d}.shp"
        shapefile_path = os.path.join(year_folder, shapefile_name)

        if os.path.exists(shapefile_path):
            try:
                gdf = gpd.read_file(shapefile_path)
                fire_count = len(gdf)  # count of fire points
                last_day = monthrange(year, month)[1]
                date = pd.to_datetime(f"{year}-{month:02d}-{last_day}")
                records.append({"DATE": date, "FCSUM": fire_count})
            except Exception as e:
                print(f"❌ Error reading {shapefile_path}: {e}")
        else:
            print(f"🚫 Missing: {shapefile_path}")

# === Save to CSV ===
df = pd.DataFrame(records)
df = df.sort_values("DATE")
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Saved time series to: {OUTPUT_CSV}")
