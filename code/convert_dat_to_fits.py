# A wrapper for the snana fits conversion feature

import os
import sys



event_name = sys.argv[1]
if not os.path.exists('../events/%s/sims_and_data/' %event_name):
    os.system('mkdir sims_and_data')

fits_path = '../events/%s/sims_and_data/LightCurvesReal_FITS' % event_name
if os.path.exists(fits_path):
    os.system('rm -r %s' %fits_path)

os.system('cp -r ../events/%s/sims_and_data/LightCurvesReal .' %event_name)

log_path = '../events/%s/logs' %event_name
if not os.path.exists(log_path):
    os.system('mkdir %s' %log_path)


#check for list, readme, and ignore files
os.system('rm LightCurvesReal/*.IGNORE LightCurvesReal/*.README LightCurvesReal/*.LIST')
os.chdir('LightCurvesReal')
os.system('ls -1 *.dat > LightCurvesReal.LIST')
os.system('touch LightCurvesReal.IGNORE')
os.system('touch LightCurvesReal.README')
os.chdir('..')

dat_path = 'LightCurvesReal'

os.system('snana.exe NOFILE PRIVATE_DATA_PATH %s VERSION_PHOTOMETRY %s VERSION_REFORMAT_FITS %s > %s/convert_dat_to_fits.log' %(dat_path, dat_path, dat_path, log_path))

#clean up code directory
os.system('rm -r LightCurvesReal')
os.system('mkdir FITS_LightCurvesReal')
os.system('mv LightCurvesReal* FITS_LightCurvesReal')
os.system('mv FITS_LightCurvesReal ../events/%s/sims_and_data/LightCurvesReal_FITS' %event_name)
