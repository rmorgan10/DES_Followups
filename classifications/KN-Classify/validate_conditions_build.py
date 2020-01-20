# A module to manage the creation of training sets of all conditions

import numpy as np
import os
import pandas as pd
import socket
import sys


event_name = sys.argv[1]
computer = socket.gethostname().split('.')[0]

if not os.path.exists('../../events/%s/KNC_validation' %event_name):
    os.system('mkdir ../../events/%s/KNC_validation' %event_name)

if not os.path.exists('../../events/%s/KNC_validation/datasets' %event_name):
    os.system('mkdir ../../events/%s/KNC_validation/datasets' %event_name)

# Specify and save allowed values    
seeing_values = [str(round(x, 2)) for x in np.linspace(0.5, 3.0, 5)]
skymag_values = [str(round(x, 2)) for x in np.linspace(24.0, 34.0, 5)]
deltat_values = [str(round(x, 2)) for x in np.linspace(1., 19., 5)]
allowed_conditions = {'SEEING': seeing_values,
                      'SKYMAG': skymag_values,
                      'DELTAT': deltat_values}
np.save('allowed_conditions.npy', allowed_conditions)
del allowed_conditions

# Use all available computers
index = 1000
last_index_finished = 1103
computers = ['des30', 'des31', 'des40']
conditions = [] 
missing_indices = [1092, 1096, 1100]
computer_index = 0
for seeing in seeing_values:
    for skymag in skymag_values:
        for deltat in deltat_values:
            # Don't repeat jobs that have already finished
            if index <= last_index_finished and index not in missing_indices:
                index += 1
                continue

            # Build up DataFrame of jobs to be run
            conditions.append([str(index), seeing, skymag, deltat, computers[computer_index]])
            index += 1
            computer_index += 1

            # Restart computer index once all computers have been used
            if computer_index == len(computers):
                computer_index = 0

running_df = pd.DataFrame(data=conditions, columns=['INDEX', 'SEEING', 'SKYMAG', 'DELTAT', 'CPU'])


# Create log file
outfile = open('../../events/%s/KNC_validation/conditions_map.txt' %event_name, 'w+')
outfile.write('INDEX  SEEING  SKYMAG  DELTAT\n')
outfile.close()

# Change to DES_Followups directory to run full pipeline
os.chdir('../..')

# Set simulation global properties
boost = 10
num_kn = 10000
num_agn = 10000
num_mdwarf = 1000
sim_include = 'all'

# Generate a training set for each set of observing conditions
select_df = running_df[running_df['CPU'].values == computer].copy().reset_index(drop=True)
for index, row in select_df.iterrows():
    r = row.copy()
    seeing = r['SEEING']
    skymag = r['SKYMAG']
    deltat = r['DELTAT']
    index = r['INDEX']

    # Run the pipeline to generate sims
    os.system('python run.py %s ' %event_name +
              '--boost %s ' %boost +
              '--num_kn %s ' %num_kn +
              '--num_agn %s ' %num_agn +
              '--num_mdwarf %s ' %num_mdwarf +
              '--sim_include %s ' %sim_include +
              '--force_conditions %s,%s,%s '%(seeing, skymag, deltat))

    # Change to classification directory
    os.chdir('classifications/KN-Classify/')

    # Build training set
    os.system('python make_all_datasets.py %s ' %event_name +
              'KN,Ia,CC,AGN,CaRT,ILOT,Mdwarf,SN91bg,Iax,PIa,SLSN,TDE')

    # Change to event/KNC directory to rename training set
    os.chdir('../../events/%s' %event_name)
                      
    # Move training set to save it
    err = os.system('mv KNC/training_data.npy KNC_validation/datasets/ts_%s.npy' %index)

    # Track training set properties
    outfile = open('KNC_validation/conditions_map.txt', 'a')
    outfile.write('%s\t%s\t%s\t%s\n' %(index, seeing, skymag, deltat))
    outfile.close()

    # Clean up event directory
    if err == 0:
        os.system('rm -rf cut_results sims_and_data report.txt KNC event_metadata.csv exptable.txt DES_metadata.csv logs sim_gen')

    # Change back to DES_Followups directory for next iteration
    os.chdir('../..')


# Done building training sets, now we need to classify
os.chdir('classifications/KN-Classify')

#os.system('python validate_conditions_classify.py %s all' %event_name)
