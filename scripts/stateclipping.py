import glob, pathlib
from pathlib import Path
import processing

firesdir = r"C:\Users\aeaturu\Desktop\WORK April 2025\Southeast USA Data Download\HMS\hms_yearly"
fires = glob.glob(firesdir+"/*.shp")

statesdir = r"C:\Users\aeaturu\Desktop\Southeast USA Data Download\shapefiles\states"
states = glob.glob(statesdir+"/*.shp")


for state in states:
    
    statelayer = QgsVectorLayer(state, '', 'ogr')
    statename = Path(state).stem.split('_')[0]
    
    for fire in fires:
        
        yearmonth = Path(fire).stem.split('_')[2]
        year = yearmonth[:4]
        month = yearmonth[4:6]
        
        filename = statename + '_' + year + '_' + month + '_HMS.shp'
        print(filename)
        firelayer = QgsVectorLayer(fire, '', 'ogr')
        
        destination = r"C:\Users\aeaturu\Desktop\WORK April 2025\fire app\data\{}".format(filename)
                
        parameters = {'INPUT': firelayer, 
                      'OVERLAY': statelayer, 
                      'OUTPUT': destination}
                      
        processing.run("native:clip", parameters)