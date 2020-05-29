# A module to impute ml results into cut results

import numpy as np
import os
import pandas as pd
import sys

event_name = sys.argv[1]
event_dir = '../events/%s/PSNID' %event_name

# load ml results -- use only PSNID for now
kn_df = pd.read_csv('%s/pred_full_KN.csv' %event_dir)
ia_df = pd.read_csv('%s/pred_full_Ia.csv' %event_dir)
cc_df = pd.read_csv('%s/pred_full_CC.csv' %event_dir)

# load classification threshold
stream = open('%s/res_numeric_metrics.txt' %event_dir, 'r')
lines = stream.readlines()
stream.close()
op_threshold = float([x for x in lines if x.find("Operating Threshold") != -1][0].strip().split(' ')[-1])

# load kn_terse_results 
kn_results = pd.read_csv("../events/%s/analysis/%s_kn_terse_cut_results.csv" %(event_name, event_name))


kn_already_cut = kn_results[kn_results['CUT'].values != -1].copy().reset_index(drop=True)
last_cut = int(np.max(kn_already_cut['SNID'].values))
kn_remaining = kn_results[kn_results['CUT'].values == -1].copy().reset_index(drop=True)

out_data = []
cut_index = list(kn_remaining.columns).index('CUT')
cols_before_cut = kn_remaining.columns[0:cut_index]
cols_after_cut = kn_remaining.columns[cut_index + 1:]

for index, row in kn_remaining.iterrows():
    
    if len(kn_df['PROB_KN'].values[kn_df['CID'].values == row['SNID']]) == 0:
        #since PSNID can only handle 20000 at a time, some may be missing classifications
        #just skip these rows for now
        continue

    if kn_df['PROB_KN'].values[kn_df['CID'].values == row['SNID']][0] < op_threshold:
        out_data.append(list(row[cols_before_cut]) + [last_cut + 10] + list(row[cols_after_cut]))
    else:
        out_data.append(list(row))



out_df = pd.DataFrame(data=out_data, columns=kn_remaining.columns)

full_results_df = pd.concat([kn_already_cut, out_df])
full_results_df.to_csv("../events/%s/analysis/%s_kn_terse_cut_results_ml.csv" %(event_name, event_name), index=False)


