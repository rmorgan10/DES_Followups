#A module to overwrite simlib file with desired observing conditions

import numpy as np
import os
import pandas as pd
import sys

# Deal with input data
event_name = sys.argv[1]
event_metadata = pd.read_csv('../events/%s/event_metadata.csv' %event_name)
mjd_explode = event_metadata['MJD_EXPLODE'].values[0]
seeing = float(sys.argv[2])
seeing_width = 0.05
sky_brightness = float(sys.argv[3])
sky_brightness_width = 0.4
delta_t = float(sys.argv[4])
delta_t_width = 0.25 

#force this script to always edit the true simlib
simlib_dir = '../events/%s/sim_gen/' %event_name
if os.path.exists(simlib_dir + 'SIMLIB_TRUE.txt'):
    simlib = simlib_dir + 'SIMLIB_TRUE.txt'
else:
    simlib = '../events/%s/sim_gen/SIMLIB.txt' %event_name
    os.system('cp %s %s' %(simlib, simlib_dir + 'SIMLIB_TRUE.txt'))

stream = open(simlib, 'r')
lines = stream.readlines()
stream.close()

# count lines with observations
nobs = len([x for x in lines if x[0:2] == 'S:'])
nlibids = len([x for x in lines if x[0:6] == 'LIBID:'])

# randomly choose arrays for each observation
seeing_array = np.random.uniform(low=seeing - seeing_width, high=seeing + seeing_width, size=nobs)
sky_brightness_array = np.random.uniform(low=sky_brightness - sky_brightness_width, high=sky_brightness + sky_brightness_width, size=nobs)
delta_t_array = np.random.uniform(low=delta_t - delta_t_width, high=delta_t + delta_t_width, size=nlibids)

#account for units
delta_t_array = delta_t_array / 24.0 #convert to days
delta_t = delta_t / 24.0 #convert to days


#iterate through lines in simlib and make changes as necessary
outlines = []
start_index = 0
end_index = 1
delta_t_index = 0
seeing_index = 0
sky_brightness_index = 0
inside_libid = False
for index, line in enumerate(lines):
    if line[0:6] == 'LIBID:':
        start_index = index
    if line[0:10] == 'END_LIBID:':
        end_index = index

        inside_libid = True

        #once end oof libid is found, start editing
        first_obs = True
        for libid_line_index, libid_line in enumerate(lines[start_index : end_index]):
            
            if libid_line[0:2] != 'S:':
                #not an observation
                outlines.append(libid_line)
            else:
                #an observation
                #S: 58711.286     887171 z  1.03  0.00  414.86  1.27 0.00 0.000  32.89  0.008  99.000
                info = [x for x in libid_line.strip().split(' ') if x != '']
                if first_obs:
                    base_mjd = float(info[1])
                    old_delta_t = base_mjd - mjd_explode
                    first_obs = False

                mjd = float(info[1])
                new_mjd = mjd - old_delta_t + delta_t + delta_t_array[delta_t_index]

                #psf = float(info[7]) #-don't need
                new_psf = seeing_array[seeing_index]
                seeing_index += 1
                
                #sky = float(info[6]) #-don't need
                zpt = float(info[10])
                #sky_mag = zpt - 2.5 * np.log10(sky_sig)
                # --> sky_sig = 10 ** ((zpt - skymag) / 2.5)
                new_sky = 10 ** ((zpt - sky_brightness) / 2.5)
                new_sky += 10 ** ((zpt - sky_brightness_array[sky_brightness_index]) / 2.5)
                sky_brightness_index += 1

                #write new line
                new_line = '  '.join(['S:', '%.3f' %new_mjd] + info[2:6] + ['%.3f' %new_sky, '%.3f' %new_psf] + info[8:]) + '\n'
                outlines.append(new_line)

        inside_libid = False
        #take a step in the delta_t_array
        delta_t_index += 1

    #don't forget lines in between libids
    if start_index < end_index and not inside_libid:
        outlines.append(line)
        
# remove final new line character so that effective area is the last entry
outlines[-1] = outlines[-1][0:-1]


# write to output file
out_stream = open('../events/%s/sim_gen/SIMLIB.txt' %event_name, 'w+')
out_stream.writelines(outlines)
out_stream.close()

