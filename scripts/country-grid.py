import glob, pathlib
from pathlib import Path
import processing

# globalgrid
gridpath = r"D:\WORK February 2022\FIRES\raw-grid"
griddir = Path(gridpath)
gridpath = glob.glob(str(griddir)+"/*Project.shp")
globalgrid = QgsVectorLayer(gridpath[0], '', 'ogr')

# country shape
region = "SA"
country = "srilanka"
directory = Path("D:\WORK February 2022\FIRES")

vlayersource = directory.joinpath(region, country)
vlayer = glob.glob(str(vlayersource) + '/*shape.shp')
countrylayer = QgsVectorLayer(vlayer[0], '', 'ogr')

# create spatial index
countrylayer.dataProvider().createSpatialIndex()

# clip globalgrid with countrylayer
# set input and output file names
countrygrid = str(vlayersource.joinpath("{}_grid.shp".format(country)))

parameters = {'INPUT': globalgrid, 
              'OVERLAY': countrylayer, 
              'OUTPUT': countrygrid}

# run the clip tool
processing.run("native:clip", parameters)