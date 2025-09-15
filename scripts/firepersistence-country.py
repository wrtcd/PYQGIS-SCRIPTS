from pathlib import Path
from qgis.PyQt.QtCore import QVariant
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import glob
import processing
 
 # enter lat, long, grid size (n), date, and minimum confidence level for H8(hcon)
country = 'myanmar'
date = '2021-03-03'
cycle = 1
hcon = 1
    
def hShape(gridshp, hcon): # make himawari shapefile 
    
    dirs = []

    for c in cycles:
        
        month = c.replace('-', '')[:6]
        day = c.replace('-', '')[6:8]
        dirs.append([month, day])

    nested = []

    directory = Path(r"D:\WORK September 2022\gridcal\data")
    himawari = directory.joinpath('himawari_hourly_2021')

    for dir in dirs:
        
        hourly = himawari.joinpath(dir[0], dir[1])
        files = glob.glob(str(hourly)+"/*.csv")
        
        nested.append(files)

    fires = [item for sublist in nested for item in sublist]
    fires.sort()

    newdf = pd.DataFrame(columns=['#year', 'month', 'day', 'hour', 
                                  'lat', 'lon', 'ave(frp)', 'max(frp)',
                                  'ave(confidence)', 'N'
                                  ])
    
    coordslist = getCoordsList(grid)
    
    for coords in coordslist:
        
        hourlymerged = pd.DataFrame(columns=['#year', 'month', 'day', 'hour', 
                                  'lat', 'lon', 'ave(frp)', 'max(frp)',
                                  'ave(confidence)', 'N'
                                  ])
        
        for f in fires:
            
            data = pd.read_csv(f, header=1)
            year = int(Path(f).stem[4:8])
            month = int(Path(f).stem[8:10].lstrip('0'))
            day = int(Path(f).stem[10:12].lstrip('0'))
            data['hours'] = Path(f).stem[13:17]
            data["ACQ_TIME"] = pd.to_datetime(data.hours, format='%H%M')
            data['DateTime'] = data['ACQ_TIME'].map(lambda t: t.replace(year=year, month=month, day=day))
            hourlymerged = hourlymerged.append(data, ignore_index = True)
            
        df = hourlymerged.loc[(hourlymerged['lon'] == coords[1]) & (hourlymerged['lat'] == coords[0]) 
                          & (hourlymerged['ave(confidence)'] >= hcon)]

        newdf = newdf.append(df)
    
    newdf['DateTime'] = newdf['DateTime'] + pd.DateOffset(hours=utc)
    newdf["local time"] = newdf['DateTime'].dt.time
    newdf['date'] = pd.to_datetime(newdf['DateTime'].dt.date)
    newdf["local time"] = newdf["local time"].apply(lambda x: x.strftime("%I:%M %p"))
    newdf = newdf.loc[(newdf['date'] >= cycles[1]) & (newdf['date'] <= cycles[len(cycles) - 2])]
    newdf = newdf.sort_values(['id', 'local time'])
    newdf["date"] = newdf["date"].astype(str)
    newdf["local time"] = newdf["local time"].astype(str)
    newdf = newdf.rename(columns={'#year': 'year'})
    newdf = newdf.drop(['year', 'month', 'day', 'hour', 'hours'], axis=1)
    newdf = newdf[['lat','lon','ave(frp)','max(frp)','ave(confidence)','id','date', 'local time','N']]
    newdf = newdf.reset_index(drop=True)
    
    hshape = QgsVectorLayer("Point", "himawari", "memory")
    hshape_provider = hshape.dataProvider()
    hshape_provider.addAttributes([QgsField("lat",QVariant.Double, 'double', 20, 2)])
    hshape_provider.addAttributes([QgsField("lon",QVariant.Double, 'double', 20, 2)])
    hshape_provider.addAttributes([QgsField("ave(frp)",QVariant.Double, 'double', 3, 2)])
    hshape_provider.addAttributes([QgsField("max(frp)",QVariant.Double, 'double', 3, 2)])
    hshape_provider.addAttributes([QgsField("ave(confidence)",QVariant.Double, 'double', 3, 2)])
    hshape_provider.addAttributes([QgsField("id",QVariant.Int, 'int', 3)])
    hshape_provider.addAttributes([QgsField("date",QVariant.String, 'date')])
    hshape_provider.addAttributes([QgsField("local time",QVariant.String, 'text')])
    hshape_provider.addAttributes([QgsField("N",QVariant.Double, 'double', 1)])
    hshape.updateFields()
    
    flist= [field.name() for field in hshape.fields()]
    
    for i in newdf.index.to_list():
    
        f = QgsFeature()
        newrow = newdf[flist].iloc[i].tolist()
        converted = convert_dtype(newrow)
        f.setAttributes(converted)
        
        lat = converted[0]
        lon = converted[1]
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon,lat)))

        hshape_provider.addFeature(f)
        
    hshape_provider.createSpatialIndex()
    
    return hshape
    
def getUTC(country): # get utc hours ahead
    
    localtime = {
                    'brunei':8,
                    'cambodia':7,
                    'indonesia':7,
                    'laos':7,
                    'myanmar':6.5,
                    'malaysia':8,
                    'philippines':8,
                    'singapore':8,
                    'thailand':7,
                    'timorleste':9,
                    'vietnam':7
                                        }
    
    return localtime[country]
    
def getCountry(lon, lat): # get utc hours ahead
    
    countriespath = r"D:\WORK September 2022\seag\data\countries\sea-shape.shp"
    countries = QgsVectorLayer(countriespath, '', 'ogr')
    
    point = QgsGeometry.fromPointXY(QgsPointXY(lon,lat))
    features = countries.getFeatures()
    
    for f in features:
        if f.geometry().contains(point):
            country = f.attributes()[9]
    
    return country
    
def getCycles(date, n):
    
    cycles = []
    
    pdate = datetime.strptime(date, "%Y-%m-%d")
    
    for i in range(-1, n + 1):
    
        cycle = pdate + timedelta(days=i)
        scycle = cycle.strftime('%Y-%m-%d')
        print(scycle)
        cycles.append(scycle)
            
    return cycles
    
def getCountryGrid(country):
    
    gridspath = r"D:\WORK September 2022\fire-persistence\grids"
    grids = glob.glob(gridspath+"\\"+'/*.shp')
    
    for grid in grids:
        
        if country in grid:
            
            layer = QgsVectorLayer(grid, '', 'ogr')
    
    
    return layer


def getCoordsList(grid):
    
    coords = []
    
    features = grid.getFeatures()
    
    for f in features:
        
        coords.append([f.attributes()[1], f.attributes()[2]])
    
    return coords
    

grid = getCountryGrid(country)
cycles = getCycles(date, cycle)
hshape = hShape(grid, hcon) 
utc = getUTC(country) 
QgsProject.instance().addMapLayer(hshape)