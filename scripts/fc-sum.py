import glob
from pathlib import Path
import processing
import pandas as pd
import csv

csvdir = r'D:\WORK JUNE 2024\fire forecasting\viirs_fire_data_from_2023_2024_May\sea csv'
files = glob.glob(csvdir + '/*.csv')

for file in files:
    
    data = pd.read_csv(file)
    data['VERSION'] = 1
    data['ACQ_DATE'] = pd.to_datetime(data['ACQ_DATE'])
    data = data.set_index('ACQ_DATE')
    
    fcdf = data.resample('1M').sum()
    fcdf = fcdf.rename(columns={'VERSION': 'FCSUM'})
    fcdf = fcdf['FCSUM']
    
    fcdf = fcdf.reset_index()
    
    name = Path(file).stem
    fcdf.to_csv(r'D:\WORK JUNE 2024\fire forecasting\datasets\csvs_to_add\sea\{}.csv'.format(name))
    