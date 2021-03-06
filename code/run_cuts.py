# A shell to place all cuts

import getpass
import os
import sys

event_name = sys.argv[1]
sims_data_both = sys.argv[2]
username = getpass.getuser()


try:
    assert sims_data_both in ['sims', 'data', 'both']
except:
    print("ERROR: Second argument must be in ['sims', 'data', 'both']")
    sys.exit()

# SIMS
if sims_data_both in ['sims', 'both']:

    for obj in ['AGN', 'CC', 'Ia', 'KN']:
        fits_dir_prefix = '%s_DESGW_%s_%s' %(username, event_name, obj)
        
        print("Formatting %s light curves" %obj)
        #if this step is being rerun, the tarball may need to be unpacked  
        if not os.path.exists('../events/%s/sims_and_data/%s_FITS' %(event_name, fits_dir_prefix)):
            os.chdir('../events/%s/sims_and_data/' %event_name)
            os.system('tar -xzf %s_FITS.tar.gz' %fits_dir_prefix)
            os.chdir('../../../code')
        #convert fits files to numpy files
        os.system('python parse_fits.py %s %s ' %(event_name, fits_dir_prefix))
                
        print("Placing cuts on %s simulations" %obj)
        #place cuts on fits files
        if not os.path.exists('../events/%s/cut_results/%s_DESGW_%s_%s_cut_results.npy' %(event_name, username, event_name, obj)):
            os.system('python get_cut_results.py %s %s' %(event_name, fits_dir_prefix))
        else:
            print("Cut results already exist, skipping cuts on %s" %obj)
        
    

# DATA
if sims_data_both in ['data', 'both']:

    fits_dir_prefix = 'LightCurvesReal'

    #convert dat to fits
    print("Reading datafiles")
    if not os.path.exists('../events/%s/sims_and_data/LightCurvesReal_FITS' %event_name):
        os.system('python convert_dat_to_fits.py %s' %event_name)

    print("Formatting data light curves")
    #convert fits files to numpy files
    if not os.path.exists('../events/%s/sims_and_data/LightCurvesReal_PYTHON' %event_name):
        #if this step is being rerun, the tarball may need to be unpacked
        if not os.path.exists('../events/%s/sims_and_data/%s_FITS' %(event_name, fits_dir_prefix)):
            os.chdir('../events/%s/sims_and_data/' %event_name)
            os.system('tar -xzf %s_FITS.tar.gz' %fits_dir_prefix)
            os.chdir('../../../code')
        os.system('python parse_fits.py %s %s' %(event_name, fits_dir_prefix)) 

    print("Placing cuts on data")
    #place cuts on fits files
    if not os.path.exists('../events/%s/cut_results/LightCurvesReal_cut_results.npy' %event_name):
        os.system('python get_cut_results.py %s %s' %(event_name, fits_dir_prefix))
    else:
        print("Cut results already exist, skipping cuts on DATA")
