from pathlib import Path
import glob
import processing

directory = Path(r"D:\WORK January 2023\monthlydroughtindices")
curryear = '2022'

firedir = curryear + " Monthly Fire Grids"
fires = glob.glob(str(directory.joinpath(curryear, firedir)) + '/*.shp')

droughtdir = curryear + " Drought Indices"
droughts = glob.glob(str(directory.joinpath(curryear, droughtdir)) + '/*.csv')

directory.joinpath(curryear, curryear + ' Monthly Subsets').mkdir(parents=True, exist_ok=True)
