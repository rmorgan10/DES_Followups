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
    parser.add_option('--num_agn', default=0, help="Number of AGN to simulate")
    parser.add_option('--clean_up', default="None", help="Things to be cleaned up")
    parser.add_option('--propid', default="", help="PropID for observations")
    parser.add_option('--first_exposure', default=0, help="First expnum of observations")
    parser.add_option('--last_exposure', default=0, help="Last expnum of observations")
    parser.add_option('--num_mdwarf', default=0, help="Number of Mdwarfs to simulate")
    parser.add_option('--sim_include', default="KN,Ia,CC,AGN", help="Transient classes to simulate")
    parser.add_option('--force_conditions', default='real', help="PSF,SKYMAG,DELTAT")
    options, args = parser.parse_args(sys.argv[2:])
    boost = float(options.boost)
    num_kn = int(float(options.num_kn))
    num_agn = int(float(options.num_agn))
    clean_up = str(options.clean_up)
    propid = str(options.propid)
    first_exposure = int(options.first_exposure)
    last_exposure = int(options.last_exposure)
    num_mdwarf = int(options.num_mdwarf)
    sim_include = str(options.sim_include).strip().split(',')
    forced_conditions = str(options.force_conditions)

# Command-line argument error checking
allowed_sims = ['KN', 'Ia', 'CC', 'AGN', 'CaRT', 'ILOT', 'Mdwarf', 'SN91bg', 'Iax', 'PIa', 'SLSN', 'TDE']
if len(sim_include) == 1:
    if sim_include[0] == 'all':
        sim_include = allowed_sims[:]
else:
    for obj in sim_include:
        if obj not in allowed_sims:
            print("%s is not one of the available models. Choose from the following list:" %obj)
            print(allowed_sims)
            sys.exit()

    


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
    
    #get full exptable if desired
    if first_exposure != 0 and last_exposure != 0 and propid != "":
        os.system('python get_exposures.py %s %s %i %i' %(event_name, propid, first_exposure, last_exposure))

    #interpret metadata
    os.system('python interpret_metadata.py %s --boost %.3f --num_kn %i --num_agn %i --num_mdwarf %i' %(event_name, boost, num_kn, num_agn, num_mdwarf))

    #generate sims
    os.system('python generate_all_sims.py %s %s %s' %(event_name, forced_conditions, ' '.join(sim_include)))
    #sys.exit()
    #apply cuts to sims and data
    os.system('python run_all_cuts.py %s both %s' %(event_name, ' '.join(sim_include)))

    #analyze results
    os.system('python analyze_results.py %s' %event_name)

    #write out a report with uncertainties
    os.system('python write_report.py %s' %event_name)
