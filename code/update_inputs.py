# update snana templates to fit event of interest

import getpass
import os
import pandas as pd
import sys
import utils

#read input data
event_name = sys.argv[1]
df = pd.read_csv('../events/%s/event_metadata.csv' %event_name)
username = getpass.getuser()

#get effective area from simlib
simlib_filename = '../events/%s/sim_gen/SIMLIB.txt' %event_name
simlib_file = open(simlib_filename, 'r')
simlib_info = simlib_file.readlines()
simlib_file.close()
eff_area = float([x for x in simlib_info[-5:] if x[0:15] == 'EFFECTIVE_AREA:'][0].split(' ')[1][0:-1])

#files needing to be updated:
# - AGN_SIMGEN.INPUT
# - SIMGEN_DES_KN.input
# - SIMGEN_DES_NONIA.input
# - SIMGEN_DES_SALT2.input

file_prefix = '../events/%s/sim_gen/' %event_name
file_list = ['AGN_SIMGEN.INPUT', 'SIMGEN_DES_KN.input', 'SIMGEN_DES_NONIA.input', 'SIMGEN_DES_SALT2.input',
             'CART_SIMGEN.INPUT', 'ILOT_SIMGEN.INPUT', 'Mdwarf_SIMGEN.INPUT', 'SN_Ia91bgSIMGEN.INPUT',
             'SN_IaxSIMGEN.INPUT', 'SN_PIaSIMGEN.INPUT', 'SN_SLSNSIMGEN.INPUT', 'TDE_SIMGEN.INPUT']
objs = ['AGN', 'KN', 'CC', 'Ia', 'CaRT', 'ILOT', 'Mdwarf', 'SN91bg', 'Iax', 'PIa', 'SLSN', 'TDE']

#iterate through files and update:
# - genversion (update during loop)
# - exposure time
# - gnerange_peakmjd
# - genrange_mjd
# - solid_angle (conversion: .00082 sterradians = 3 sqdeg )
# - mjd explode (kn only)

exp_time = '1' #str(round(df['EXPTIME_(sec)'].values[0] / 60.0, 3))
mjd_min = str(int(float(df['MJD_EXPLODE'].values[0])) - 60)
mjd_max = str(int(float(df['MJD_EXPLODE'].values[0])) + 30)
mjd_exp = str(df['MJD_EXPLODE'].values[0])
solid_angle = str(round(eff_area / 3.0 * .00082, 6))
min_z, max_z = utils.get_ligo_z_range(df['LIGO_distance_(Mpc)'].values[0], df['LIGO_sigma_(Mpc)'].values[0]) 




for filename, obj in zip(file_list, objs):
    
    #construct new input information
    header = ['#',
              '# SIMGEN file for ' + obj,
              '#',
              ' ',
              '#--------------------------------------------------------------------',
              '# Event-specific info to be overwritten',
              '#--------------------------------------------------------------------',
              ' ',
              'GENRANGE_PEAKMJD: ' + mjd_min + ' ' + mjd_max,
              'GENRANGE_MJD: ' + mjd_min + ' ' + mjd_max,
              'GENVERSION: %s_DESGW_' %username  + event_name + '_' + obj,
              'EXPOSURE_TIME: ' + exp_time,
              'SOLID_ANGLE: ' + solid_angle]

    if obj == 'KN':
        header.append('MJD_EXPLODE: ' + mjd_exp)
        header.append('GENRANGE_REDSHIFT: ' + str(min_z) + ' ' + str(max_z))
        header.append('NGEN_LC: ' + str(df['NUM_KN'].values[0]))
    elif obj == 'AGN':
        header.append('NGEN_LC: ' + str(df['NUM_AGN'].values[0]))
    elif obj == 'CC' or obj == 'Ia':
        header.append('NGEN_SEASON: ' + str(df['BOOST'].values[0]))
    elif obj == 'Mdwarf':
        header.append('NGEN_LC: ' + str(df['NUM_Mdwarf'].values[0]))
    elif obj in ['PIa', 'Iax', 'SN91bg']:
        header.append('NGEN_LC: ' + str(df['BOOST'].values[0] * 1000))
    elif obj in ['TDE', 'SLSN', 'ILOT', 'CaRT']:
        header.append('NGEN_LC: ' + str(df['BOOST'].values[0] * 1000))

    buffer_lines = ['#--------------------------------------------------------------------',
                    "# Don't need to change anything after this point  (I sure hope)",
                    '#--------------------------------------------------------------------']

    input_lines = [x + '\n' for x in header + buffer_lines]

    #open template file
    template_file = open(file_prefix + filename, 'r')
    template_lines = template_file.readlines()
    template_file.close()
    
    #construct output file
    output_lines = input_lines + template_lines[len(input_lines) + 1:]

    #write to output file
    outfile = open(file_prefix + filename, 'w+')
    outfile.writelines(output_lines)
    outfile.close()



#File header looks like this:
"""
# 
# SIMGEN file for KN
#

#--------------------------------------------------------------------
# Event-specific info to be overwritten
#--------------------------------------------------------------------

GENRANGE_PEAKMJD: 58598 58628
GENRANGE_MJD: 58598 58628
GENVERSION:  RM_Net_AGN
EXPOSURE_TIME: 1.5
SOLID_ANGLE:  0.0082
MJD_EXPLODE: 55555

#--------------------------------------------------------------------
# Don't need to change anything after this point  (I sure hope)
#--------------------------------------------------------------------
"""
