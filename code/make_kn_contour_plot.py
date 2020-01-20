# Inputs for kn contour plotting functions

import sys

import kn_contour_plot_functions as funcs

event_name = sys.argv[1]
outfile = '../events/%s/analysis/kn_contour.pdf' %event_name

# Event specific info

if event_name == 'GW190814_1001':
    cuts = [1, 18]
    filenames = ['../events/%s/analysis/%s_cut_%i_kn_efficiencies_table.csv' %(event_name, event_name, cut) for cut in cuts] 

    backgrounds = [396.5 + 174.0, 0.001]
    lam = 1.0
    f = 0.99

    sigma_list = [{'20': 6, '21': 6, '12': 6}, {'20': 8, '21': 8, '12': 12}]
    plot_contour_list = [False, True]
    hist_param_list = [{'color': 'black',
                        'lw': 2,
                        'linestyle': 'dotted'},
                       {'color': 'black',
                        'lw': 2,
                        'linestyle': 'solid'}]



# Make plots
full_plot_data = funcs.make_full_plot_data(filenames, backgrounds, lam=lam, f=f, sigma_list=sigma_list)
funcs.make_plot_full(full_plot_data, plot_contour_list=plot_contour_list, hist_param_list=hist_param_list, outfile=outfile)
