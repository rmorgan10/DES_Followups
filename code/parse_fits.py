# functions for parsing SNANA fits files 

import numpy as np
import pandas as pd
from astropy.io import fits
import sys

#deal with input data
event_name = sys.argv[1]
phot_file = '../events/%s/LightCurvesReal_FITS/LightCurvesReal_PHOT.FITS' %event_name
head_file = '../events/%s/LightCurvesReal_FITS/LightCurvesReal_HEAD.FITS' %event_name

#read head file
hdu = fits.open(head_file)
head_columns = hdu[1].columns.names
head_data = hdu[1].data
hdu.close()
head_df = pd.DataFrame(data=head_data, columns=head_columns)

#read phot file
lcs = []
hdu = fits.open(phot_file)
phot_columns = hdu[1].columns.names
phot_data = hdu[1].data
hdu.close()

#split phot data into individual light curve dataframes
lc_data = []
total = float(len(phot_data))
counter = 0.0
for data_line in phot_data:
    #track progress
    counter += 1.0
    progress = counter / total * 100
    sys.stdout.write('\rProgress:  %.2f %%' %progress)
    sys.stdout.flush()

    #organize light curves
    if data_line[1] == '-':
        lcs.append(pd.DataFrame(data=np.array(lc_data), columns=phot_columns))
        lc_data = []
    else:
        lc_data.append(data_line)

#construct out dictionary
out_dict = {}
for index, row in head_df.iterrows():
    out_dict[row['SNID']] = {'metadata': row, 'lightcurve': lcs[index]}

#save out dict
os.system('mkdir ../events/%s/LightCurvesReal_PYTHON' %event_name)
np.save('../events/%s/LightCurvesReal_PYTHON/LightCurvesReal.npy' %event_name, out_dict)
