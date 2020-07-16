# A module to parse cut summary files and print a nice table

import getpass
import numpy as np
import os
import pandas as pd
import sys

import utils

event_name = sys.argv[1]
sim_include = sys.argv[2]
os.chdir('../events/%s/cut_results' %event_name)
username = getpass.getuser()

try:
    force_area = float(sys.argv[2])
except:
    force_area = None

#check for existence of summary files
for obj in sim_include.split(','):
    if not os.path.exists('%s_DESGW_%s_%s_cut_summary.txt' %(username, event_name, obj)):
        print("ERROR: %s cut summary file is missing." %obj)
        sys.exit()

if not os.path.exists('LightCurvesReal_cut_summary.txt'):
    print("ERROR: LightCurvesReal cut summary file is missing.")
    sys.exit()

#Read and format cut summary files
all_results = []
for obj in sim_include.split(','):
    results = pd.read_csv('%s_DESGW_%s_%s_cut_summary.txt' %(username, event_name, obj), delim_whitespace=True)
    results[obj] = results['REMAINING'].values
    results = results.drop('REMAINING', axis=1)
    all_results.append(results.copy())

df = pd.read_csv('LightCurvesReal_cut_summary.txt', delim_whitespace=True)
df['DATA'] = df['REMAINING'].values
df = df.drop('REMAINING', axis=1)

#make a df that will have all the raw counts of the cutflow  
for res in all_results:
    df = df.merge(res, on=['CUT', 'NAME'])

df.to_csv('MERGED_CUT_RESULTS.csv')


# This could be useful at some point for calculating expected numbers of objects, but needs to be adapted and is not vital
# for generating the simulations
"""
#incorporate expected rates of objects
event_info = pd.read_csv('../event_metadata.csv')

##use boost to scale the number of SNe
boost = float(event_info['BOOST'].values[0])

##read uncertainty on SNe numbers from log files
ia_log = open('../logs/sim_ia.log', 'r')
lines = ia_log.readlines()
ia_log.close()
ia_unc = float([y for y in [x for x in lines[-20:] if x[0:39] == '  Number of SNe per season AFTER CUTS :'][0].split(' ') if y != '' and y != '\n'][-1]) / boost

cc_log = open('../logs/sim_cc.log', 'r')
lines = cc_log.readlines()
cc_log.close()
cc_unc = float([y for y in [x for x in lines[-200:] if x[0:39] == '  Number of SNe per season AFTER CUTS :'][0].split(' ') if y != '' and y != '\n'][-1]) / boost


##use prob kn to scale the number of KN
prob_KN = event_info['LIGO_prob_KN'].values[0]

##use effective area to scale the number of agn
simlib_file = open('../sim_gen/SIMLIB.txt', 'r')
lines = simlib_file.readlines()
simlib_file.close()
eff_area = float([x for x in lines[-5:] if x[0:15] == 'EFFECTIVE_AREA:'][0].split(' ')[1][0:-1])

#calc area scale factor
if force_area is None:
    scale_factor = 1.0
else:
    scale_factor = force_area / eff_area
"""



