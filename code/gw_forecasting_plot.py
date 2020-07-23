# Make Forecasting Plot

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.stats import poisson
import sys

from matplotlib import rcParams
rcParams['font.family'] = 'serif'

event_name = sys.argv[1]

try:
    kn_template = int(sys.argv[2])
    kn_label = sys.argv[3]
except:
    #default to GW170817-blue
    kn_template = 178
    kn_label = 'GW170817-like (blue)'



def fraction_n_sigma(eff, bkg, size=100000):
    
    if bkg > 1:
        n_array = np.arange(int(10*bkg))
    else:
        n_array = np.arange(10)
    
    prob_observe_n_with_sig = (1.0 - eff) * poisson.pmf(mu=bkg, k=n_array) + eff * poisson.pmf(mu=bkg, k=(n_array-1))
    prob_observe_n_with_sig /= np.sum(prob_observe_n_with_sig)
    prob_observe_n_with_bkg = poisson.pmf(mu=bkg, k=n_array)
    prob_observe_n_with_bkg /= np.sum(prob_observe_n_with_bkg)
    
    sig_choices = np.random.choice(n_array, size=size, p=prob_observe_n_with_sig)
    bkg_choices = np.random.choice(n_array, size=size, p=prob_observe_n_with_bkg)
    
    output_array = poisson.sf(mu=bkg_choices, k=sig_choices)
    
    one_sigma_cond = (output_array < 0.317310507863)
    two_sigma_cond = (output_array < 0.045500263896)
    three_sigma_cond = (output_array < 0.002699796063)
    four_sigma_cond = (output_array < 0.000063342484)
    five_sigma_cond = (output_array < 0.000000573303)
    
    return (float(len(output_array[one_sigma_cond])) / len(output_array),
            float(len(output_array[two_sigma_cond])) / len(output_array),
            float(len(output_array[three_sigma_cond])) / len(output_array),
            float(len(output_array[four_sigma_cond])) / len(output_array),
            float(len(output_array[five_sigma_cond])) / len(output_array))
    

def append_and_clean_lists(new_effs, new_bkgs, old_effs, old_bkgs, 
                           one_sig, two_sig, three_sig, four_sig, five_sig):
    #backgrounds must be increasing
    effs = list(old_effs)
    bkgs = list(old_bkgs)

    #calc significances
    for eff, bkg in zip(new_effs, new_bkgs):
        a, b, c, d, e = fraction_n_sigma(eff, bkg)
        one_sig.append(a)
        two_sig.append(b)
        three_sig.append(c)
        four_sig.append(d)
        five_sig.append(e)
        effs.append(eff)
        bkgs.append(bkg)
        
        
    #drop list elements with background == 0.0
    indices_to_keep = (np.array(bkgs) != 0.0)
    
    return (np.array(one_sig)[indices_to_keep],
            np.array(two_sig)[indices_to_keep],
            np.array(three_sig)[indices_to_keep],
            np.array(four_sig)[indices_to_keep],
            np.array(five_sig)[indices_to_keep],
            np.array(bkgs)[indices_to_keep],
            np.array(effs)[indices_to_keep])


## INFO NEEDED
# - tpr curve
# - fpr curve
ml_info = np.load('../events/%s/PSNID/ml_curves.npy' %event_name).item()


# - initial sn_background after all non-ml cuts
# - expected background at each cut
background_df = pd.read_csv('../events/%s/cut_results/MERGED_CUT_RESULTS.csv' %event_name)
sn_background = list(background_df['Ia_scaled'].values + background_df['CC_scaled'].values)[1:]
initial_bkg = sn_background[-1] + 0.0
sn_background.reverse()

bkgs = initial_bkg * ml_info['fpr']


# - KN template choice, default to GW170817-blue 
# - initial efficiency after all non ml cuts
# - template efficiency at each cut
kn_df = pd.read_csv('../events/%s/analysis/%s_kn_terse_cut_results_ml.csv' %(event_name, event_name))

template_cut_arr = kn_df['CUT'].values[kn_df['SIM_TEMPLATE_INDEX'].values == kn_template]
cuts, counts = np.unique(template_cut_arr, return_counts=True)

shifted_cuts = list(cuts)[1:] + list(cuts)[0:1]
shifted_counts = list(counts)[1:] + list(counts)[0:1]

effs = []
total = float(np.sum(shifted_counts))
gone = 0.0
for num_cut in shifted_counts[0:-1]:
    gone += num_cut
    effs.append((total - gone) / total)


initial_eff = effs[-1] + 0.0
sigs = initial_eff * ml_info['tpr']
#sigs /= np.max(sigs)

effs.reverse()


### Begin main calculation

one_sig, two_sig, three_sig, four_sig, five_sig = [], [], [], [], []
for eff, bkg in zip(sigs, bkgs):
    a, b, c, d, e = fraction_n_sigma(eff, bkg)
    one_sig.append(a)
    two_sig.append(b)
    three_sig.append(c)
    four_sig.append(d)
    five_sig.append(e)

one_sig, two_sig, three_sig, four_sig, five_sig, bkgs, sigs = append_and_clean_lists(effs, 
                                                                                     sn_background, 
                                                                                     sigs, 
                                                                                     bkgs, 
                                                                                     one_sig, 
                                                                                     two_sig, 
                                                                                     three_sig, 
                                                                                     four_sig, 
                                                                                     five_sig)



### Make plot

fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 0.4]}, figsize=(5, 5), dpi=120)

ax1.plot(bkgs, one_sig, label=r'$1 \sigma$', color='#bae4bc', lw=2)
ax1.plot(bkgs, two_sig, label=r'$2 \sigma$', color='#7bccc4', lw=2)
ax1.plot(bkgs, three_sig, label=r'$3 \sigma$', color='#43a2ca', lw=2)
ax1.plot(bkgs, four_sig, label=r'$4 \sigma$', color='#0868ac', lw=2)

ax1.axvline(x=initial_bkg, lw=0.5, color='black', ls='--')
#ax1.text(initial_bkg * 2, 0.95, 'Before ML', horizontalalignment='right')
#ax1.text(initial_bkg / 2, 0.95, 'With ML', horizontalalignment='left')
ax1.text(initial_bkg * 2, 0.95, 'Before ML', horizontalalignment='left')
ax1.text(initial_bkg / 2, 0.95, 'With ML', horizontalalignment='right')

ax1.set_xscale('log')
#ax1.set_xlim(np.max(bkgs), 1.e-2)
ax1.set_xlim(2.e-2, np.max(bkgs))
ax1.set_ylim(-0.02, 1.02)
ax1.set_ylabel("Fraction of Follow-ups", fontsize=12)
#ax1.legend(loc='lower right', fontsize=12)
ax1.legend(loc='lower left', fontsize=12) 

ax2.plot(bkgs, sigs / sigs.max(), color='black', lw=2)
ax2.set_xscale('log')
#ax2.set_xlim(np.max(bkgs), 1.e-2)
ax2.set_xlim(2.e-2, np.max(bkgs))
ax2.set_ylim(0.0, 1.0)
ax2.set_ylabel("Relative\nKN Efficiency", fontsize=12)
ax2.set_xlabel("Remaining Background", fontsize=12)

ax2.axvline(x=initial_bkg, lw=0.5, color='black', ls='--')

#ax2.text(2.e-2, 0.85, kn_label, horizontalalignment='right')
ax2.text(2.e-2, 0.85, kn_label, horizontalalignment='left') 

fig.tight_layout()

fig.savefig('../events/%s/analysis/gw_forecasting.pdf' %event_name)

#plt.show()
