from pathlib import Path
import csv
from collections import defaultdict
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsPointXY
import processing
import calendar

# === Directories ===
raster_dir = Path(r"C:\Users\aeaturu\Desktop\WORK March 2025\Southeast USA Data Download\VIIRS NASA FIRMS\preppedcropscape")
firepoints_root = Path(r"C:\Users\aeaturu\Desktop\WORK March 2025\Southeast USA Data Download\VIIRS NASA FIRMS\preppedfiredataset\monthlyfires")
output_dir = Path(r"C:\Users\aeaturu\Desktop\WORK March 2025\Southeast USA Data Download\VIIRS NASA FIRMS\croptype-fc-frp")
output_dir.mkdir(parents=True, exist_ok=True)

# === Full Crop Code to Name Mapping (0–255) ===
crop_code_to_name = {i: "Unknown" for i in range(256)}
crop_code_to_name.update({
    0: "Background", 1: "Corn", 2: "Cotton", 3: "Rice", 4: "Sorghum", 5: "Soybeans",
    6: "Sunflower", 10: "Peanuts", 11: "Tobacco", 12: "Sweet Corn", 13: "Pop or Orn Corn",
    14: "Mint", 21: "Barley", 22: "Durum Wheat", 23: "Spring Wheat", 24: "Winter Wheat",
    25: "Other Small Grains", 26: "Dbl Crop WinWht/Soybeans", 27: "Rye", 28: "Oats",
    29: "Millet", 30: "Speltz", 31: "Canola", 32: "Flaxseed", 33: "Safflower",
    34: "Rape Seed", 35: "Mustard", 36: "Alfalfa", 37: "Other Hay/Non Alfalfa",
    38: "Camelina", 39: "Buckwheat", 41: "Sugarbeets", 42: "Dry Beans", 43: "Potatoes",
    44: "Other Crops", 45: "Sugarcane", 46: "Sweet Potatoes", 47: "Misc Vegs & Fruits",
    48: "Watermelons", 49: "Onions", 50: "Cucumbers", 51: "Chick Peas", 52: "Lentils",
    53: "Peas", 54: "Tomatoes", 55: "Caneberries", 56: "Hops", 57: "Herbs",
    58: "Clover/Wildflowers", 59: "Sod/Grass Seed", 60: "Switchgrass",
    61: "Fallow/Idle Cropland", 63: "Forest", 64: "Shrubland", 65: "Barren",
    66: "Cherries", 67: "Peaches", 68: "Apples", 69: "Grapes", 70: "Christmas Trees",
    71: "Other Tree Crops", 72: "Citrus", 74: "Pecans", 75: "Almonds", 76: "Walnuts",
    77: "Pears", 81: "Clouds/No Data", 82: "Developed", 83: "Water", 87: "Wetlands",
    88: "Nonag/Undefined", 92: "Aquaculture", 111: "Open Water", 112: "Perennial Ice/Snow",
    121: "Developed/Open Space", 122: "Developed/Low Intensity",
    123: "Developed/Med Intensity", 124: "Developed/High Intensity", 131: "Barren",
    141: "Deciduous Forest", 142: "Evergreen Forest", 143: "Mixed Forest",
    152: "Shrubland", 176: "Grass/Pasture", 190: "Woody Wetlands",
    195: "Herbaceous Wetlands", 204: "Pistachios", 205: "Triticale", 206: "Carrots",
    207: "Asparagus", 208: "Garlic", 209: "Cantaloupes", 210: "Prunes", 211: "Olives",
    212: "Oranges", 213: "Honeydew Melons", 214: "Broccoli", 215: "Avocados",
    216: "Peppers", 217: "Pomegranates", 218: "Nectarines", 219: "Greens",
    220: "Plums", 221: "Strawberries", 222: "Squash", 223: "Apricots", 224: "Vetch",
    225: "Dbl Crop WinWht/Corn", 226: "Dbl Crop Oats/Corn", 227: "Lettuce",
    228: "Dbl Crop Triticale/Corn", 229: "Pumpkins", 230: "Dbl Crop Lettuce/Durum Wht",
    231: "Dbl Crop Lettuce/Cantaloupe", 232: "Dbl Crop Lettuce/Cotton",
    233: "Dbl Crop Lettuce/Barley", 234: "Dbl Crop Durum Wht/Sorghum",
    235: "Dbl Crop Barley/Sorghum", 236: "Dbl Crop WinWht/Sorghum",
    237: "Dbl Crop Barley/Corn", 238: "Dbl Crop WinWht/Cotton",
    239: "Dbl Crop Soybeans/Cotton", 240: "Dbl Crop Soybeans/Oats",
    241: "Dbl Crop Corn/Soybeans", 242: "Blueberries", 243: "Cabbage",
    244: "Cauliflower", 245: "Celery", 246: "Radishes", 247: "Turnips",
    248: "Eggplants", 249: "Gourds", 250: "Cranberries", 254: "Dbl Crop Barley/Soybeans"
})

# === Store summaries ===
state_summaries = defaultdict(list)

# === Process each shapefile ===
for shp_path in firepoints_root.rglob("*.shp"):
    print(f"🔄 Iterating: {shp_path.name}")
    filename = shp_path.stem.lower()
    parts = filename.split("_")

    if len(parts) != 3:
        print(f"⚠️ Skipping malformed filename: {filename}")
        continue

    state_name = parts[0]
    year = int(parts[1])
    month = int(parts[2])
    month_name = calendar.month_name[month]

    raster_path = raster_dir / f"{parts[0]}_cdl_{year}.tif"
    if not raster_path.exists():
        print(f"❌ Raster not found: {raster_path.name}")
        continue

    fire_layer = QgsVectorLayer(str(shp_path), "Fire", "ogr")
    raster_layer = QgsRasterLayer(str(raster_path), "Crop")

    if not fire_layer.isValid() or not raster_layer.isValid():
        print(f"⚠️ Invalid layers: {filename}")
        continue

    stats = {}

    result = processing.run("native:rastersampling", {
        'INPUT': str(shp_path),
        'RASTERCOPY': str(raster_path),
        'COLUMN_PREFIX': 'crop_',
        'OUTPUT': 'memory:'
    })
    sampled_layer = result['OUTPUT']

    for feat in sampled_layer.getFeatures():
        crop_code = feat['crop_1'] if feat['crop_1'] is not None else -1
        frp = feat['FRP'] if feat['FRP'] is not None else 0

        if crop_code not in stats:
            stats[crop_code] = [0, 0.0]

        stats[crop_code][0] += 1
        stats[crop_code][1] += frp

    for code, (count, frp_sum) in stats.items():
        crop_name = crop_code_to_name.get(code, "Unknown")
        frp_mean = frp_sum / count if count > 0 else 0
        state_summaries[state_name].append([
            state_name, year, month, month_name, code, crop_name,
            count, round(frp_sum, 2), round(frp_mean, 2)
        ])

    print(f"✅ Processed: {filename}")

# === Split summaries per state and year ===
state_year_summaries = defaultdict(lambda: defaultdict(list))
for state_name, rows in state_summaries.items():
    for row in rows:
        year = row[1]
        state_year_summaries[state_name][year].append(row)

# === Save files ===
for state_name, yearly_data in state_year_summaries.items():
    all_rows = []
    for year_rows in yearly_data.values():
        all_rows.extend(year_rows)

    state_csv = output_dir / f"{state_name.replace(' ', '_')}_viirs_summary.csv"
    with open(state_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "State", "Year", "Month", "Month Name", "Crop Code", "Description",
            "Fire Count", "FRP_SUM", "FRP_MEAN"
        ])
        writer.writerows(all_rows)
    print(f"📁 Saved full summary: {state_csv.name}")

    for year, rows in yearly_data.items():
        year_csv = output_dir / f"{state_name.replace(' ', '_')}_{year}_viirs_summary.csv"
        with open(year_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "State", "Year", "Month", "Month Name", "Crop Code", "Description",
                "Fire Count", "FRP_SUM", "FRP_MEAN"
            ])
            writer.writerows(rows)
        print(f"📁 Saved yearly summary: {year_csv.name}")

# === Combine all into one mega summary ===
mega_summary = []
for state_rows in state_summaries.values():
    mega_summary.extend(state_rows)

mega_csv = output_dir / "all_states_viirs_summary.csv"
with open(mega_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "State", "Year", "Month", "Month Name", "Crop Code", "Description",
        "Fire Count", "FRP_SUM", "FRP_MEAN"
    ])
    writer.writerows(mega_summary)

print(f"📦 Saved mega summary: {mega_csv.name}")
