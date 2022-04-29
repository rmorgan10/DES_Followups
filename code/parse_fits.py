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
if len(sys.argv) > 3:
    stop_point = int(float(sys.argv[3]))
else:
    stop_point = -1

phot_file = '../events/%s/sims_and_data/%s_FITS/%s_PHOT.FITS' %(event_name, fits_dir_prefix, fits_dir_prefix)
head_file = '../events/%s/sims_and_data/%s_FITS/%s_HEAD.FITS' %(event_name, fits_dir_prefix, fits_dir_prefix)

#deal with output data
transient_class = fits_dir_prefix.split('_')[-1]
process_log_file = '../events/%s/logs/parse_%s.log' %(event_name, transient_class)



if not os.path.exists('../events/%s/sims_and_data/%s_PYTHON' %(event_name, fits_dir_prefix)):
    os.system('mkdir ../events/%s/sims_and_data/%s_PYTHON' %(event_name, fits_dir_prefix))

    # NS 14.01.22
    if os.path.exists(head_file + '.gz'):
        os.system('gunzip ' + head_file + '.gz')
        os.system('gunzip ' + phot_file + '.gz')
    
    #check if sim tar files need to be unpacked
    if not os.path.exists(head_file):
        os.system('pwd')
        os.chdir('../events/%s/sims_and_data' %event_name)
        os.system('pwd')
        os.system('ls')
        #sys.exit()
        os.system('rm -rf %s_FITS' %fits_dir_prefix)
        os.system('tar -xzf %s.tar.gz' %fits_dir_prefix)
        os.chdir('../../../code')

    #read head file
    hdu = fits.open(head_file)
    head_columns = hdu[1].columns.names
    head_data = hdu[1].data
    hdu.close()
    head_df = pd.DataFrame(data=head_data, columns=head_columns)
    # hack to fix issue of spectroscopic redshifts in real data have z_err = 99
    if 'REDSHIFT_FINAL_ERR' in head_columns:
        head_df['REDSHIFT_FINAL_ERR'].replace(to_replace=99.0, value=1.e-4, inplace=True)

    #read phot file
    lcs = []
    hdu = fits.open(phot_file)
    phot_columns = hdu[1].columns.names
    phot_data = hdu[1].data
    hdu.close()

    #split phot data into individual light curve dataframes
    lc_data = []
    total = len(phot_data)
    counter = 0
    for data_line in phot_data:

        #track progress
        counter += 1
        progress = float(counter) / total * 100
        #sys.stdout.write('\rProgress:  %.2f %%' %progress)
        #sys.stdout.flush()
        if (total - counter) % 100 == 0:
            log = open(process_log_file, 'w+') 
            log.write('%.2f' % progress)
            log.close()

        #organize light curves
        if data_line[1] == '-':
            try:
                df = pd.DataFrame(data=np.array(lc_data), columns=phot_columns)
                #force photflag definition to include the 8192 bit for ml socre > 0.7
                df['PHOTFLAG'] = [12288 if int(x) == 4096 and float(y) > 0.7 else x for x, y in zip(df['PHOTFLAG'].values, df['PHOTPROB'].values)]
                #add mag and mag_err
                df['MAG'] = [27.5 - 2.5 * np.log10(float(x)) if float(x) > 0.0 else 99.0 for x in df['FLUXCAL'].values]
                df['MAGERR'] = [np.abs(2.5 * np.log10(float(x) / (float(x) + float(y)))) if float(x) > 0.0 else 99.0 for x, y in zip(df['FLUXCAL'].values, df['FLUXCALERR'].values)] 
                lcs.append(df)
                lc_data = []
            except:
                lcs.append('SKIP')
                lc_data = []
        else:
            lc_data.append(data_line)

        if len(lcs) == stop_point: break

    #construct out dictionary
    out_dict = {}
    for index, row in head_df.iterrows():

        if index == stop_point: break

        if type(lcs[index]) != type('SKIP'):
            out_dict[row['SNID'].strip()] = {'metadata': row, 'lightcurve': lcs[index]}


    #save out dict
    np.save('../events/%s/sims_and_data/%s_PYTHON/%s.npy' %(event_name, fits_dir_prefix, fits_dir_prefix), out_dict)

    #tar and delete snana fits files
    os.chdir('../events/%s/sims_and_data' %event_name)
    os.system('tar -czf %s_FITS.tar.gz %s_FITS' %(fits_dir_prefix, fits_dir_prefix))
    os.system('rm -rf %s_FITS/*' %fits_dir_prefix)
    #os.rmdir('%s_FITS' %fits_dir_prefix)
    os.chdir('../../../code')

    #close log file
    #log.close() --closed earlier

else:
    print("Python-ized light curves already exists, skipping light curve processing")
