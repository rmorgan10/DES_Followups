# A module to write a report of the cutflow

# later implementations should automatically do error checking in all logs and print a summary here
import math
import numpy as np
import pandas as pd
import sys

event_name = sys.argv[1]

sim_include = sys.argv[2]

try:
    mode = sys.argv[3]
except:
    mode = 'normal'




df = pd.read_csv('../events/%s/cut_results/MERGED_CUT_RESULTS.csv' %event_name)


def format_uncertainty(value, plus, minus):
    #update this function to handle rounding of values
    error = np.max([plus, minus])
    if error == 0.0:
        return "%s +/- 0.0" %value

    try:
        assert error > 0.0
    except:
        #print("WARNING: Uncertainty less than zero. %s +/- %s" %(value, error))
        return "%s +/- %s" %(value, error)

    num_digits = int(-1 * math.floor(math.log10(error)) + 1)
        
    res = round(value, num_digits)
    err = round(error, num_digits)
        
    return "%s +/- %s" %(res, err)

if mode == 'terse':
    def format_uncertainty(value, plus=None, minus=None):
        return "%.2f" %value
    

#Write report
outlines = []

outlines.append("   -----------------------------------------------------   ")
outlines.append("                        Cut Summary                        ")
outlines.append("   -----------------------------------------------------   \n")
outlines.append(" No.\tCut Name                                       ")
outlines.append(" ---\t---------------------------------------------")

for index, row in df[['CUT', 'NAME']].iterrows():
    outlines.append(" %s\t%s" %(row['CUT'], row['NAME']))

outlines.append("\n")
outlines.append("   -----------------------------------------------------   ")
outlines.append("                      Cut Efficiency                       ")
outlines.append("   -----------------------------------------------------   \n")
outlines.append(" No.\tData\t\t" + '\t\t'.join(sim_include.split(',')))
outlines.append(" ---\t----\t\t" + '\t\t'.join(['-' * len(x) for x in sim_include.split(',')]))
for index, row in df.iterrows():
    
    out_line = ' %s\t%s\t\t' %(row['CUT'], row['DATA'])
    for obj in sim_include.split(','):
        out_line += '%s\t' %format_uncertainty(row[obj])
            
    outlines.append(out_line)

#Print report to screen
for line in outlines:
    print(line)

#Save report
outlines = [x + '\n' for x in outlines]
outfile = open('../events/%s/report.txt' %event_name, 'w+')
outfile.writelines(outlines)
outfile.close()
