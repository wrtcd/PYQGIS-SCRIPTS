import glob, pathlib
from pathlib import Path
import processing

# Yearly fire directory
directory = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_yearly")
curryear = '2012'

# Search for the exact match (e.g., 'seusa_2012.shp')
pattern = str(directory / f"hms_fire{curryear}.shp")
files = glob.glob(pattern)
if not files:
    raise FileNotFoundError(f"No file found for year {curryear}")
fire = files[0]
firelayer = QgsVectorLayer(fire, '', 'ogr')

statespath = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\shapefiles\states"
states = glob.glob(statespath + "/*.shp")

months = ["%.2d" % i for i in range(1, 13)]
stringmonths = [str(m) for m in months]

lastday = {}
lastday['01'] = '31'
lastday['02'] = '28'
lastday['03'] = '31'
lastday['04'] = '30'
lastday['05'] = '31'
lastday['06'] = '30'
lastday['07'] = '31'
lastday['08'] = '31'
lastday['09'] = '30'
lastday['10'] = '31'
lastday['11'] = '30'
lastday['12'] = '31'

for s in states:
    
    state = QgsVectorLayer(s, '', 'ogr')
    statename = Path(s).stem.split('_')[0]
    
    print(statename)
                    
    parameters = {'INPUT': firelayer, 
                  'OVERLAY': state, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
     
    clipped = processing.run("native:clip", parameters)['OUTPUT']
    
    for month in stringmonths:
        
        if int(curryear) in [2012, 2016, 2020, 2024]:
            lastday['02'] = '29'
        
        startDate = str(curryear)+'-{}-01'.format(month)
        endDate = str(curryear)+'-{}-{}'.format(month, lastday[month])
        
        print(startDate, endDate)
        
        clipped.selectByExpression("\"ACQ_DATE\">='{}' and \"ACQ_DATE\"<='{}'".format(startDate, endDate))
        
        savedir = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_seusa")
        
        # Create output directory if it doesn't exist
        outdir = savedir / statename / curryear
        outdir.mkdir(parents=True, exist_ok=True)
        
        destination = str(outdir / '{}_{}_{}_hms.shp'.format(statename, curryear, month))
        
        writer = QgsVectorFileWriter.writeAsVectorFormat(clipped, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
        del(writer)
