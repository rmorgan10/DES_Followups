# A module to manage the creation of training sets of all conditions

import numpy as np
import os
import sys


event_name = sys.argv[1]

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

# Create log file
outfile = open('../../events/%s/KNC_validation/conditions_map.txt', 'w+')
outfile.write('INDEX  SEEING  SKYMAG  DELTAT\n')
outfile.close()

# Change to DES_Followups directory to run full pipeline
os.chdir('../..')

boost = 10
num_kn = 10000
num_agn = 10000
num_mdwarf = 10000
sim_include = 'all'

index = 1000
# Generate a training set for each set of observing conditions
for seeing in seeing_values:
    for skymag in skymag_values:
        for deltat in deltat_values:

            # Run the pipeline to generate sims
            os.system('python run.py %s ' %event_name +
                      '--boost %s ' %boost +
                      '--num_kn %s ' %num_kn +
                      '--num_agn %s ' %num_agn +
                      '--num_mdwarf %s ' %num_mdwarf +
                      '--sim_include %s ' %sim_include +
                      '--force_conditions %s,%s,%s '%(seeing, skymag, deltat)
                      )

            # Change to classification directory
            os.chdir('classifications/KN-Classify/')

            # Build training set
            os.system('python make_all_datasets.py %s ' %event_name +
                      'KN,Ia,CC,AGN,CaRT,ILOT,Mdwarf,SN91bg,Iax,PIa,SLSN,TDE')

            # Change to event/KNC directory to rename training set
            os.chdir('../../events/%s' %event_name)
                      
            # Move training set to save it
            os.system('mv KNC/training_data.npy KNC_validation/datasets/ts_%s.npy' %index)

            # Track training set properties
            outfile = open('KNC_validation/conditions_map.txt', 'a')
            outfile.write('%i\t%s\t%s\t%s\n' %(index, seeing, skymag, deltat))
            outfile.close()

            # Clean up event directory
            os.system('rm -rf cut_results sims_and_data report.txt KNC event_metadata.csv exptable.txt DES_metadata.csv')

            # Update index
            index += 1

            # Change back to DES_Followups directory for next iteration
            os.chdir('../..')

            # Run once for testing
            break
        break
    break


# Done building training sets, now we need to classify
os.chdir('classifications/KN-Classify')

os.system('python validate_conditions_classify.py %s all' %event_name)
