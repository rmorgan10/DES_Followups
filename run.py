## Outer Shell for Follow-up Pipeline

### This shell will both generate sims and place cuts on observations


import os
import pandas as pd
import sys

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
    

if mode == 'interactive':
    print("Running in interactive mode.\n")
    #prompt the user for all needed values and create necessary files




    #set mode to normal so that the main codes will execute
    print("Interactive mode completed. Switching to normal mode.\n")
    mode = 'normal'

if mode == 'normal':
    print("Running in normal mode.\n")

    #interpret metadata
    os.system('python interpret_metadata.py %s' %event_name)

    #generate sims
    os.system('python generate_sims.py %s' %event_name)

    #apply cuts to sims and data
    os.system('python run_cuts.py %s both' %event_name)

    #analyze results
    os.system('python analyze_results.py %s' %event_name)
