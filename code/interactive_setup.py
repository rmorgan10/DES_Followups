"""This script automates the creation of an event dir by promting user.

To run the DES_Followups pipeline, you need the MJD of the event and the path to
the dat files. In the case of a GW event, you also need the LIGO mean and std
distance, as well as the KN probability. This script will first promt the user
for all necessary information and then set up the event directory to run the
main pipeline.
"""

import glob
import os
import sys

event_name = sys.argv[1]

os.system('mkdir ../events/%s' %event_name)
os.chdir('../events/%s' %event_name)

# Dat file path
dat_file_path = raw_input("Enter the absolute path to the dat files directory (should end with /LightCurvesReal/, enter 'q' to quit):")
if not dat_file_path[-1] == '/':
    dat_file_path += '/'
dat_files = glob.glob("%s*.dat" %dat_file_path)
while len(dat_files) == 0:
    if dat_file_path.lower() == 'q':
        sys.exit(1)
    print("No dat files found at entered path, try again or enter 'q' to quit.")
    dat_file_path = raw_input("Enter the absolute path to the dat files directory (should end with /LightCurvesReal/, enter 'q' to quit):")
    if not dat_file_path[-1] == '/':
        dat_file_path += '/'
    dat_files = glob.glob("%s*.dat" %dat_file_path)

dat_file_path_file = open('dat_file_path.txt', 'w+')
dat_file_path_file.write(dat_file_path)
dat_file_path_file.close()

def get_float_value(name):
    """Receive a float value from the user.

    Args:
      name (str): Name to give to the user when prompting.
    
    Returns:
      floating-point value entered by the user.
    """
    while True:
        value = raw_input("Enter the %s (enter 'q' to quit): " %name)

        if value.lower() == 'q':
            sys.exit(1)

        try:
            value = float(value)
            return value
        except ValueError:
            print("Unable to convert entered value to a float. Try again.")

# Trigger MJD
print('')
trigger_mjd = str(get_float_value("MJD of the alert"))

# GW properties
print('')
first_time = True
is_gw = 'k'
while is_gw.lower() not in ['y', 'n']:
    if not first_time:
        print("Input not recognized.")
    is_gw = raw_input("Is the event a GW event? (y/n/q to quit)")
    if is_gw.lower() == 'q':
        sys.exit(1)
    first_time = False


if is_gw.lower() == 'y':
    ligo_dist = str(get_float_value("Mean LIGO distance in Mpc"))
    ligo_std = str(get_float_value("LIGO distance std in Mpc"))
    ligo_prob_kn = str(get_float_value("LIGO probabilty of KN"))
    ligo_header = 'NAME,MJD_EXPLODE,LIGO_distance_(Mpc),LIGO_sigma_(Mpc),LIGO_prob_KN\n'
    ligo_data = ','.join([event_name, trigger_mjd, ligo_dist, ligo_std, ligo_prob_kn])
else:
    ligo_header = 'NAME,MJD_EXPLODE\n'
    ligo_data = ','.join([event_name, trigger_mjd])

ligo_metadata_file = open('LIGO_metadata.csv', 'w+')
ligo_metadata_file.write(ligo_header)
ligo_metadata_file.write(ligo_data)
ligo_metadata_file.close()
    
