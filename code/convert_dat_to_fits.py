# A wrapper for the snana fits conversion feature

import os
import sys

#dat_path = sys.argv[1]

event_name = sys.argv[1]
fits_path = '../events/%s/LightCurvesReal_FITS' % event_name
if os.path.exists(fits_path):
    os.system('rm -r %s' %fits_path)

os.system('cp -r ../events/%s/LightCurvesReal .' %event_name)

#check for list, readme, and ignore files
os.system('rm LightCurvesReal/*.IGNORE LightCurvesReal/*.README LightCurvesReal/*.LIST')
os.chdir('LightCurvesReal')
os.system('ls -1 *.dat > LightCurvesReal.LIST')
os.system('touch LightCurvesReal.IGNORE')
os.system('touch LightCurvesReal.README')
os.chdir('..')

dat_path = 'LightCurvesReal'

os.system('snana.exe NOFILE PRIVATE_DATA_PATH %s VERSION_PHOTOMETRY %s VERSION_REFORMAT_FITS %s' %(dat_path, dat_path, dat_path))

#clean up code directory
os.system('rm -r LightCurvesReal')
os.system('mkdir FITS_LightCurvesReal')
os.system('mv LightCurvesReal* FITS_LightCurvesReal')
os.system('mv FITS_LightCurvesReal ../events/%s/LightCurvesReal_FITS' %event_name)
