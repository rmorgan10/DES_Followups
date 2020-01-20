# A module to remove files of previous runs

#ideally will be given more options in future

import os
import sys

event_name = sys.argv[1]
mode = sys.argv[2]

# modes
allowed_modes = ['sims', 'everything']
if mode not in allowed_modes:
    print("'%s' not in allowed modes for clean up" %mode)
    sys.exit()

#redo_sims
if mode == 'sims':
    os.system('rm -rf ../events/%s/sim_gen' %event_name)
    os.system('rm -rf ../events/%s/sims_and_data/*_CC_*' %event_name)
    os.system('rm -rf ../events/%s/sims_and_data/*_Ia_*' %event_name)
    os.system('rm -rf ../events/%s/sims_and_data/*_KN_*' %event_name)
    os.system('rm -rf ../events/%s/sims_and_data/*_AGN_*' %event_name)
    os.system('rm -rf ../events/%s/cut_results/*_CC_*' %event_name)
    os.system('rm -rf ../events/%s/cut_results/*_Ia_*' %event_name)
    os.system('rm -rf ../events/%s/cut_results/*_KN_*' %event_name)
    os.system('rm -rf ../events/%s/cut_results/*_AGN_*' %event_name)
    os.system('rm -rf ../events/%s/event_metadata.csv' %event_name)
    os.system('rm -rf ../events/%s/DES_metadata.csv' %event_name)
    os.system('rm -rf ../events/%s/exptable.txt' %event_name)
    print("Cleaned existing simulations")

#destroy it all
if mode == 'everything':
    os.system('rm -rf ../events/%s/analysis' %event_name)
    os.system('rm -rf ../events/%s/sims_and_data' %event_name)
    os.system('rm -rf ../events/%s/sim_gen' %event_name)
    os.system('rm -rf ../events/%s/cut_results' %event_name)
    os.system('rm -rf ../events/%s/logs' %event_name)
    os.system('rm -rf ../events/%s/event_metadata.csv' %event_name)
    os.system('rm -rf ../events/%s/DES_metadata.csv' %event_name)
    os.system('rm -rf ../events/%s/exptable.txt' %event_name)
    os.system('rm -rf ../events/%s/report.txt' %event_name)
    print("Clobbered all existing results for %s" %event_name)
