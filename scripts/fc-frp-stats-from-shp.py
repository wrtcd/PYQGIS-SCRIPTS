import glob
from pathlib import Path
import pandas as pd
from qgis.core import QgsVectorLayer, QgsAggregateCalculator

firedir = r"C:\Users\aeaturu\Desktop\WORK April 2025\aayushi - data download\clipped2"
fires = glob.glob(firedir + '/*.shp')
fires.sort()

df = pd.DataFrame(columns=['fcsum', 'frpmean', 'frpsum'])

for f in fires:
    layer = QgsVectorLayer(f, '', 'ogr')
    classnumber = Path(f).stem.split('_')[0]

    fcsum = layer.aggregate(QgsAggregateCalculator.Count, "VERSION")[0]
    frpmean = layer.aggregate(QgsAggregateCalculator.Mean, "FRP")[0]
    frpsum = layer.aggregate(QgsAggregateCalculator.Sum, "FRP")[0]

    df.loc[classnumber] = {'fcsum': fcsum, 'frpmean': frpmean, 'frpsum': frpsum}

df.to_csv(r"C:\Users\aeaturu\Desktop\WORK April 2025\aayushi - data download\fcfrp2.csv")
