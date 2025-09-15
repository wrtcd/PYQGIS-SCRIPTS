INPUT='C:\Users\aeaturu\Desktop\January 2022\FIRES\grids_2021_weibull_grid.shp'
OUTPUT='C:\Users\aeaturu\Desktop\January 2022\FIRES\domain_2021_weibull_raster.shp'
	
	C:/OSGeo4W/bin/gdal_rasterize.exe -a Weibull -tr 0.01 0.01 -a_nodata 0.0 \
	-te 60.505200177 29.406105 74.892101989 38.472115 \
	-ot Float32 -of GTiff \
	$INPUT "$OUTPUT"

