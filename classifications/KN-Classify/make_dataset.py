# A script to make a full training set

import numpy as np
import pandas as pd
import sys

import extract_features as extract
import organize

event_name = sys.argv[1]
obj = sys.argv[2]

# Get features from light curves
extract.run_extraction(event_name, obj)

# Load featurized data
df = pd.read_csv('../../events/%s/KNC/%s_feats.csv' %(event_name, obj))

# Organize by light curve properties
datasets = organize.breakup(df)

# Save results
np.save('../../events/%s/KNC/%s_datasets.npy' %(event_name, obj), datasets)
