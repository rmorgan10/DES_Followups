# A module to collect sims for psnid

import getpass
import os
import sys

event_name = sys.argv[1]
sim_include = sys.argv[2]
path = '../../events/%s/sims_and_data' %event_name
username = getpass.getuser()


for obj in sim_include.split(','):
    #copy files
    os.system('cp %s/%s_DESGW_%s_%s_FITS.tar.gz .' %(path, username, event_name, obj))
    #unpack tarballs
    os.system('tar -xzf %s_DESGW_%s_%s_FITS.tar.gz' %(username, event_name, obj))
    #rename files
    os.system('mv %s_DESGW_%s_%s_FITS %s_DESGW_%s_%s' %(username, event_name, obj, username, event_name, obj))

