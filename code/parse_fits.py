# functions for parsing SNANA fits files 

##### Need to edit to work on an arbitrary fits directory


from astropy.io import fits
import numpy as np
import os
import pandas as pd
import sys


#deal with input data
event_name = sys.argv[1]
fits_dir_prefix = sys.argv[2]
phot_file = '../events/%s/sims_and_data/%s_FITS/%s_PHOT.FITS' %(event_name, fits_dir_prefix, fits_dir_prefix)
head_file = '../events/%s/sims_and_data/%s_FITS/%s_HEAD.FITS' %(event_name, fits_dir_prefix, fits_dir_prefix)

if not os.path.exists('../events/%s/sims_and_data/%s_PYTHON' %(event_name, fits_dir_prefix)):
    os.system('mkdir ../events/%s/sims_and_data/%s_PYTHON' %(event_name, fits_dir_prefix))
    
    #read head file
    hdu = fits.open(head_file)
    head_columns = hdu[1].columns.names
    head_data = hdu[1].data
    hdu.close()
    head_df = pd.DataFrame(data=head_data, columns=head_columns)

    #read phot file
    lcs = []
    hdu = fits.open(phot_file)
    phot_columns = hdu[1].columns.names
    phot_data = hdu[1].data
    hdu.close()

    #split phot data into individual light curve dataframes
    lc_data = []
    total = float(len(phot_data))
    counter = 0.0
    for data_line in phot_data:
        #track progress
        counter += 1.0
        progress = counter / total * 100
        sys.stdout.write('\rProgress:  %.2f %%' %progress)
        sys.stdout.flush()

        #organize light curves
        if data_line[1] == '-':
            try:
                df = pd.DataFrame(data=np.array(lc_data), columns=phot_columns)
                #force photflag definition to include the 8192 bit for ml socre > 0.7
                df['PHOTFLAG'] = [12288 if int(x) == 4096 and float(y) > 0.7 else x for x, y in zip(df['PHOTFLAG'].values, df['PHOTPROB'].values)]
                lcs.append(df)
                lc_data = []
            except:
                lcs.append('SKIP')
                lc_data = []
        else:
            lc_data.append(data_line)

    #construct out dictionary
    out_dict = {}
    for index, row in head_df.iterrows():
        if type(lcs[index]) != type('SKIP'):
            out_dict[row['SNID'].strip()] = {'metadata': row, 'lightcurve': lcs[index]}

    #save out dict
    np.save('../events/%s/sims_and_data/%s_PYTHON/%s.npy' %(event_name, fits_dir_prefix, fits_dir_prefix), out_dict)

    #tar and delete snana fits files
    os.chdir('../events/%s/sims_and_data' %event_name)
    os.system('tar -czf %s_FITS.tar.gz %s_FITS' %(fits_dir_prefix, fits_dir_prefix))
    os.system('rm -r %s_FITS' %fits_dir_prefix)
    os.chdir('../../../code')

else:
    print("Python-ized light curves already exists, skipping light curve processing")
