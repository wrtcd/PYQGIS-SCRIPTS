import glob, pathlib
from pathlib import Path
import processing
from datetime import datetime, timedelta

# Function to convert YYYYDDD to YYYY-MM-DD
def convert_yearday_to_date(yearday):
    yearday = str(yearday)
    year = int(yearday[:4])
    day_of_year = int(yearday[4:])
    date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
    return date.strftime('%Y-%m-%d')

# Yearly fire directory
directory = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_yearly")
curryear = '2012'

# Search for the exact match (e.g., 'hms_fire2012.shp')
pattern = str(directory / f"hms_fire{curryear}.shp")
files = glob.glob(pattern)
if not files:
    raise FileNotFoundError(f"No file found for year {curryear}")
fire = files[0]
firelayer = QgsVectorLayer(fire, '', 'ogr')

statespath = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\shapefiles\states"
states = glob.glob(statespath + "/*.shp")

months = ["%.2d" % i for i in range(1, 13)]

# Loop over each state shapefile
for s in states:

    state = QgsVectorLayer(s, '', 'ogr')
    statename = Path(s).stem.split('_')[0]
    
    parameters = {'INPUT': firelayer, 
                  'OVERLAY': state, 
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
     
    clipped = processing.run("native:clip", parameters)['OUTPUT']
    
    for month in months:

        start_date = datetime(int(curryear), int(month), 1)
        if month == '12':
            end_date = datetime(int(curryear) + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(int(curryear), int(month) + 1, 1) - timedelta(days=1)
        
        start_yearday = int(start_date.strftime('%Y%j'))
        end_yearday = int(end_date.strftime('%Y%j'))

        expression = f"\"YEARDAY\" >= {start_yearday} AND \"YEARDAY\" <= {end_yearday}"
        clipped.selectByExpression(expression)

        savedir = Path(r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_seusa")
        outdir = savedir / statename / curryear
        outdir.mkdir(parents=True, exist_ok=True)
        
        destination = str(outdir / '{}_{}_{}_hms.shp'.format(statename, curryear, month))
        
        writer = QgsVectorFileWriter.writeAsVectorFormat(clipped, destination, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)
        del(writer)
