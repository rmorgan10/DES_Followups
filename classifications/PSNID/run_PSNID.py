# A shell to collect sims and data and then trigger psnid

import datetime
import getpass
import numpy as np
import os
import pandas as pd
import random
import sys
import time

event_name = sys.argv[1]
try:
    cutoff = int(sys.argv[2])
except:
    print("second command line argument must be an integer")
    sys.exit()
username = getpass.getuser()

print("Updating PSNID input files")
# update paths in PSNID files
modes = {'DATA': {'filename': 'psnid_DATA.nml', 'version': 'VERSION: LightCurvesReal', 'list': "   SNCID_LIST_FILE = 'good_snids_DATA.txt'"},
         'Ia': {'filename': 'psnid_Ia.nml', 'version': 'VERSION: %s_DESGW_%s_Ia' %(username, event_name), 'list': "   SNCID_LIST_FILE = 'good_snids_Ia.txt'"},
         'CC': {'filename': 'psnid_CC.nml', 'version': 'VERSION: %s_DESGW_%s_CC' %(username, event_name), 'list': "   SNCID_LIST_FILE = 'good_snids_CC.txt'"},
         'KN': {'filename': 'psnid_KN.nml', 'version': 'VERSION: %s_DESGW_%s_KN' %(username, event_name), 'list': "   SNCID_LIST_FILE = 'good_snids_KN.txt'"}}

for obj, mode in modes.iteritems():
    stream = open('template_psnid.nml', 'r')
    lines = stream.readlines()
    stream.close()

    outlines = []
    for line in lines:
        if line.find('PRIVATE_DATA_PATH') != -1:
            outlines.append(line.split('REPLACEME')[0] + os.getcwd() + "'\n")
        elif line[0:8] == 'VERSION:':
            outlines.append(mode['version'] + '\n')
        elif line.find('SNCID_LIST_FILE') != -1:
            outlines.append(mode['list'] + '\n')
        elif line[0:7] == 'OUTDIR:':
            outlines.append('OUTDIR:  OUTPUT_%s\n' %obj)
        else:
            outlines.append(line)

    stream = open(mode['filename'], 'w+')
    stream.writelines(outlines)
    stream.close()


#garb = raw_input("Waiting...")
print("Collecting simulations")
# collect sims
os.system('python get_sims.py %s' %event_name)

#make good snid lists for sims
print("Making good snid lists")
for obj in ['Ia', 'CC', 'KN']:
    print(obj)
    good_snids = []
    d = np.load('../../events/%s/cut_results/%s_DESGW_%s_%s_cut_results.npy' %(event_name, username, event_name, obj)).item()
    for snid, info in d.iteritems():
        if int(info['cut']) > cutoff or int(info['cut']) == -1:
            good_snids.append(int(snid))

    del d

    if len(good_snids) > 20000:
        good_snids = random.sample(good_snids, k=20000)

    stream = open('good_snids_%s.txt' %obj, 'w+')
    stream.writelines([str(x) + '\n' for x in good_snids])
    stream.close()



#garb = raw_input("Waiting...")
print("Collecting data")
# collect data
os.system('python get_candidates.py %s %i' %(event_name, cutoff))

#run psnid
for obj, mode in modes.iteritems():
    os.system('split_and_fit.pl %s' %mode['filename'])
    print("Running PSNID on %s. Started at %s" %(obj, datetime.datetime.now().strftime('%H:%M')))

    time.sleep(60)
    done = False
    while not done:
        time.sleep(10)

        stream = open('OUTPUT_%s/MERGE.LOG' %obj, 'r')
        lines = stream.readlines()
        stream.close()

        done = len([x for x in lines if x.find('MERGED') != -1]) == 1

    time.sleep(60)
    if not os.path.exists('OUTPUT_%s/SPLIT_JOBS_LCFIT.tar.gz' %obj):
        print("Error in fitting simulations")
        sys.exit()


#garb = raw_input("Waiting...")
print("Cleaning up...")
# clean up
os.system('rm psnid_DATA.nml')
os.system('rm psnid_KN.nml')
os.system('rm psnid_Ia.nml')
os.system('rm psnid_CC.nml')

os.system('rm good_snids_*.txt')

event_dir = '../../events/%s/PSNID' %event_name
if not os.path.exists(event_dir):
    os.system('mkdir %s' %event_dir)


os.system('mv OUTPUT_KN/%s_DESGW_%s_KN/FITOPT000.FITRES %s/KN.FITRES' %(username, event_name, event_dir))
os.system('mv OUTPUT_Ia/%s_DESGW_%s_Ia/FITOPT000.FITRES %s/Ia.FITRES' %(username, event_name, event_dir))
os.system('mv OUTPUT_CC/%s_DESGW_%s_CC/FITOPT000.FITRES %s/CC.FITRES' %(username, event_name, event_dir))
os.system('mv OUTPUT_DATA/LightCurvesReal/FITOPT000.FITRES %s/DATA.FITRES' %event_dir)

os.system('rm -rf OUTPUT_*')

os.system('rm %s_DESGW_%s_CC_FITS.tar.gz' %(username, event_name))
os.system('rm %s_DESGW_%s_KN_FITS.tar.gz' %(username, event_name))
os.system('rm %s_DESGW_%s_Ia_FITS.tar.gz' %(username, event_name))

os.system('rm -rf %s_DESGW_%s_CC' %(username, event_name))
os.system('rm -rf %s_DESGW_%s_KN' %(username, event_name))
os.system('rm -rf %s_DESGW_%s_Ia' %(username, event_name))
os.system('rm -rf LightCurvesReal')

print("Done!")
