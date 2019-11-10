# A module to run cross classificaitons on different training sets

import numpy as np
import pandas as pd
import sys

from classify import classify

event_name = sys.argv[1]
mode = sys.argv[2]
assert mode in ['good', 'fair', 'poor', 'all']

# Load allowable values
allowed_conditions = np.load('allowed_conditions.npy').item()
seeing_values = allowed_conditions['SEEING']
skymag_values = allowed_conditions['SKYMAG']
deltat_values = allowed_conditions['DELTAT']
del allowed_conditions

# Read index file into dict
df = pd.read_csv('../../events/%s/KNC_validation/conditions_map.txt' %event_name, delim_whitespace=True)
df = df.apply(pd.to_numeric)
condition_dict = {}
for index, row in df.iterrows():
    r = row.copy()
    condition_dict[r['INDEX']] = {'SEEING': r['SEEING'],
                                  'SKYMAG': r['SKYMAG'],
                                  'DELTAT': r['DELTAT']}

# reverse the dictionary for quick lookup
index_dict = {'%.2f_%.2f_%.2f' %(float(info['SEEING']), float(info['SKYMAG']), float(info['DELTAT'])): index for index, info in condition_dict.iteritems()}



def run(mode, fixed_seeing, fixed_skymag, fixed_delta_t, event_name=event_name, index_dict=index_dict, seeing_values=seeing_values, skymag_values=skymag_values, deltat_values=deltat_values):
    assert mode != 'all'
    
    # Variable seeing, fixed skymag and deltat
    seeing_outfile = open('../../events/%s/KNC_validation/seeing_%s_results.txt' %(event_name, mode), 'w+')
    seeing_outfile.write('TRAINING\tTESTING\SCORE\n')
    seeing_outfile.close()

    for train_seeing in seeing_values:

        #load training set corresponding to conditions
        train_cond_string = '%.2f' %train_seeing + '_' + fixed_skymag + '_' + fixed_deltat
        cond_index = index_dict[train_cond_string]
        training_set = np.load('../../events/%s/KNC_validation/datasets/ts_%s.npy' %(event_name, cond_index)).item()

        #load all test sets into memory that we will classify based on this training set
        test_sets = {}
        for test_seeing in seeing_values:
            cond_string = '%.2f' %test_seeing + '_' + fixed_skymag + '_' + fixed_deltat
            cond_index = index_dict[cond_string]
            test_sets['%.2f' %test_seeing] = np.load('../../events/%s/KNC_validation/datasets/ts_%s.npy' %(event_name, index)).item()

        # For each training set, collect and classify like test sets
        all_auc_scores, all_samples, all_test_cond_strings = [], [], []
        for code, train_df in training_set.iteritems():
            #collect like test sets
            test_dfs, outfiles, report_files, test_cond_strings = [], [], [], []
            for test_seeing in test_sets.keys():
                test_cond_string = test_seeing + '_' + good_skymag + '_' + good_deltat
                #poor observing conditions may lead to all light curves for a given code being cut out
                try:
                    test_dfs.append(test_sets[test_seeing][code])
                except:
                    #put in placeholder df and flag row
                    test_dfs.append(train_df)
                    test_cond_string += 'BAD'
                    
                test_cond_strings.append(test_cond_string)
                outfiles.append('../../events/%s/KNC_validation/garb.csv' %event_name)
                report_files.append('../../events/%s/KNC_validation/garb.txt' %event_name)

            auc_scores, samples = classify(train_df, test_dfs, outfiles, report_files, n_jobs=-1, output_auc=True)
            all_auc_scores.append(auc_scores)
            all_samples.append(samples)
            all_test_cond_strings.append(test_cond_strings)

        # Restructure lists and load into dataframe
        data = []
        for ii in range(len(all_test_cond_strings)):
            for jj in range(len(all_auc_scores[ii])):
                data.append([all_test_cond_strings[ii], all_auc_scores[ii][jj], all_samples[ii][jj]])
        out_df = pd.DataFrame(data=data, columns=['TEST_COND', 'AUC', 'SAMPLES'])

        # Drop rows that were flagged earlier due to missing data
        good_indices = [int(x) for x in np.linspace(0, out_df.shape[0], out_df.shape[0]) if out_df['TEST_COND'].values[x].find('BAD') == -1]
        out_df = out_df.iloc[good_indices].reset_index(drop=True).copy()

        # Reduce to final scores and save
        for test_cond in np.unique(out_df['TEST_COND'].values):
            partial_df = out_df[out_df['TEST_COND'].values == test_cond]
            score = np.dot(partial_df['AUC'].values, partial_df['SAMPLES'].values) / np.sum(partial_df['SAMPLES'].values)
            
            seeing_outfile = open('../../events/%s/KNC_validation/seeing_%s_results.txt' %(event_name, mode), 'a')
            seeing_outfile.write('%s\t%s\t%s\n' %(train_cond_string, test_cond, score))
            seeing_outfile.close()

    return
    # if that worked, duplicate above code for variable skymag and for variable deltat


if mode in ['good', 'all']:

    good_seeing = '%.2f' %np.min(df['SEEING'].values)
    good_skymag = '%.2f' %np.max(df['SKYMAG'].values)
    good_deltat = '%.2f' %np.min(df['DELTAT'].values)

    run('good', good_seeing, good_skymag, good_delta_t)

if mode in ['fair', 'all']:

    fair_seeing = '%.2f' %sorted(df['SEEING'].values)[int(float(df.shape[0]) / 2)]
    fair_skymag = '%.2f' %sorted(df['SKYMAG'].values)[int(float(df.shape[0]) / 2)]
    fair_deltat = '%.2f' %sorted(df['DELTAT'].values)[int(float(df.shape[0]) / 2)]

    run('fair', fair_seeing, fair_skymag, fair_deltat)

if mode in ['poor', 'all']:

    poor_seeing = '%.2f' %np.max(df['SEEING'].values)
    poor_skymag = '%.2f' %np.min(df['SKYMAG'].values)
    poor_deltat = '%.2f' %np.max(df['DELTAT'].values)

    run('good', poor_seeing, poor_skymag, poor_delta_t)
