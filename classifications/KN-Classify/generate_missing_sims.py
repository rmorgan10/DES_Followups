# A module to check for existing sims and trigger missing sims

import getpass
import os
import sys
import time

event_name = sys.argv[1]
username = getpass.getuser()

#Check for missing sims
required_sims = ['KN', 'Ia', 'CC', 'AGN', 'CaRT', 'ILOT', 'SN91bg', 'Iax', 'PIa', 'SLSN', 'TDE']
needed_sims = ''
for obj in required_sims:
    if not os.path.exists('../../events/%s/cut_results/%s_DESGW_%s_%s_cut_results.npy' %(event_name, username, event_name, obj)):
        needed_sims += obj
        needed_sims += ','

#Trigger missing sims
if needed_sims != '':
    print("KN-Classify needs to simulate %s\nThe main ipeline will start shortly..." %needed_sims[:-1])
    time.sleep(5)
    os.chdir('../../')
    os.system('python run.py %s --num_agn 10000 --num_kn 10000 --num_mdwarf 10000 --boost 10 --sim_include %s' %(event_name, needed_sims[:-1]))

