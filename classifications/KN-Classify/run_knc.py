# Outer shell for KN-Classify

#import numpy as np
#from optparse import OptionParser
import os
import sys

event_name = sys.argv[1]
sim_include = sys.argv[2]

# build training sets
os.system('python make_all_datasets.py %s %s' %(event_name, sim_include))




# featurize real data if desired
if data != 'None':
    os.system('python process_data.py %s' %event_name)









default_training = '../../events/%s/KNC/training_data.npy' %event_name
parser = OptionParser(__doc__)
parser.add_option('--train', default=default_training, help="Path to training data")
parser.add_option('--data', default='None', help="Path to real data")
parser.add_option('--test_size', default=0.2, help="Fractional size of test set")
options, args = parser.parse_args(sys.argv[2:])
train = options.train
data = options.data
test_size = options.test_size

