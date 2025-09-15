import glob, pathlib
from pathlib import Path
import processing

c = 'philippines'

firespath = r"D:\WORK September 2022\seag\data\himawari_daily_agriculture_fires\{}".format(c)
fires = glob.glob(str(firespath)+"/*shp")

result = {}

for f in fires:
    
    date = Path(f).stem.split('_')[1]
    layer = QgsVectorLayer(f, '', 'ogr')
    
    count = layer.aggregate(QgsAggregateCalculator.Sum, "N")[0]
    
    result[date] = count
    
print(*sorted(result, key=result.get, reverse=True)[:10], sep='\n')
    