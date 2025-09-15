pointlayerpath = r"D:\WORK February 2022\FIRES\SA\afghanistan\afghanistan_fires.shp"
polygonlayerpath = r"D:\WORK February 2022\FIRES\SA\afghanistan\afghanistan_grid.shp"

pointlayer = QgsVectorLayer(pointlayerpath, '', 'ogr')
polygonlayer = QgsVectorLayer(polygonlayerpath, '', 'ogr')

pointlayer.dataProvider().createSpatialIndex()
polygonlayer.dataProvider().createSpatialIndex()

parameters = {'POLYGONS': polygonlayer,
              'POINTS': pointlayer,
              'FIELD': 'Count',  
              'OUTPUT': 'memory'}
              
countpointsinpolygon = processing.run("native:countpointsinpolygon", parameters)

layer = iface.addVectorLayer(countpointsinpolygon['OUTPUT'], '', 'ogr')