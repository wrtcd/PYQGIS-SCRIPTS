from pylab import *
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import glob, pathlib
from pathlib import Path

region='SA'
country='india'

globaldirectory = pathlib.Path.home().joinpath('Desktop', 'January 2022', 'Fires', region, country, 'Yearly Grids')
weibulldirectory = globaldirectory.joinpath('Weibull')
files = glob.glob(str(weibulldirectory)+'./*.csv')

Path(globaldirectory.joinpath('Weibull Curves')).mkdir(parents=True, exist_ok=True)

for file in files:
    
    df = pd.read_csv(file)
    
    weibull = df['Weibull']
    fires = df['Fires']
    fn = str(Path(file).stem)
    country = fn[:len(fn)-13:].title()
    year = file[-8:-4:]
    
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    
    plt.scatter(fires, weibull, s=32, c=['r'])
    axes.set_xlabel('Fire Count')
    axes.set_ylabel('Probability Exceedance % (Weibull)')
    axes.set_title('Probability Exceedance (Weibull) - {} {}'.format(year, country))
    show()
    
    outdirectory = str(globaldirectory.joinpath('Weibull Curves'))
    output = fn.replace('weibull', 'weibull_curve')
    fig.savefig(outdirectory+ "\\" +output, dpi=300)