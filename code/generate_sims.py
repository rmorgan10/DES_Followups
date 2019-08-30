# Shell to call all simulation generation functions

import getpass
import os
import pandas as pd
import sys

#read input data
event_name = sys.argv[1]
df = pd.read_csv('../events/%s/event_metadata.csv' %event_name)
username = getpass.getuser()

#check for and nuke existing sims directory
sim_path = '../events/%s/sims' % event_name
if os.path.exists(sim_path):
    os.system('rm -r %s' %sim_path)

#make sims sub directory
os.system('mkdir %s' %sim_path)

#call makeSimlib_easyaccess.py
os.system('python makeSimlib_easyaccess.py -o "../events/%s/sims/SIMLIB_raw.txt"' %event_name + 
          ' --exptable "../events/%s/exptable.txt"' %event_name +
          ' --min_ra %.1f --max_ra %.1f --min_dec %.1f --max_dec %.1f' %(df['MIN_RA'].values[0], df['MAX_RA'].values[0],
                                                                         df['MIN_DEC'].values[0], df['MAX_DEC'].values[0]))

#call clean_simlib.py
os.system('python clean_simlib.py ../events/%s/sims/SIMLIB_raw.txt ../events/%s/sims/SIMLIB.txt' %(event_name, event_name))

#copy templates to sims directory
os.system('cp ../templates/* ../events/%s/sims/' %event_name)

#call update_inputs.py
os.system('python update_inputs.py %s' %event_name)


#generate and retrieve simulations
os.chdir('../events/%s/sims/' %event_name)
sim_dir_prefix = '/data/des41.b/data/SNDATA_ROOT/SIM/' + username + '_DESGW_' + event_name + '_'
os.system('snlc_sim.exe AGN_SIMGEN.INPUT')
os.system('mv ' + sim_dir_prefix + 'AGN  .')
os.system('snlc_sim.exe SIMGEN_DES_KN.input')
os.system('mv ' + sim_dir_prefix + 'KN  .')
os.system('snlc_sim.exe SIMGEN_DES_NONIA.input')
os.system('mv ' + sim_dir_prefix + 'CC  .')
os.system('snlc_sim.exe SIMGEN_DES_SALT2.input')
os.system('mv ' + sim_dir_prefix + 'Ia  .')

