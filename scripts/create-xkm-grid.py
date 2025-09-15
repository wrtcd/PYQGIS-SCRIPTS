from pathlib import Path
from qgis.PyQt.QtCore import QVariant
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import glob
import processing
 
 # enter lat, long, grid size (n), date, and minimum confidence level for H8(hcon)
lat = 5.20
lon = 120.16

n = 3000

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
    
gridshp = createGrid(lat, lon, n)
QgsProject.instance().addMapLayer(gridshp)