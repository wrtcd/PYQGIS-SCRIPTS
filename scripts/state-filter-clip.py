import glob
from pathlib import Path
import processing

# 📂 Input fire shapefiles (already yearly)
firesdir = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_yearly"
fires = glob.glob(firesdir + "/*.shp")

# 📍 SEUSA unified boundary
boundary_path = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\shapefiles\boundary.shp"
boundary_layer = QgsVectorLayer(boundary_path, '', 'ogr')

# 📂 Output folder
outdir = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\fire app\data")
outdir.mkdir(parents=True, exist_ok=True)

for fire in fires:
    firelayer = QgsVectorLayer(fire, '', 'ogr')

    # ✅ Extract year from filename
    stem = Path(fire).stem  # e.g., 'hms_fire2012'
    year = ''.join(filter(str.isdigit, stem))  # safely extract '2012'

    if len(year) != 4:
        print(f"⚠️ Skipping file with unexpected name: {fire}")
        continue

    # ✅ Filter GOES-only
    firelayer.setSubsetString('"SATELLITE" IN (\'GOES-EAST\', \'GOES-WEST\')')

    # ✅ Define output filename
    clipped_path = str(outdir / f"SEUSA_{year}_GOES_HMS.shp")

    print(f"Clipping {stem} → {clipped_path}")

    # Clip to SEUSA boundary
    processing.run("native:clip", {
        'INPUT': firelayer,
        'OVERLAY': boundary_layer,
        'OUTPUT': clipped_path
    })
