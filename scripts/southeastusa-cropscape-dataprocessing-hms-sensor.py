from pathlib import Path
import csv
import calendar
from collections import defaultdict
from qgis.core import QgsVectorLayer, QgsRasterLayer
import processing

# === Directories ===
raster_dir = Path(r"C:\Users\aeaturu\Desktop\Southeast USA Data Download\preppedcropscape")
firepoints_root = Path(r"C:\Users\aeaturu\Desktop\hms_seusa")
output_dir = Path(r"C:\Users\aeaturu\Desktop\Southeast USA Data Download\croptype-fc-frp-hms-sensors")
output_dir.mkdir(parents=True, exist_ok=True)

# === Crop Code to Name Mapping (0–255) ===
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

# === Store: state → (year, month) → sensor → crop_code → [count, frp_sum]
sensor_crop_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0.0]))))

# === Process HMS fire shapefiles ===
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
        print(f"❌ Invalid layer(s): {shp_path.name}")
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

        stats = sensor_crop_stats[state_name][(year, month)][sensor][crop_code]
        stats[0] += 1
        stats[1] += frp

    print(f"✅ Done: {shp_path.name}")

# === Save to CSV ===
for state_name, year_month_data in sensor_crop_stats.items():
    out_csv = output_dir / f"{state_name}_sensor_crop_breakdown.csv"
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "State", "Year", "Month", "Month Name", "Sensor",
            "Crop Code", "Crop Name", "Fire Count", "FRP_SUM", "FRP_MEAN"
        ])

        for (year, month), sensor_data in year_month_data.items():
            month_name = calendar.month_name[month]
            for sensor, crop_data in sensor_data.items():
                for crop_code, (count, frp_sum) in crop_data.items():
                    crop_name = crop_code_to_name.get(crop_code, "Unknown")
                    frp_mean = round(frp_sum / count, 2) if count > 0 else 0
                    writer.writerow([
                        state_name, year, month, month_name, sensor,
                        crop_code, crop_name, count,
                        round(frp_sum, 2), frp_mean
                    ])
    print(f"📁 Saved: {out_csv.name}")
