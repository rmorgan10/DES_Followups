## Outer Shell for Follow-up Pipeline

### This shell will both generate sims and place cuts on observations


import os
import pandas as pd
import sys

from optparse import OptionParser

# move to code directory
os.chdir('code')

header =  """
_________________________________________________________________________________
    ____  _____ ____    _____     _ _                                            
   |  _ \| ____/ ___|  |  ___|__ | | | _____      __          _   _ _ __         
   | | | |  _| \___ \  | |_ / _ \| | |/ _ \ \ /\ / /  _____  | | | | '_ \        
   | |_| | |___ ___) | |  _| (_) | | | (_) \ V  V /  |_____| | |_| | |_) |       
   |____/|_____|____/  |_|  \___/|_|_|\___/ \_/\_/            \__,_| .__/        
                                                                   |_|           
       _                _           _       ____  _            _ _                 
      / \   _ __   __ _| |_   _ ___(_)___  |  _ \(_)_ __   ___| (_)_ __   ___    
     / _ \ | '_ \ / _` | | | | / __| / __| | |_) | | '_ \ / _ \ | | '_ \ / _ \   
    / ___ \| | | | (_| | | |_| \__ \ \__ \ |  __/| | |_) |  __/ | | | | |  __/   
   /_/   \_\_| |_|\__,_|_|\__, |___/_|___/ |_|   |_| .__/ \___|_|_|_| |_|\___|   
                          |___/                    |_|                           
---------------------------------------------------------------------------------
"""

print('\n\n\n')
print(header)
print('\n')

#Determine mode of operation based on presence of event_name
if len(sys.argv) == 1:
    mode = 'interactive'
else:
    event_name = sys.argv[1]
    mode = 'normal'

    #parse for bosst, num_kn, and num_agn
    parser = OptionParser(__doc__)
    parser.add_option('--boost', default=10, help="Number of seasons to simulate for SNe")
    parser.add_option('--num_kn', default=10000, help="Number of KNe to simulate")
    parser.add_option('--num_agn', default=10000, help="Number of AGN to simulate")
    parser.add_option('--clean_up', default="None", help="Things to be cleaned up")
    options, args = parser.parse_args(sys.argv[2:])
    boost = float(options.boost)
    num_kn = int(float(options.num_kn))
    num_agn = int(float(options.num_agn))
    clean_up = str(options.clean_up)
    

    

if mode == 'interactive':
    print("Running in interactive mode.\n")
    #prompt the user for all needed values and create necessary files
    



    #set mode to normal so that the main codes will execute
    print("Interactive mode completed. Switching to normal mode.\n")
    mode = 'normal'

if mode == 'normal':
    print("Running in normal mode.\n")

    #clean up if desired
    if clean_up != "None":
        os.system("python clean_up.py %s %s" %(event_name, clean_up))

    #interpret metadata
    os.system('python interpret_metadata.py %s --boost %.3f --num_kn %i --num_agn %i' %(event_name, boost, num_kn, num_agn))

    #generate sims
    os.system('python generate_sims.py %s' %event_name)

    #apply cuts to sims and data
    os.system('python run_cuts.py %s both' %event_name)

    #analyze results
    os.system('python analyze_results.py %s' %event_name)

    #write out a report with uncertainties
    os.system('python write_report.py %s' %event_name)
