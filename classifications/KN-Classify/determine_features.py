# A module to determine the optimal features and write them to a csv

import getpass
import numpy as np
import pandas as pd
import sys

from features import FeatureExtractor

event_name = sys.argv[1]
username = getpass.getuser()
results_dir = '../../events/%s/cut_results/' %event_name

# load kn results and look at a single light curve
kn_res = np.load(results_dir + '%s_DESGW_%s_KN_cut_results.npy' %(username, event_name)).item()

# determine properties of light curves
# nobs and filters
nobs, bands = [], []
for i in range(100):
    lc = list(kn_res.values())[i]['lightcurve']
    cond = (lc['PHOTFLAG'].values > 4095)
    flts, counts = np.unique(lc[cond]['FLT'].values, return_counts=True)
    nobs.append(np.sum(counts))
    bands.append(flts)
lc_bands = bands[np.argmax(np.array([len(x) for x in bands]))]
lc_nobs = np.max(nobs)

#pairs
if len(lc_bands) >= 2:
    pairs = []
    for band_set in bands:
        if len(band_set) == 4:
            pairs.append(['gr', 'ri', 'iz', 'gi', 'gz', 'rz'])
            break

        if len(band_set) == 3:
            missing_band = [x for x in ['g', 'r', 'i', 'z'] if x not in band_set][0]
            missing_dict = {'g': ['ri', 'iz', 'rz'],
                            'r': ['gi', 'gz', 'iz'],
                            'i': ['gr', 'gz', 'rz'],
                            'z': ['gr', 'gi', 'ri']}
            pairs.append(missing_dict[missing_band])
            
        if len(band_set) == 2:
            bit_representation = {'g': 1, 'r': 2, 'i': 4, 'z': 8}
            band_bits = bit_representation[band_set[0]] + bit_representation[band_set[1]]
            band_bit_dict = {3: 'gr', 6: 'ri', 12: 'iz', 5: 'gi', 9: 'gz', 10: 'rz'}
            pairs.append([band_bit_dict[band_bits]])
    lc_pairs = pairs[np.argmax(np.array([len(x) for x in pairs]))]
else:
    lc_pairs = []


### Summary
# Available filter pairs are listed in lc_pairs
# Available filters are listed in lc_bands
# Available number of observations is lc_nobs

#based on lc_pairs, lc_bands, and lc_nobs, find the meaningful features
FExtractor = FeatureExtractor()

#['nobs_brighter_than', 'slope', 'same_nite_color_diff', 'total_color_diff', 'snr', 'flat', 'half', 'mag']
good_families = FExtractor.families
if len(lc_pairs) == 0:
    good_families.remove('same_nite_color_diff')
if len(lc_bands) < 2:
    good_families.remove('total_color_diff')
if lc_nobs < 6:
    good_families.remove('half')
if lc_nobs < 3:
    good_families.remove('flat')
if lc_nobs < 2:
    good_families.remove('slope')

useable_features = []
for feat in FExtractor.features:
    if np.max([feat.find(x) for x in good_families]):
        #feat is allowed



#write to a log file
outlines = ['LC_PAIRS: ' + ','.join(lc_pairs) + '\n',
            'LC_BANDS: ' + ','.join(lc_bands) + '\n',
            'LC_NOBS: ' + str(lc_nobs) + '\n']

outfile = '../../events/%s/logs/KNC_features.log'

