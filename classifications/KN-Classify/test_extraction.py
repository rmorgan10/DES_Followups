# A module to test feature extraction
# might be able to turn this into a shell when done testing

import pandas as pd

import extract_features as ef
import organize as o


obj = 'KN'
event_name = 'test'

ef.run_extraction(event_name, obj)


print('\n\n')
df = pd.read_csv('../../events/test/KNC/KN_feats.csv')


