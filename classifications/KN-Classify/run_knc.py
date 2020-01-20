# Outer shell for KN-Classify

import os
import sys

event_name = sys.argv[1]
sim_include = sys.argv[2]

# build training sets
os.system('python make_all_datasets.py %s %s' %(event_name, sim_include))

# Process data
os.system('python process_data.py %s' %event_name)

# Perform classifications
os.system('python classify_data.py %s' %event_name)

# Collect results
os.system('python collect_results.py %s' %event_name)



