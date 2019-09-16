# A module to parse cut summary files and print a nice table

import getpass
import numpy as np
import os
import pandas as pd
import sys

import utils

event_name = sys.argv[1]
os.chdir('../events/%s/cut_results' %event_name)
username = getpass.getuser()

#check for existence of summary files
if not os.path.exists('%s_DESGW_%s_AGN_cut_summary.txt' %(username, event_name)):
    print("ERROR: AGN cut summary file is missing.")
    sys.exit()

if not os.path.exists('%s_DESGW_%s_KN_cut_summary.txt' %(username, event_name)):
    print("ERROR: KN cut summary file is missing.")
    sys.exit()

if not os.path.exists('%s_DESGW_%s_Ia_cut_summary.txt' %(username, event_name)):
    print("ERROR: SN-Ia cut summary file is missing.")
    sys.exit()

if not os.path.exists('%s_DESGW_%s_CC_cut_summary.txt' %(username, event_name)):
    print("ERROR: SN-CC cut summary file is missing.")
    sys.exit()

if not os.path.exists('LightCurvesReal_cut_summary.txt'):
    print("ERROR: LightCurvesReal cut summary file is missing.")
    sys.exit()

#Read and format cut summary files
agn_results = pd.read_csv('%s_DESGW_%s_AGN_cut_summary.txt' %(username, event_name), delim_whitespace=True)
agn_results['AGN'] = agn_results['REMAINING'].values
agn_results = agn_results.drop('REMAINING', axis=1)
kn_results = pd.read_csv('%s_DESGW_%s_KN_cut_summary.txt' %(username, event_name), delim_whitespace=True)
kn_results['KN'] = kn_results['REMAINING'].values
kn_results = kn_results.drop('REMAINING', axis=1)
ia_results = pd.read_csv('%s_DESGW_%s_Ia_cut_summary.txt' %(username, event_name), delim_whitespace=True)
ia_results['Ia'] = ia_results['REMAINING'].values
ia_results = ia_results.drop('REMAINING', axis=1)
cc_results = pd.read_csv('%s_DESGW_%s_CC_cut_summary.txt' %(username, event_name), delim_whitespace=True)
cc_results['CC'] = cc_results['REMAINING'].values
cc_results = cc_results.drop('REMAINING', axis=1)
data_results = pd.read_csv('LightCurvesReal_cut_summary.txt', delim_whitespace=True)
data_results['DATA'] = data_results['REMAINING'].values
data_results = data_results.drop('REMAINING', axis=1)

#make a df that will have all the raw counts of the cutflow
df = data_results.merge(kn_results, on=['CUT', 'NAME']).merge(ia_results, on=['CUT', 'NAME']).merge(cc_results, on=['CUT', 'NAME']).merge(agn_results, on=['CUT', 'NAME'])

#incorporate expected rates of objects
event_info = pd.read_csv('../event_metadata.csv')

##use boost to scale the number of SNe
boost = float(event_info['BOOST'].values[0])

##read uncertainty on SNe numbers from log files
ia_log = open('../logs/sim_ia.log', 'r')
lines = ia_log.readlines()
ia_log.close()
ia_unc = float([y for y in [x for x in lines[-20:] if x[0:39] == '  Number of SNe per season AFTER CUTS :'][0].split(' ') if y != '' and y != '\n'][-1]) / boost

cc_log = open('../logs/sim_cc.log', 'r')
lines = cc_log.readlines()
cc_log.close()
cc_unc = float([y for y in [x for x in lines[-200:] if x[0:39] == '  Number of SNe per season AFTER CUTS :'][0].split(' ') if y != '' and y != '\n'][-1]) / boost


##use prob kn to scale the number of KN
prob_KN = event_info['LIGO_prob_KN'].values[0]

##use effective area to scale the number of agn
simlib_file = open('../sim_gen/SIMLIB.txt', 'r')
lines = simlib_file.readlines()
simlib_file.close()
eff_area = float([x for x in lines[-5:] if x[0:15] == 'EFFECTIVE_AREA:'][0].split(' ')[1][0:-1])

#AGN
agn_cut_results = np.load('%s_DESGW_%s_AGN_cut_results.npy' %(username, event_name)).item()
agn_scaled = []
err_plus = []
err_minus = []
##use limiting mag to scale the number of agn
for cutnum in [int(x) for x in np.arange(len(df['CUT'].values))]:

    means, upper_errs, lower_errs = [], [], []
    for flt in ['g', 'r', 'i', 'z']:
        if int(event_info[flt].values[0]) == 1:
            try:
                num_agn, [num_agn_plus_unc, num_agn_minus_unc] = utils.calc_expected_agn_using_mag_eff(event_info, eff_area, agn_cut_results, flt, cutnum)
            except:
                num_agn, num_agn_plus_unc, num_agn_minus_unc = 0.0, 0.0, 0.0

            means.append(num_agn)
            upper_errs.append(num_agn_plus_unc)
            lower_errs.append(num_agn_minus_unc)

    agn_scaled.append(np.mean(means))
    err_plus.append(np.sqrt(np.sum(np.power(np.array(upper_errs), 2))) / len(means))
    err_minus.append(np.sqrt(np.sum(np.power(np.array(lower_errs), 2))) / len(means))


df['AGN_scaled'] = agn_scaled
df['AGN_scaled_err_plus'] = err_plus
df['AGN_scaled_err_minus'] = err_minus

print(df[['AGN_scaled', 'AGN_scaled_err_plus', 'AGN_scaled_err_minus']])

## Ia
ia_scaled = [df['Ia'].values[0] / boost]
err_plus = [ia_unc / boost]
err_minus = [ia_unc / boost]
for value in df['Ia'].values[1:]:
    eff, [err_high, err_low] = utils.confidenceInterval(n=ia_scaled[-1] * boost, k=value)
    ia_scaled.append(value / boost)
    err_plus.append(eff * np.sqrt((err_high / boost) ** 2 + (err_plus[-1]) ** 2))
    err_minus.append(eff * np.sqrt((err_low /boost) ** 2 + (err_minus[-1]) ** 2))

df['Ia_scaled'] = ia_scaled
df['Ia_scaled_err_plus'] = err_plus
df['Ia_scaled_err_minus'] = err_minus

print(df[['Ia_scaled', 'Ia_scaled_err_plus', 'Ia_scaled_err_minus']])

## CC
cc_scaled = [df['CC'].values[0] / boost]
err_plus = [cc_unc / boost]
err_minus = [cc_unc / boost]
for value in df['CC'].values[1:]:
    eff, [err_high, err_low] = utils.confidenceInterval(n=cc_scaled[-1] * boost, k=value)
    cc_scaled.append(value / boost)
    err_plus.append(eff * np.sqrt((err_high / boost) ** 2 + (err_plus[-1]) ** 2))
    err_minus.append(eff * np.sqrt((err_low /boost) ** 2 + (err_minus[-1]) ** 2))

df['CC_scaled'] = cc_scaled
df['CC_scaled_err_plus'] = err_plus
df['CC_scaled_err_minus'] = err_minus

print(df[['CC_scaled', 'CC_scaled_err_plus', 'CC_scaled_err_minus']])

## KN
num_kn = float(event_info['NUM_KN'].values[0]) * event_info['LIGO_prob_KN'].values[0]
kn_eff = [1.0]
err_plus = [0.0]
err_minus = [0.0]
for value in df['KN'].values[1:]:
    eff, [err_high, err_low] = utils.confidenceInterval(n=kn_eff[-1] * num_kn, k=value)
    kn_eff.append(eff * kn_eff[-1])
    err_plus.append(eff * np.sqrt((err_high) ** 2 + (err_plus[-1]) ** 2))
    err_minus.append(eff * np.sqrt((err_low) ** 2 + (err_minus[-1]) ** 2))

df['KN_scaled'] = kn_eff
df['KN_scaled_err_plus'] = err_plus
df['KN_scaled_err_minus'] = err_minus

print(df[['KN_scaled', 'KN_scaled_err_plus', 'KN_scaled_err_minus']])

## Data
remaining = [df['DATA'].values[0]]
err_plus = [0.0]
err_minus = [0.0]
for value in df['DATA'].values[1:]:
    remaining.append(value)
    eff, [err_high, err_low] = utils.confidenceInterval(n=remaining[-1], k=value)
    err_plus.append(err_high)
    err_minus.append(err_low)

df['DATA_err_plus'] = err_plus
df['DATA_err_minus'] = err_minus

print(df[['DATA', 'DATA_err_plus', 'DATA_err_minus']])

df.to_csv('MERGED_CUT_RESULTS.csv')
