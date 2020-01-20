# A module to collect sims for psnid

import getpass
import os
import sys

event_name = sys.argv[1]
path = '../../events/%s/sims_and_data' %event_name
username = getpass.getuser()


#copy files
os.system('cp %s/%s_DESGW_%s_KN_FITS.tar.gz .' %(path, username, event_name))
os.system('cp %s/%s_DESGW_%s_Ia_FITS.tar.gz .' %(path, username, event_name))
os.system('cp %s/%s_DESGW_%s_CC_FITS.tar.gz .' %(path, username, event_name))

#unpack tarballs
os.system('tar -xzf %s_DESGW_%s_KN_FITS.tar.gz' %(username, event_name))
os.system('tar -xzf %s_DESGW_%s_Ia_FITS.tar.gz' %(username, event_name))
os.system('tar -xzf %s_DESGW_%s_CC_FITS.tar.gz' %(username, event_name))

#rename files
os.system('mv %s_DESGW_%s_KN_FITS %s_DESGW_%s_KN' %(username, event_name, username, event_name))
os.system('mv %s_DESGW_%s_Ia_FITS %s_DESGW_%s_Ia' %(username, event_name, username, event_name))
os.system('mv %s_DESGW_%s_CC_FITS %s_DESGW_%s_CC' %(username, event_name, username, event_name))
