# A module to execute cuts on an individual transient simulation

import getpass
import os
import sys

event_name = sys.argv[1]
username = getpass.getuser()
obj = sys.argv[2]


fits_dir_prefix = '%s_DESGW_%s_%s' %(username, event_name, obj)

if not os.path.exists('../events/%s/sims_and_data/%s_DESGW_%s_%s_PYTHON' %(event_name, username, event_name, obj)):
    print("Formatting %s light curves" %obj)
    #if this step is being rerun, the tarball may need to be unpacked  
    if not os.path.exists('../events/%s/sims_and_data/%s_FITS' %(event_name, fits_dir_prefix)):
        os.chdir('../events/%s/sims_and_data/' %event_name)
        os.system('tar -xzf %s_FITS.tar.gz' %fits_dir_prefix)
        os.chdir('../../../code')
    #convert fits files to numpy files
    os.system('python parse_fits.py %s %s ' %(event_name, fits_dir_prefix))
else:
    print("Formatted %s light curves already exist, skipping" %obj)

#place cuts on fits files
if not os.path.exists('../events/%s/cut_results/%s_DESGW_%s_%s_cut_results.npy' %(event_name, username, event_name, obj)):
    print("Cutting simulations")
    os.system('python get_cut_results.py %s %s' %(event_name, fits_dir_prefix))
else:
    print("Cut results already exist, skipping cuts on %s" %obj)


#make a done file in the log directory
os.system('touch ../events/%s/logs/run_cuts_%s.DONE' %(event_name, obj))
