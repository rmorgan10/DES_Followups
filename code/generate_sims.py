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
sim_path = '../events/%s/sim_gen' % event_name
if os.path.exists(sim_path):
    os.system('rm -r %s' %sim_path)
os.system('mkdir %s' %sim_path)

"""
#clobber existing sims
if os.path.exists('../events/%s/sims_and_data' % event_name):

    #instead of clobbering, just exit so that run.py moves on to the next part
    #print("Existing simulations found! moving to light curve formatting stage")
    #sys.exit()
    pass
    ###save data from being deleted if it is in there
    ##if os.path.exists('../events/%s/sims_and_data/LightCurvesReal' %event_name):
    ##    os.system('mv ../events/%s/sims_and_data/LightCurvesReal ../events/%s' %(event_name, event_name))
    ##    os.system('rm -r ../events/%s/sims_and_data' %event_name)
    ##    os.system('mkdir ../events/%s/sims_and_data' %event_name)
    ##    os.system('mv ../events/%s/LightCurvesReal ../events/%s/sims_and_data' %(event_name, event_name))
    ##else:
    ##    os.system('rm -r ../events/%s/sims_and_data' %event_name)
    ##    os.system('mkdir ../events/%s/sims_and_data' %event_name)
else:
    os.system('mkdir ../events/%s/sims_and_data' %event_name)

"""

log_path = '../events/%s/logs' %event_name
if not os.path.exists(log_path):
    os.system('mkdir %s' %log_path)


if not os.path.exists('../events/%s/sim_gen/SIMLIB.txt' %event_name):
    print("Querying DB for observing conditions")
    #call makeSimlib_easyaccess.py
    os.system('python makeSimlib_easyaccess.py -o "../events/%s/sim_gen/SIMLIB_raw.txt"' %event_name + 
          ' --exptable "../events/%s/exptable.txt"' %event_name +
          ' --min_ra %.1f --max_ra %.1f --min_dec %.1f --max_dec %.1f > %s/make_simlib.log' %(df['MIN_RA'].values[0], df['MAX_RA'].values[0],
                                                                         df['MIN_DEC'].values[0], df['MAX_DEC'].values[0], log_path))

    #call clean_simlib.py
    os.system('python clean_simlib.py ../events/%s/sim_gen/SIMLIB_raw.txt ../events/%s/sim_gen/SIMLIB.txt' %(event_name, event_name))
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
### AGN
if not os.path.exists('sims_and_data/%s_DESGW_%s_AGN_FITS' %(username, event_name)):
    print("Simulating AGN")
    os.system('snlc_sim.exe sim_gen/AGN_SIMGEN.INPUT > logs/sim_agn.log')
    os.system('mv ' + sim_dir_prefix + 'AGN  sims_and_data/%s_DESGW_%s_AGN_FITS' %(username, event_name))
else:
    print("AGN sims done!")
### KN
if not os.path.exists('sims_and_data/%s_DESGW_%s_KN_FITS' %(username, event_name)):
    print("Simulating KNe")
    os.system('snlc_sim.exe sim_gen/SIMGEN_DES_KN.input > logs/sim_kn.log')
    os.system('mv ' + sim_dir_prefix + 'KN  sims_and_data/%s_DESGW_%s_KN_FITS' %(username, event_name))
else:
    print("KN sims done!")
### CC
if not os.path.exists('sims_and_data/%s_DESGW_%s_CC_FITS' %(username, event_name)):
    print("Simulating SNe-CC")
    os.system('snlc_sim.exe sim_gen/SIMGEN_DES_NONIA.input > logs/sim_cc.log')
    os.system('mv ' + sim_dir_prefix + 'CC  sims_and_data/%s_DESGW_%s_CC_FITS' %(username, event_name))
else:
    print("CC sims done!")

### Ia
if not os.path.exists('sims_and_data/%s_DESGW_%s_Ia_FITS' %(username, event_name)):
    print("Simulating SNe-Ia")
    os.system('snlc_sim.exe sim_gen/SIMGEN_DES_SALT2.input > logs/sim_ia.log')
    os.system('mv ' + sim_dir_prefix + 'Ia  sims_and_data/%s_DESGW_%s_Ia_FITS' %(username, event_name))
else:
    print("Ia sims done!")

#tar sims directory when finished
#os.system('tar -czf sims.tar.gz sims_and_data')

##instead, tar the sim directories individually after parsing them in parse_fits.py
