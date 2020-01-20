# A module to select the best features for classification

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import sys

event_name = sys.argv[1]
event_dir = '../../events/%s/PSNID' %event_name

# Load, label, and concatenate dataframes
data_df = pd.read_csv('%s/DATA.FITRES' %event_dir, delim_whitespace=True, comment='#')

dfs = []
for obj in ['CC', 'KN', 'Ia']:
    df = pd.read_csv('%s/%s.FITRES' %(event_dir, obj), delim_whitespace=True, comment='#')
    df['CLASS'] = obj
    dfs.append(df)
df = pd.concat(dfs)

# Drop nonnumeric columns or columns with truth information
meaningful_columns = ['PKMJDINI', 'SNRMAX1', 'SNRMAX2', 'SNRMAX3', 'ITYPE_BEST', 'Z_Ia', 'SHAPEPAR_Ia', 
                      'COLORPAR_Ia', 'COLORLAW_Ia', 'TMAX_Ia', 'DMU_Ia', 'TOBSMIN_Ia', 'TOBSMAX_Ia', 
                      'CHI2_Ia', 'NPT_Ia', 'FITPROB_Ia', 'PBAYES_Ia', 'LCQ_Ia', 'Ze_Ia', 'SHAPEPARe_Ia', 
                      'COLORPARe_Ia', 'COLORLAWe_Ia', 'TMAXe_Ia', 'DMUe_Ia', 'PEAKMAG_g_Ia', 'PEAKMAG_r_Ia',
                      'PEAKMAG_i_Ia', 'PEAKMAG_z_Ia', 'Z_Ibc', 'COLORPAR_Ibc', 'COLORLAW_Ibc', 'TMAX_Ibc',
                      'DMU_Ibc', 'TOBSMIN_Ibc', 'TOBSMAX_Ibc', 'CHI2_Ibc', 'NPT_Ibc', 'FITPROB_Ibc',
                      'PBAYES_Ibc', 'LCQ_Ibc', 'PEAKMAG_g_Ibc', 'PEAKMAG_r_Ibc', 'PEAKMAG_i_Ibc', 
                      'PEAKMAG_z_Ibc', 'Z_II', 'COLORPAR_II', 'COLORLAW_II', 'TMAX_II', 'DMU_II', 'TOBSMIN_II',
                      'TOBSMAX_II', 'CHI2_II', 'NPT_II', 'FITPROB_II', 'PBAYES_II', 'LCQ_II', 'PEAKMAG_g_II',
                      'PEAKMAG_r_II', 'PEAKMAG_i_II', 'PEAKMAG_z_II', 'CLASS']
df = df[meaningful_columns].copy().reset_index(drop=True)

# Select 15 features with largest difference between means of the distributions
diff_data = []
for col in meaningful_columns[0:-1]:
    kn_mean = np.mean(df[col].values[df['CLASS'].values == 'KN'])
    sn_mean = np.mean(df[col].values[df['CLASS'].values != 'KN'])
    kn_sn_diff = np.abs((kn_mean - sn_mean) / np.abs(np.mean(df[col].values)))

    diff_data.append([col, kn_sn_diff])

diff_df = pd.DataFrame(data=diff_data, columns=['FEATURE', 'DIFF'])
sorted_diff_df = diff_df.sort_values(by='DIFF', ascending=False)


chosen_feats = list(sorted_diff_df['FEATURE'].values[0:15]) 
feat_df = df[chosen_feats + ['CLASS']].copy().reset_index(drop=True)

#balance classes
feat_df_sn = feat_df[feat_df['CLASS'] != 'KN']
feat_df_kn = feat_df[feat_df['CLASS'] == 'KN']
sample_size = np.min([feat_df_sn.shape[0], feat_df_kn.shape[0]])
feat_df = pd.concat([feat_df_sn.sample(sample_size), feat_df_kn.sample(sample_size)]).copy().reset_index(drop=True)


# Output training and test sets as csv files
X_train, X_test, y_train, y_test = train_test_split(feat_df[chosen_feats], feat_df['CLASS'], test_size=0.3, random_state=6, stratify=feat_df['CLASS'])
out_train_df = pd.concat([X_train, y_train], axis=1)
out_test_df = pd.concat([X_test, y_test], axis=1)

out_train_df.to_csv('%s/training_set.csv' %event_dir, index=False)
out_test_df.to_csv('%s/testing_set.csv' %event_dir, index=False)

# Output featurized data
data_df[chosen_feats + ['CID']].to_csv('%s/data.csv' %event_dir, index=False)
