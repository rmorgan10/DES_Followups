# A module to automatically construct metadata information from dat files

import glob
import numpy as np
from optparse import OptionParser
import os
import pandas as pd
import sys

import utils

event_name = sys.argv[1]

if len(sys.argv) > 2:
    parser = OptionParser(__doc__)
    parser.add_option('--boost', default=10, help="Number of seasons to simulate for SNe")
    parser.add_option('--num_kn', default=10000, help="Number of KNe to simulate")
    parser.add_option('--num_agn', default=10000, help="Number of AGN to simulate")
    options, args = parser.parse_args(sys.argv[2:])
    boost = int(float(options.boost))
    num_kn = int(float(options.num_kn))
    num_agn = int(float(options.num_agn))
else:
    boost = 10
    num_kn = 10000
    num_agn = 10000


def get_mag_lims(df):
    mag_lims = []
    for index, row in df.iterrows():
        try:
            mag_lims.append(utils.MAGLIMIT_calculator(row['ZPFLUX'], row['PSF'], row['ZPFLUX'] - 2.5 * np.log10(row['SKYSIG']), 50.0))
        except:
            pass
    return mag_lims

dat_file_path_file = open('../events/%s/dat_file_path.txt' %event_name, 'r')
dat_file_path = dat_file_path_file.readlines()[0]
dat_file_path_file.close()
if dat_file_path[-1] == '\n':
    dat_file_path = dat_file_path[0:-1]
if dat_file_path[-1] != '/':
    dat_file_path = dat_file_path + '/'

#copy dat files to event directory for future use
os.system('cp -r %s ../events/%s/sims_and_data' %(dat_file_path, event_name))

ras, decs, expnums, glim, rlim, ilim, zlim = [], [], [], [], [], [], []
g, r, i, z = False, False, False, False
dat_files = glob.glob('../events/%s/sims_and_data/LightCurvesReal/*.dat' %event_name)


total = len(dat_files)
counter = 0.0

for dat_file in dat_files:
    #print(dat_file)
    
    #Track progress
    counter += 1.0
    progress = counter / total * 100.0
    sys.stdout.write('\rProgress:  %.2f     ' %progress)
    sys.stdout.flush()
    
    #parse the dat file
    lines = utils.open_dat(dat_file)
    lc = utils.get_terse_lc(lines)
    md = utils.get_meta_data(lines)
    
    #save ra and dec
    ras.append(float(md['RA']))
    decs.append(float(md['DEC']))
    
    #save expnums
    expnums += [int(x) for x in lc['EXPNUM'].values]

    #save limiting magnitude and band representation
    g_lc = lc[lc['FLT'].values == 'g']
    r_lc = lc[lc['FLT'].values == 'r']
    i_lc = lc[lc['FLT'].values == 'i']
    z_lc = lc[lc['FLT'].values == 'z']
    
    if g_lc.shape[0] != 0:
        g = True
        glim += get_mag_lims(g_lc)

    if r_lc.shape[0] != 0:
        r = True
        rlim += get_mag_lims(r_lc)

    if i_lc.shape[0] != 0:
        i = True
        ilim += get_mag_lims(i_lc)

    if z_lc.shape[0] != 0:
        z = True
        zlim += get_mag_lims(z_lc)


### calculate necessart metadata values
min_ra = np.min(ras) - 5.0
max_ra = np.max(ras) + 5.0
min_dec = np.min(decs) - 5.0
max_dec = np.max(decs) + 5.0

if len(glim) != 0:
    mag_lim_g = np.median(glim)
    mag_lim_g_std = np.std(glim)
else:
    mag_lim_g = 0.0
    mag_lim_g_std = 0.0

if len(rlim) !=0:
    mag_lim_r =np.median(rlim)
    mag_lim_r_std = np.std(rlim)
else:
    mag_lim_r =0.0
    mag_lim_r_std = 0.0

if len(ilim) !=0:
    mag_lim_i =np.median(ilim)
    mag_lim_i_std = np.std(ilim)
else:
    mag_lim_i =0.0
    mag_lim_i_std = 0.0

if len(zlim) !=0:
    mag_lim_z =np.median(zlim)
    mag_lim_z_std = np.std(zlim)
else:
    mag_lim_z =0.0
    mag_lim_z_std = 0.0

g = int(g)
r = int(r)
i = int(i)
z = int(z)


#compile into a csv
cols = ['NAME', 'MIN_RA', 'MAX_RA', 'MIN_DEC', 'MAX_DEC', 
        'LIM_MAG_g', 'LIM_MAG_r', 'LIM_MAG_i', 'LIM_MAG_z',
        'LIM_MAG_g_std', 'LIM_MAG_r_std', 'LIM_MAG_i_std', 'LIM_MAG_z_std',
        'g', 'r', 'i', 'z',
        'BOOST', 'NUM_KN', 'NUM_AGN']

data = [[event_name, min_ra, max_ra, min_dec, max_dec,
         mag_lim_g, mag_lim_r, mag_lim_i, mag_lim_z,
         mag_lim_g_std, mag_lim_r_std, mag_lim_i_std, mag_lim_z_std,
         g, r, i, z, 
         boost, num_kn, num_agn]]

event_info = pd.DataFrame(data=data, columns=cols)
event_info.to_csv('../events/%s/DES_metadata.csv' %event_name, index=False)

#merge with LIGO csv to make full event_metadata
ligo_df = pd.read_csv('../events/%s/LIGO_metadata.csv' %event_name)

event_metadata_df = ligo_df.merge(event_info, on='NAME')
event_metadata_df.to_csv('../events/%s/event_metadata.csv' %event_name, index=False)

