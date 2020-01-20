# A module to average all light curves passing cuts

import numpy as np
import pandas as pd
import sys

event_name = sys.argv[1]
obj = sys.argv[2]

event_metadata = pd.read_csv('../events/%s/event_metadata.csv' %event_name)
mjd_explode = event_metadata['MJD_EXPLODE'].values[0]

df = pd.read_csv('../events/%s/analysis/%s_lc_data.csv' %(event_name, obj))
df = df[np.array(df['FLUXCAL'].values, dtype=float) > 0.0].copy().reset_index(drop=True)

nite_data = [int(round(x)) for x in np.array(df['MJD'].values, dtype=float)]
df['NITE'] = nite_data
df['MAG'] = 27.5 - 2.5 * np.log10(df['FLUXCAL'].values)
df['MAGERR'] = np.abs(27.5 - 2.5 * np.log10(df['FLUXCAL'].values + df['FLUXCALERR'].values) - df['MAG'].values)

def get_lc(df, mjd_explode):
    #get the mean light curve for an individual group

    bands = np.unique(df['FLT'].values)
    nites = np.unique(df['NITE'].values)

    for flt in bands:
        
        flt_df = df[df['FLT'].values == flt].copy().reset_index(drop=True)
        
        days_after_trigger = []
        days_after_trigger_err = []
        mean_mags = []
        mean_magerrs = []
        
        for nite in nites:
            
            nite_df = flt_df[flt_df['NITE'].values == nite]
            
            days_after_trigger = np.mean(np.array(nite_df['MJD'].values, dtype=float)) - mjd_explode
            days_after_trigger_err.append(np.std(np.array(nite_df['MJD'].values, dtype=float)))

            # Do a weighted average, weight by errors and brightness to account for brighter objects having larger errors
            mean_mags.append(np.sum(nite_df['MAG'].values / (nite_df['MAGERR'].values ** 2 * (27.5 - nite_df['MAG'].values))) / 
                             np.sum(1.0 / (nite_df['MAGERR'].values ** 2 * (27.5 - nite_df['MAG'].values))))

            mean_magerrs.append(np.std(mean_mags))


            
            
            


