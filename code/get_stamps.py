# A module to collect the stamps for the candidates

import numpy as np
import os
import pandas as pd
import sys

# Set up event directory
event_name = sys.argv[1]
if not os.path.exists('../events/%s/stamps' %event_name):
    os.system('mkdir ../events/%s/stamps' %event_name)

# Target stamps
dat_file_path_file = open('../events/%s/dat_file_path.txt' %event_name, 'r')
dat_file_path = dat_file_path_file.readlines()[0]
dat_file_path_file.close()
stamp_dir = dat_file_path.split('makedatafiles')[0] + 'stamps/'

# Collect the snids of the candidates
candidate_summary_df = pd.read_csv('../events/%s/cut_results/LightCurvesReal_candidate_summary.txt' %event_name)

### Functions to read a dat file
# Open a file
def open_dat(dat_file):
    infile = open(dat_file, 'r')
    lines = infile.readlines()
    infile.close()
    return lines

# Get phot data for single dat file
def get_terse_lc(lines):

    columns = [y for y in [x.split(' ') for x in lines if x[0:8] == 'VARLIST:'][0] if y != ''][1:-1]
    data = [[y for y in x.split(' ') if y != ''][1:-1] for x in lines if x[0:4] == 'OBS:']
    df = pd.DataFrame(data=data, columns=columns)
    
    for col in columns:
        if col != 'FLT' and col != 'FIELD':
            df[col] = pd.to_numeric(df[col])

    return df

# Iterate through the candidates
for index, row in candidate_summary_df.iterrows():

    # Make a directory for the candidate's stamps
    if not os.path.exists('../events/%s/stamps/%s' %(event_name, str(int(row['SNID'])))):
        os.system('mkdir ../events/%s/stamps/%s' %(event_name, str(int(row['SNID']))))

    # Grab the light curve of the candidate
    lines = open_dat('../events/%s/sims_and_data/LightCurvesReal/des_real_00%s.dat' %(event_name, str(int(row['SNID']))))
    lc = get_terse_lc(lines)

    # Copy the stamps for each observation to an organized directory
    for lc_index, lc_row in lc.iterrows():
        
        # Skip observations without a detection
        if int(lc_row['OBJID']) == 0:
            continue

        # Organize by SNID/NITE/FLT
        if not os.path.exists('../events/%s/stamps/%s/%s' %(event_name, str(int(row['SNID'])), str(int(lc_row['NITE'])))):
            os.system(' mkdir ../events/%s/stamps/%s/%s' %(event_name,str(int(row['SNID'])), str(int(lc_row['NITE']))))
        if not os.path.exists('../events/%s/stamps/%s/%s/%s' %(event_name,str(int(row['SNID'])), str(int(lc_row['NITE'])), str(lc_row['FLT']))):
            os.system(' mkdir ../events/%s/stamps/%s/%s/%s' %(event_name,str(int(row['SNID'])), str(int(lc_row['NITE'])), str(lc_row['FLT'])))

        os.system('cp %s*%s.gif ../events/%s/stamps/%s/%s/%s' %(stamp_dir, str(int(lc_row['OBJID'])), 
                                                                event_name, str(int(row['SNID'])), str(int(lc_row['NITE'])), str(lc_row['FLT'])))
