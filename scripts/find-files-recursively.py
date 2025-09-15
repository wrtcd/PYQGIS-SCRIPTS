import os, fnmatch

suffix = ['_grid_2021.shp']
exclude = set(['Refactored', 'Weibull Grids'])

def findExt(folder):
    
    matches = []
    
    for root, dirnames, filenames in os.walk(folder):
        dirnames[:] = [dn for dn in dirnames if dn not in exclude]
        for file in suffix:
            for filename in fnmatch.filter(filenames, '*' + file):
                matches.append(os.path.join(root, filename))
    return matches

grids_2021 = findExt(r"C:\Users\aeaturu\Desktop\January 2022\FIRES")

parameters = {'LAYERS': grids_2021, 
              'CRS': 'EPSG:4326', 
              'OUTPUT': r"C:\Users\aeaturu\Desktop\January 2022\Fires\grids_2021_merged.shp"}

processing.run("qgis:mergevectorlayers", parameters) 

''' 
for grid in grids_2021:
    iface.addVectorLayer(grid, '', 'ogr')
'''
    