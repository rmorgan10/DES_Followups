# A module to extract features from the real data

import numpy as np
import pandas as pd
import sys

import extract_features as extract
import organize

event_name = sys.argv[1]

# Load data
cut_res = np.load('../../events/%s/cut_results/LightCurvesReal_cut_results.npy' %event_name).item()

# Extract features
outfile = '../../events/%s/KNC/DATA_feats.csv'
extract.extract_all_to_csv(cut_res, obj='DATA', outfile)

# Organize by light curve properties
df = pd.read_csv(outfile)
datasets = organize.breakup(df)

# Output organized features
np.save('../../events/%s/KNC/DATA_datasets.npy' %event_name, datasets)
