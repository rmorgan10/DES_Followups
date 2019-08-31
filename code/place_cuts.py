# A module to place cuts on light curves

import pandas as pd
import numpy as np
import sys

import cuts

event_name = sys.argv[1]

#parse cut_file
cut_filename = '../events/%s/cuts.csv' %event_name
cut_df = pd.read_csv(cut_filename)

#initialize cutlist object
all_cuts = cuts.CutList().all_cuts

#check that all cuts in cut_df are defined
undefined_cuts = []
for index, row in cut_df.iterrows():
    if row['NAME'] not in all_cuts:
        undefined_cuts.append(row['NAME'])

if len(undefined_cuts) != 0:
    print("ERROR: The following cuts are not defined in cuts.py: ")
    print(undefined_cuts)
    sys.exit()


#load light curve dictionary
data_dict = np.load('../events/%s/LightCurvesReal_PYTHON/LightCurvesReal.npy').item()

#place cuts in order, save snids passing each cut in list files
