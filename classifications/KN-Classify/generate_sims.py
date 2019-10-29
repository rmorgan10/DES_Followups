# Shell to call all simulation generation functions

import getpass
import numpy as np
import os
import pandas as pd
import sys

#read input data
event_name = sys.argv[1]
df = pd.read_csv('../events/%s/event_metadata.csv' %event_name)
username = getpass.getuser()



#check for and nuke existing sims directory
sim_path = '../events/%s/sim_gen' % event_name
if os.path.exists(sim_path):
    os.system('rm -r %s' %sim_path)
os.system('mkdir %s' %sim_path)

log_path = '../events/%s/logs' %event_name
if not os.path.exists(log_path):
    os.system('mkdir %s' %log_path)


if not os.path.exists('../events/%s/sim_gen/SIMLIB.txt' %event_name):
    print("Querying DB for observing conditions")
    #call makeSimlib_easyaccess.py
    ## run 10 times and track averate and std of returned effective areas
    areas = []
    total = 10
    for i in range(total):
        progress = float(i + 1) / 10 * 100
        sys.stdout.write('\rProgress:  %i %%' %int(progress))
        sys.stdout.flush()
        os.system('python makeSimlib_easyaccess.py -o "../events/%s/sim_gen/SIMLIB_raw.txt"' %event_name + 
                  ' --exptable "../events/%s/exptable.txt"' %event_name +
                  ' --min_ra %.1f --max_ra %.1f --min_dec %.1f --max_dec %.1f > %s/make_simlib.log' %(df['MIN_RA'].values[0], df['MAX_RA'].values[0],
                                                                                                      df['MIN_DEC'].values[0], df['MAX_DEC'].values[0], log_path))
        f = open("../events/%s/sim_gen/SIMLIB_raw.txt" %event_name, 'r')
        eff_area = f.readlines()[-1]
        f.close()
        areas.append(eff_area.split(' ')[-1])

    #call clean_simlib.py
    areas = [float(x) for x in areas]
    area, std = np.mean(areas), np.std(areas)
    log_file = open('../events/%s/logs/eff_area.log' %event_name, 'w+')
    log_file.write('%.6f' %std)
    log_file.close()
    os.system('python clean_simlib.py ../events/%s/sim_gen/SIMLIB_raw.txt ../events/%s/sim_gen/SIMLIB.txt %.6f' %(event_name, event_name, area))
else:
    print("Existing SIMLIB found, skipping simlib generation")

if not os.path.exists('../events/%s/sim_gen/SIMGEN_DES_NONIA.input' %event_name):
    #copy templates to sims directory
    os.system('cp ../templates/* ../events/%s/sim_gen/' %event_name)

    #call update_inputs.py
    os.system('python update_inputs.py %s' %event_name)
else:
    print("Existing SIM_INPUTS found, skipping update inputs")

#generate and retrieve simulations
os.chdir('../events/%s' %event_name)
if not os.path.exists('sims_and_data'):
    os.system('mkdir sims_and_data')

sim_dir_prefix = '/data/des41.b/data/SNDATA_ROOT/SIM/' + username + '_DESGW_' + event_name + '_'
print("Simulating light curves...")


###
#Parallelized and monitored implementation
###
args = []
if not os.path.exists('sims_and_data/%s_DESGW_%s_AGN_FITS' %(username, event_name)):
    args.append('agn')
    os.system('snlc_sim.exe sim_gen/AGN_SIMGEN.INPUT > logs/sim_agn.log &')
if not os.path.exists('sims_and_data/%s_DESGW_%s_KN_FITS' %(username, event_name)):
    args.append('kn')
    os.system('snlc_sim.exe sim_gen/SIMGEN_DES_KN.input > logs/sim_kn.log &')
if not os.path.exists('sims_and_data/%s_DESGW_%s_CC_FITS' %(username, event_name)):
    args.append('cc')
    os.system('snlc_sim.exe sim_gen/SIMGEN_DES_NONIA.input > logs/sim_cc.log &')
if not os.path.exists('sims_and_data/%s_DESGW_%s_Ia_FITS' %(username, event_name)):
    args.append('ia')
    os.system('snlc_sim.exe sim_gen/SIMGEN_DES_SALT2.input > logs/sim_ia.log &')

os.chdir('../../code')
monitor_args = ' '.join(args)
os.system('python monitor_sims.py %s %s' %(event_name, monitor_args))

os.chdir('../events/%s' %event_name)
os.system('mv ' + sim_dir_prefix + 'AGN  sims_and_data/%s_DESGW_%s_AGN_FITS' %(username, event_name))
os.system('mv ' + sim_dir_prefix + 'KN  sims_and_data/%s_DESGW_%s_KN_FITS' %(username, event_name))
os.system('mv ' + sim_dir_prefix + 'CC  sims_and_data/%s_DESGW_%s_CC_FITS' %(username, event_name))
os.system('mv ' + sim_dir_prefix + 'Ia  sims_and_data/%s_DESGW_%s_Ia_FITS' %(username, event_name))

