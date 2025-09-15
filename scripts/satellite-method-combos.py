from pathlib import Path
import pandas as pd
from qgis.core import QgsVectorLayer

# === Input Directory ===
firepoints_root = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_seusa")

# === Collect Unique Satellite–Method Combos ===
satellite_method_combos = set()

for shp_path in firepoints_root.rglob("*.shp"):
    layer = QgsVectorLayer(str(shp_path), "fire", "ogr")
    if not layer.isValid():
        continue

    for feat in layer.getFeatures():
        sat = feat['Satellite'] if 'Satellite' in feat.fields().names() else None
        method = feat['Method'] if 'Method' in feat.fields().names() else None
        if sat and method:
            satellite_method_combos.add((sat, method))

# === Create DataFrame ===
combo_df = pd.DataFrame(sorted(satellite_method_combos), columns=["Satellite", "Method"])

# === Output CSV Path ===
output_csv = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\seusa-new\satellite_method_combinations.csv")

# === Save to CSV ===
combo_df.to_csv(output_csv, index=False)

print(f"✅ Saved: {output_csv}")
