from pathlib import Path
from qgis.PyQt.QtCore import QVariant
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import glob
import processing
 
 # enter lat, long, grid size (n), date, and minimum confidence level for H8(hcon)
lon = 107.28
lat = 21.70
date = '2021-12-03'
n = 3
hcon = 1

def createGrid(lon, lat, n): # function that create a n x n grid from the grid center
    
    dist = 0.02
    lonlist = [round(lon - dist * n, 2) for n in range(-(n//2), (n//2)+1)]
    latlist = [round(lat + dist * n, 2) for n in range(-(n//2), (n//2)+1)]
    
    coordslist = gridcoords(lonlist, latlist)
    
    gridcentroids = QgsVectorLayer("Point", "temp", "memory")
    layer_provider = gridcentroids.dataProvider()
    layer_provider.addAttributes([QgsField("id", QVariant.Int, 'int', 3)])
    layer_provider.addAttributes([QgsField("lat", QVariant.Double, 'double', 3, 2)])
    layer_provider.addAttributes([QgsField("lon", QVariant.Double, 'double', 3, 2)])
    gridcentroids.updateFields()
    
    fieldcounter = 0
    for c in coordslist:
        
        id = fieldcounter
        lat = c[0]
        lon = c[1]
        
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon,lat)))
        f.setAttributes([id, lat, lon])
        layer_provider.addFeature(f)
        fieldcounter = fieldcounter + 1

    gridcentroids.updateExtents() 

    parameters = {
                    'INPUT': gridcentroids,
                    'SHAPE:': 0,
                    'WIDTH': 0.02,
                    'HEIGHT': 0.02,
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                    }
    gridshp = processing.run("native:rectanglesovalsdiamonds", parameters)['OUTPUT']
    gridshp.setName('{} x {}_grid'.format(n, n))
    
    return gridshp
    
def getCoordsList(lon, lat, n): # call grid's centroids list formula with arguments
    
    dist = 0.02
    lonlist = [round(lon - dist * n, 2) for n in range(-(n//2), (n//2)+1)]
    latlist = [round(lat + dist * n, 2) for n in range(-(n//2), (n//2)+1)]
    
    coordslist = gridcoords(lonlist, latlist)
    return coordslist
    
def gridcoords(x, y): # formula to create grid centroids list
    
    coords = []
    
    for i in x:
        for j in y:
            coords.append([i, j])
            
    return coords
    
def convert_dtype(data): # convert pandas datatypes to qgis types 
    """ function to convert pandas data types to native python type """
       
    def conversion(element):
        ## try and except are used because strings (in this context) behave differently  
        ## to ints/floats and do not have a dtype attribute
        try:
            if element.dtype.name == 'int64':
                return int(element)
            elif element.dtype.name == 'float64':
                return float(element)
            else:
                return element
        except:
            return element
       
    return [conversion(x) for x in data]

def hShape(gridshp, date, hcon): # make himawari shapefile 
    
    dt = datetime.strptime(date, '%Y-%m-%d')
    dtprev = dt - timedelta(days=1)
    
    hdate = dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')
    hdateprev = dtprev.strftime('%Y')+dtprev.strftime('%m')+dtprev.strftime('%d')
    
    directory = Path(r"D:\WORK September 2022\gridcal\data")
    himawari = directory.joinpath('himawari_hourly_2021')
    
    #current day
    year = hdate[:4]
    yearmonth = hdate[:6]
    month = hdate[4:6]
    day = hdate[6:]
    hourly = himawari.joinpath(yearmonth, day)
    firescur = glob.glob(str(hourly)+"/*.csv")
    
    #prevday
    yearprev = hdateprev[:4]
    yearmonthprev = hdateprev[:6]
    monthprev = hdateprev[4:6]
    dayprev = hdateprev[6:]
    hourlyprev = himawari.joinpath(yearmonthprev, dayprev)
    firesprev = glob.glob(str(hourlyprev)+"/*.csv")
    
    fires = firesprev + firescur
    fires.sort()

    newdf = pd.DataFrame(columns=['#year', 'month', 'day', 'hour', 
                                  'lat', 'lon', 'ave(frp)', 'max(frp)',
                                  'ave(confidence)', 'N'
                                  ])
    idx = 0
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
        df['id'] = idx
        newdf = newdf.append(df)
        idx = idx + 1
    
    newdf['DateTime'] = newdf['DateTime'] + pd.DateOffset(hours=utc)
    newdf["local time"] = newdf['DateTime'].dt.time
    newdf['date'] = pd.to_datetime(newdf['DateTime'].dt.date)
    newdf["local time"] = newdf["local time"].apply(lambda x: x.strftime("%I:%M %p"))
    newdf = newdf.loc[newdf['date'] == date]
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

def vShape(gridshp, date): # make viirs shapefile
    
    directory = Path(r"D:\WORK September 2022\gridcal\data")
    viirs = directory.joinpath('viirs')
    fires = glob.glob(str(viirs)+"/*.shp")
    fire = QgsVectorLayer(fires[0], '', 'ogr')
    
    parameters = {
                'INPUT': fire, 
                'OVERLAY': gridshp, 
                'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }

    # run the clip tool
    clipped = processing.run("native:clip", parameters)        
    
    clippedlayer = clipped['OUTPUT']
    
    clippedlayer.selectByExpression("\"ACQ_DATE\"='{}'".format(date))
    
    parameters = {
                    'INPUT': clippedlayer, 
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                }
    
    vshape = processing.run('qgis:saveselectedfeatures', parameters)['OUTPUT']
    
    parameters = {
                    'INPUT': vshape,
                    'JOIN': gridshp,
                    'PREDICATE': [5],
                    'DISCARD_NONMATCHING':True,
                    'JOIN_FIELDS': 'id',
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                    }
    
    vjabl = processing.run('qgis:joinattributesbylocation', parameters)
    vshape = vjabl['OUTPUT']
    
    parameters = {
                    'INPUT': vshape, 
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                    }

    vspshape = processing.run("qgis:multiparttosingleparts", parameters)['OUTPUT']
    vspshape.setName('viirs')
    
    layer = utcTolocal(vspshape, utc)
    layer.dataProvider().createSpatialIndex()
    
    return layer

def mShape(gridshp, date): # make modis shapefile 
    
    directory = Path(r"D:\WORK September 2022\gridcal\data")
    viirs = directory.joinpath('modis')
    fires = glob.glob(str(viirs)+"/*.shp")
    fire = QgsVectorLayer(fires[0], '', 'ogr')
    
    parameters = {
                    'INPUT': fire, 
                    'OVERLAY': gridshp, 
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                }

    # run the clip tool
    clipped = processing.run("native:clip", parameters)        
    
    clippedlayer = clipped['OUTPUT']
    
    clippedlayer.selectByExpression("\"ACQ_DATE\"='{}'".format(date))
    
    parameters = {
                    'INPUT': clippedlayer, 
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                }
    
    mshape = processing.run('qgis:saveselectedfeatures', parameters)['OUTPUT']
    
    parameters = {
                    'INPUT': mshape,
                    'JOIN': gridshp,
                    'PREDICATE': [5],
                    'DISCARD_NONMATCHING':True,
                    'JOIN_FIELDS': 'id',
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                    }
    
    mjabl = processing.run('qgis:joinattributesbylocation', parameters)
    mshape = mjabl['OUTPUT']
    mshape.setName('modis')
    
    layer = utcTolocal(mshape, utc)
    layer.dataProvider().createSpatialIndex()
    
    return mshape
    
def renameField(rlayer, oldname, newname): # rename grid fields
  
  findex = rlayer.dataProvider().fieldNameIndex(oldname)
  
  if findex != -1:
    rlayer.dataProvider().renameAttributes({findex: newname})
    rlayer.updateFields()

def gridstats(gridshp, hshape, vshape, mshape): # calculate grid stats
    
    parameters = {'POLYGONS': gridshp,
                  'POINTS': hshape,
                  'WEIGHT': 'N',
                  'FIELD': 'H FC',  
                  'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }
    hcount = processing.run("native:countpointsinpolygon", parameters)['OUTPUT']
    
    parameters = {'POLYGONS': hcount,
                  'POINTS': vshape,
                  'FIELD': 'V FC',  
                  'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }
    hvcount = processing.run("native:countpointsinpolygon", parameters)['OUTPUT']
    
    parameters = {'POLYGONS': hvcount,
                  'POINTS': mshape,
                  'FIELD': 'M FC',  
                  'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }
    hvmcount = processing.run("native:countpointsinpolygon", parameters)['OUTPUT']
    
    parameters = {'INPUT': hvmcount,
                  'JOIN': hshape,
                  'PREDICATE': 1,
                  'JOIN_FIELDS':['ave(frp)'],
                  'SUMMARIES':[5,6],
                  'DISCARD_NONMATCHING':False,
                  'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }
    hfrp = processing.run("qgis:joinbylocationsummary", parameters)['OUTPUT']
    
    parameters = {'INPUT': hfrp,
                  'JOIN': vshape,
                  'PREDICATE': 1,
                  'JOIN_FIELDS':['FRP'],
                  'SUMMARIES':[5,6],
                  'DISCARD_NONMATCHING':False,
                  'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }
    hvfrp = processing.run("qgis:joinbylocationsummary", parameters)['OUTPUT']
    
    parameters = {'INPUT': hvfrp,
                  'JOIN': mshape,
                  'PREDICATE': 1,
                  'JOIN_FIELDS':['FRP'],
                  'SUMMARIES':[5,6],
                  'DISCARD_NONMATCHING':False,
                  'OUTPUT': 'TEMPORARY_OUTPUT'
                                            }
    hvmfrp = processing.run("qgis:joinbylocationsummary", parameters)['OUTPUT']
    
    hvmfrp.setName('{}x{} gridstats'.format(n, n))
    
    renameField(hvmfrp,"ave(frp)_sum", "H AVGFRP SUM")
    renameField(hvmfrp,"ave(frp)_mean", "H AVGFRP MEAN")
    renameField(hvmfrp,"FRP_sum", "V FRP SUM")
    renameField(hvmfrp,"FRP_mean", "V FRP MEAN")
    renameField(hvmfrp,"FRP_sum_2", "M FRP SUM")
    renameField(hvmfrp,"FRP_mean_2", "M FRP MEAN")
    
    output = results + "\\" + "{}_{}_{}_{}_gridstats".format(country, date, lon, lat) + '.csv'
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "CSV"

    QgsVectorFileWriter.writeAsVectorFormatV2(hvmfrp, output, QgsCoordinateTransformContext(), options)
    
    return hvmfrp
    
def mergeStats(): # merge 3 layers
    
    parameters = {
                    'INPUT': vshape, 
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                    }

    vspshape = processing.run("qgis:multiparttosingleparts", parameters)['OUTPUT']
    
    merged = []
    layerlist = QgsProject.instance().mapLayers()
    for layer in layerlist:
        merged.append(layer)
    
    parameters = {
                    'LAYERS': merged, 
                    'CRS': 'EPSG:4326', 
                    'OUTPUT': 'TEMPORARY_OUTPUT'
                                                    }

    mergestats = processing.run("qgis:mergevectorlayers", parameters)['OUTPUT']
    mergestats.setName("mergestats")
    
    output = results + "\\" + "{}_{}_{}_{}_mergestats".format(country, date, lon, lat) + '.csv'
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "CSV"

    QgsVectorFileWriter.writeAsVectorFormatV2(mergestats, output, QgsCoordinateTransformContext(), options)
        
    return mergestats

def getUTC(lon, lat): # get utc hours ahead
    
    countriespath = r"D:\WORK September 2022\gridcal\data\countries\sea-shape.shp"
    countries = QgsVectorLayer(countriespath, '', 'ogr')
    
    point = QgsGeometry.fromPointXY(QgsPointXY(lon,lat))
    features = countries.getFeatures()
    
    for f in features:
        if f.geometry().contains(point):
            country = f.attributes()[9]
    
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
    
    countriespath = r"D:\WORK September 2022\gridcal\data\countries\sea-shape.shp"
    countries = QgsVectorLayer(countriespath, '', 'ogr')
    
    point = QgsGeometry.fromPointXY(QgsPointXY(lon,lat))
    features = countries.getFeatures()
    
    for f in features:
        if f.geometry().contains(point):
            country = f.attributes()[9]
    
    return country
    
def utcTolocal(layer, utc):
    
    layer_provider = layer.dataProvider()
    features = layer.getFeatures()
    
    layer_provider.addAttributes([QgsField("local time",QVariant.String)])
    layer_provider.addAttributes([QgsField("date",QVariant.String)])
    layer.updateFields()
    
    local_time_idx = layer.fields().lookupField("local time")
    date_to_add_idx = layer.fields().lookupField("date")
    acqdate_idx = layer.fields().lookupField("ACQ_DATE")
    acqtime_idx = layer.fields().lookupField("ACQ_TIME")
    
    
    for f in features:
        
        fid = f.id()
        utc_string = f.attributes()[acqdate_idx] + " " + f.attributes()[acqtime_idx]
        utc_time = datetime.strptime(utc_string,"%Y-%m-%d %H%M")
        utc_offset  = utc_time + timedelta(hours=utc)
        date = utc_offset.strftime("%Y-%m-%d")
        time = utc_offset.strftime("%I:%M %p")
        
        attr_value = {local_time_idx:time, date_to_add_idx:date}
        layer_provider.changeAttributeValues({fid:attr_value})
    
    flist = [acqdate_idx, acqtime_idx]
    layer_provider.deleteAttributes(flist)
    layer.updateFields()
        
    return layer


gridshp = createGrid(lat, lon, n) 
coordslist = getCoordsList(lat, lon, n) 
utc = getUTC(lon, lat) 

hshape = hShape(gridshp, date, hcon) 
vshape = vShape(gridshp, date) 
mshape = mShape(gridshp, date) 

country = getCountry(lon, lat)
results = r"D:\WORK September 2022\gridcal\data\results"

QgsProject.instance().addMapLayer(hshape)
QgsProject.instance().addMapLayer(vshape)
QgsProject.instance().addMapLayer(mshape)

mergestats = mergeStats() 
gridstats = gridstats(gridshp, hshape, vshape, mshape) 
QgsProject.instance().addMapLayer(gridstats)
QgsProject.instance().addMapLayer(mergestats)