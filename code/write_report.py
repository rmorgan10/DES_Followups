# A module to write a report of the cutflow

# later implementations should automatically do error checking in all logs and print a summary here

import pandas as pd
import sys

event_name = sys.argv[1]

df = pd.read_csv('../events/%s/cut_results/MERGED_CUT_RESULTS.csv' %event_name)


def format_uncertainty(center, plus, minus):
    #update this function to handle rounding of values
    return center, plus, minus


# iterate through df and print out necessary rows
classes = []



print(df[['CUT', 'AGN_scaled', 'Ia_scaled', 'CC_scaled', 'DATA', 'KN_scaled']])

print(df['NAME'])
