from pathlib import Path
import csv
import calendar
from collections import defaultdict
from qgis.core import QgsVectorLayer, QgsRasterLayer
import processing

# === Directories ===
raster_dir = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\preppedcropscape")
firepoints_root = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_seusa")
output_dir = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\seusa-new\geos\croptype-fc-frp-geos")
output_dir.mkdir(parents=True, exist_ok=True)

# === Refined Crop Code Dictionary ===
crop_code_to_name = {
    1: "Corn", 2: "Cotton", 3: "Rice", 4: "Sorghum", 5: "Soybeans", 6: "Sunflower",
    10: "Peanuts", 11: "Tobacco", 12: "Sweet Corn", 13: "Pop or Orn Corn", 14: "Mint",
    21: "Barley", 22: "Durum Wheat", 23: "Spring Wheat", 24: "Winter Wheat", 25: "Other Small Grains",
    26: "Dbl Crop WinWht/Soybeans", 27: "Rye", 28: "Oats", 29: "Millet", 30: "Speltz",
    31: "Canola", 32: "Flaxseed", 33: "Safflower", 34: "Rape Seed", 35: "Mustard",
    36: "Alfalfa", 37: "Other Hay/Non Alfalfa", 38: "Camelina", 39: "Buckwheat",
    41: "Sugarbeets", 42: "Dry Beans", 43: "Potatoes", 44: "Other Crops", 45: "Sugarcane",
    46: "Sweet Potatoes", 47: "Misc Vegs & Fruits", 48: "Watermelons", 49: "Onions",
    50: "Cucumbers", 51: "Chick Peas", 52: "Lentils", 53: "Peas", 54: "Tomatoes",
    55: "Caneberries", 56: "Hops", 57: "Herbs", 58: "Clover/Wildflowers", 59: "Sod/Grass Seed",
    60: "Switchgrass", 61: "Fallow/Idle Cropland", 66: "Cherries", 67: "Peaches",
    68: "Apples", 69: "Grapes", 176: "Grass/Pasture", 204: "Pistachios", 205: "Triticale",
    206: "Carrots", 207: "Asparagus", 208: "Garlic", 209: "Cantaloupes", 210: "Prunes",
    211: "Olives", 212: "Oranges", 213: "Honeydew Melons", 214: "Broccoli", 215: "Avocados",
    216: "Peppers", 217: "Pomegranates", 218: "Nectarines", 219: "Greens", 220: "Plums",
    221: "Strawberries", 222: "Squash", 223: "Apricots", 224: "Vetch", 225: "Dbl Crop WinWht/Corn",
    226: "Dbl Crop Oats/Corn", 227: "Lettuce", 228: "Dbl Crop Triticale/Corn", 229: "Pumpkins",
    230: "Dbl Crop Lettuce/Durum Wht", 231: "Dbl Crop Lettuce/Cantaloupe", 232: "Dbl Crop Lettuce/Cotton",
    233: "Dbl Crop Lettuce/Barley", 234: "Dbl Crop Durum Wht/Sorghum", 235: "Dbl Crop Barley/Sorghum",
    236: "Dbl Crop WinWht/Sorghum", 237: "Dbl Crop Barley/Corn", 238: "Dbl Crop WinWht/Cotton",
    239: "Dbl Crop Soybeans/Cotton", 240: "Dbl Crop Soybeans/Oats", 241: "Dbl Crop Corn/Soybeans",
    242: "Blueberries", 243: "Cabbage", 244: "Cauliflower", 245: "Celery", 246: "Radishes",
    247: "Turnips", 248: "Eggplants", 249: "Gourds", 250: "Cranberries", 254: "Dbl Crop Barley/Soybeans"
}

# === Summary Stores ===
sensor_crop_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0.0])))))

# === Process Each Fire File ===
for shp_path in firepoints_root.rglob("*.shp"):
    print(f"🔄 {shp_path.name}")
    filename = shp_path.stem.lower()
    parts = filename.split("_")
    if len(parts) != 4:
        print(f"⚠️ Skipping malformed filename: {filename}")
        continue

    state_name = parts[0]
    year = int(parts[1])
    month = int(parts[2])
    raster_path = raster_dir / f"{state_name}_cdl_{year}.tif"
    if not raster_path.exists():
        print(f"❌ Missing raster: {raster_path.name}")
        continue

    fire_layer = QgsVectorLayer(str(shp_path), "fire", "ogr")
    raster_layer = QgsRasterLayer(str(raster_path), "crop")
    if not fire_layer.isValid() or not raster_layer.isValid():
        print(f"❌ Invalid layer(s) in {shp_path.name}")
        continue

    result = processing.run("native:rastersampling", {
        'INPUT': str(shp_path),
        'RASTERCOPY': str(raster_path),
        'COLUMN_PREFIX': 'crop_',
        'OUTPUT': 'memory:'
    })
    sampled_layer = result['OUTPUT']

    for feat in sampled_layer.getFeatures():
        frp = feat['FRP']
        if frp is None or frp == -999.0:
            continue

        crop_code = feat['crop_1'] if feat['crop_1'] is not None else -1
        sensor = feat['Satellite'] if 'Satellite' in feat.fields().names() else "Unknown"
        method = feat['Method'] if 'Method' in feat.fields().names() else "Unknown"

        if sensor not in ["GOES-EAST", "GOES-WEST"]:
            continue

        stats = sensor_crop_stats[state_name][(year, month)][sensor][crop_code][method]
        stats[0] += 1
        stats[1] += frp

    print(f"✅ Done: {shp_path.name}")

# === Write Monthly Summary CSVs ===
all_rows = []
for state_name, year_month_data in sensor_crop_stats.items():
    out_csv = output_dir / f"{state_name}_geos_summary.csv"
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "State", "Year", "Month", "Month Name", "Sensor", "Method",
            "Crop Code", "Crop Name", "Fire Count", "FRP_SUM", "FRP_MEAN"
        ])

        for (year, month), sensor_data in year_month_data.items():
            month_name = calendar.month_name[month]
            for sensor, crop_data in sensor_data.items():
                for crop_code, method_data in crop_data.items():
                    for method, (count, frp_sum) in method_data.items():
                        crop_name = crop_code_to_name.get(crop_code, "Unknown")
                        frp_mean = round(frp_sum / count, 2) if count > 0 else 0
                        row = [
                            state_name, year, month, month_name, sensor, method,
                            crop_code, crop_name, count, round(frp_sum, 2), frp_mean
                        ]
                        writer.writerow(row)
                        all_rows.append(row)
    print(f"📁 Saved: {out_csv.name}")

# === Write Yearly Summary CSVs ===
for state_name, year_month_data in sensor_crop_stats.items():
    yearly_data = defaultdict(list)

    for (year, month), sensor_data in year_month_data.items():
        month_name = calendar.month_name[month]
        for sensor, crop_data in sensor_data.items():
            for crop_code, method_data in crop_data.items():
                for method, (count, frp_sum) in method_data.items():
                    crop_name = crop_code_to_name.get(crop_code, "Unknown")
                    frp_mean = round(frp_sum / count, 2) if count > 0 else 0
                    row = [
                        state_name, year, month, month_name, sensor, method,
                        crop_code, crop_name, count, round(frp_sum, 2), frp_mean
                    ]
                    yearly_data[year].append(row)

    for year, rows in yearly_data.items():
        out_csv = output_dir / f"{state_name}_{year}_geos_summary.csv"
        with open(out_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "State", "Year", "Month", "Month Name", "Sensor", "Method",
                "Crop Code", "Crop Name", "Fire Count", "FRP_SUM", "FRP_MEAN"
            ])
            writer.writerows(rows)
        print(f"📁 Saved: {out_csv.name}")

# === Write Mega Summary CSV ===
mega_csv = output_dir / "all_states_geos_summary.csv"
with open(mega_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "State", "Year", "Month", "Month Name", "Sensor", "Method",
        "Crop Code", "Crop Name", "Fire Count", "FRP_SUM", "FRP_MEAN"
    ])
    writer.writerows(all_rows)
print(f"📦 Saved mega summary: {mega_csv.name}")
