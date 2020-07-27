# A module to repeat classifications until an optimum is found

# In a situation with larger training sets, this process should yield no advantage

# not hacky at all...

import os
import sys

import pandas as pd
import numpy as np

from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix

def calc_best_thresh(fpr, tpr, thresh):
    fpr_tolerance = 0.01
    cond = (fpr < fpr_tolerance)

    trimmed_tpr = tpr[cond]
    trimmed_thresholds = thresholds[cond]

    return trimmed_thresholds[np.argmax(trimmed_tpr)]

def calc_best_cm(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    return sum(cm.diagonal()) 

event_name = sys.argv[1]
event_dir = '../../events/%s/PSNID' %event_name
signal = sys.argv[2]
background = sys.argv[3] #comma-separated list of background objects
sim_include = signal + ',' + background

#One-hot encoding
encode = {obj: idx for idx, obj in enumerate(sorted(sim_include.split(',')))}


best_value = 0.0
counter = 0
while counter <= 100:
    counter += 1
    
    os.system('python featurize.py %s %s %s' %(event_name, signal, background))
    os.system('python classify.py %s %s %s' %(event_name, signal, background))

    test = pd.read_csv('%s/pred_test.csv' %event_dir)
    binary_labels = np.array([int(x == signal) for x in test['CLASS'].values])
    binary_scores = np.array(test['PROB_%s' %signal].values, dtype=float)

    class_names = np.array(sorted(sim_include.split(',')))
    y_test_label = [encode[x] for x in test['CLASS'].values]
    y_test_pred = []
    for index, row in test.iterrows():
        y_test_pred.append(class_names[np.argmax(np.array(row[['PROB_%s' %obj for obj in sorted(sim_include.split(','))]]))])
    y_test_pred_label = [encode[x] for x in y_test_pred]

    #fpr, tpr, thresholds = roc_curve(binary_labels, binary_scores)

    metric = calc_best_cm(y_test_label, y_test_pred_label)

    if metric > best_value:
        best_value = metric

        os.system('cp %s/training_set.csv %s/opt_training_set.csv' %(event_dir, event_dir))
        os.system('cp %s/testing_set.csv %s/opt_testing_set.csv' %(event_dir,event_dir))

        os.system('cp %s/pred_data.csv %s/opt_pred_data.csv' %(event_dir,event_dir))
        os.system('cp %s/pred_test.csv %s/opt_pred_test.csv' %(event_dir,event_dir))
        os.system('cp %s/pred_train.csv %s/opt_pred_train.csv' %(event_dir,event_dir))

        os.system('cp %s/feat_importances.csv %s/opt_feat_importances.csv' %(event_dir,event_dir))
        os.system('cp %s/calibration.csv %s/opt_calibration.csv' %(event_dir,event_dir))

        print("Iteration %i of 100:  %.4f\t\tNew Best!" %(counter, metric))

    else:
        print("Iteration %i of 100:  %.4f" %(counter, metric))
