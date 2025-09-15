#!/bin/bash

for f in afghanistan_weibull_grid_20{12..21}.shp;do
	cwd=$(PWD)
	pd="$(dirname "$cwd")"
	year=${f: -8:4}
	suffix=${f: -22}
	country=${f%"$suffix"}	
	wraster='_weibull_raster_'
	echo $f
	INPUT=$f
	OUTPUT="$pd"/Weibull\ Rasters/$country$wraster$year.tif
	echo $OUTPUT
	
	C:/OSGeo4W/bin/gdal_rasterize.exe -a Weibull -tr 0.01 0.01 -a_nodata 0.0 \
	-te 60.505200177 29.406105 74.892101989 38.472115 \
	-ot Float32 -of GTiff \
	$INPUT "$OUTPUT"
done
