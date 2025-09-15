import glob, pathlib
from pathlib import Path

# subsetting yearly fires
path = r"F:\WORK August 2022\drought-fires\countries"
dest = r"F:\WORK August 2022\drought-fires-spatial\sea fires"
fires = []

for path in Path(path).rglob('Yearly Fires'):
    print(str(path))
    for f in glob.glob(str(path)+'/*.shp'):
        fires.append(f)

years = [str(x) for x in range(2012, 2022)]

for year in years:
    
    mergefires = []

    for fire in fires:
        
        ext = Path(fire).stem[-4:]
        if(ext == year):
            mergefires.append(fire)
    
    print(len(mergefires))
    parameters = {'LAYERS': mergefires, 
                  'CRS': 'EPSG:4326', 
                  'OUTPUT': str(Path(dest).joinpath("sea_fires_{}.shp".format(year)))}

    processing.run("qgis:mergevectorlayers", parameters)
