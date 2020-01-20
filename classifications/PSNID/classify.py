# Classifier for PSNID + RFC method

import numpy as np
import pandas as pd
import sys
from scipy.interpolate import interp1d

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve

event_name = sys.argv[1]
event_dir = '../../events/%s/PSNID' %event_name

#load training and testing sets
train_df = pd.read_csv('%s/training_set.csv' %event_dir)
test_df = pd.read_csv('%s/testing_set.csv' %event_dir)

#load data
data_df = pd.read_csv('%s/data.csv' %event_dir)

#get training features
feats = [x for x in train_df.columns if x != 'CLASS']

#train a random forest classifeir
rfc = RandomForestClassifier(n_estimators=100, criterion='entropy', max_depth=5, n_jobs=-1, random_state=6)
rfc.fit(train_df[feats], train_df['CLASS'])

out_feat_df = pd.DataFrame(data=np.array([feats, rfc.feature_importances_]).T, columns=['FEATURE', 'IMPORTANCE'])
out_feat_df.to_csv('%s/feat_importances.csv' %event_dir, index=False)


#make predictions
## note labels are in alphabetical order: (CC = 0, Ia = 1, KN = 2)
train_pred = rfc.predict_proba(train_df[feats])
test_pred = rfc.predict_proba(test_df[feats])
data_pred = rfc.predict_proba(data_df[feats])

#calibrate KN probabilities to Purity of test set
test_labels_binary = [int(x == 'KN') for x in test_df['CLASS'].values]
test_scores_binary = test_pred[:,2]
precision, recall, thresholds = precision_recall_curve(test_labels_binary, test_scores_binary)
inv_recall = 1.0 - recall
cal_constants = thresholds - inv_recall[:-1]
fit_cal_constants = [0.0] + list(cal_constants) + [0.0]
fit_thresholds = [0.0] + list(thresholds) + [1.0]
calibrate = interp1d(fit_thresholds, fit_cal_constants)

#save calibration data to a file
cal_df = pd.DataFrame(data=np.array([[1.0] + list(precision), [1.0] + list(recall), [0.0] + list(thresholds) + [1.0]]).T, columns=['PRECISION', 'RECALL', 'THRESHOLD'])
cal_df.to_csv('%s/calibration.csv' %event_dir, index=False)

def calibrate_kn(probs, calibrate=calibrate):
    calibrated_probs = []
    for prob in probs:
        #calibrated_prob = calibrate(prob) + prob
        calibrated_prob = prob - calibrate(prob)

        calibrated_probs.append(calibrated_prob)
        #if calibrated_prob > 1.0:
        #    calibrated_probs.append(1.0)
        #elif calibrated_prob < 0.0:
        #    calibrated_probs.append(0.0)
        #else:
        #    calibrated_probs.append(calibrated_prob)
    
    return calibrated_probs


def calibrate_sn(cc_probs, ia_probs, probs, calibrate_kn=calibrate):
    calibrated_probs = []
    for ia_prob, cc_prob, prob in zip(ia_probs, cc_probs, probs):
        if ia_prob + cc_prob == 0.0:
            calibrated_probs.append(0.0)
        else:
            kn_prob = 1.0 - (ia_prob + cc_prob)
            calibrated_kn_prob = calibrate_kn(kn_prob)
            calibrated_sn_prob = 1.0 - calibrated_kn_prob
            subclass_fraction = prob / (ia_prob + cc_prob)
            calibrated_subclass_prob = subclass_fraction * calibrated_sn_prob

            calibrated_probs.append(calibrated_subclass_prob)
            #if calibrated_subclass_prob < 0.0:
            #    calibrated_probs.append(0.0)
            #elif calibrated_subclass_prob > 1.0:
            #    calibrated_probs.append(1.0)
            #else:
            #    calibrated_probs.append(calibrated_subclass_prob)

    return calibrated_probs



#save results
train_df['PROB_CC'] = calibrate_sn(train_pred[:,0], train_pred[:,1], train_pred[:,0])
train_df['PROB_Ia'] = calibrate_sn(train_pred[:,0], train_pred[:,1], train_pred[:,1])
train_df['PROB_KN'] = calibrate_kn(train_pred[:,2])
test_df['PROB_CC'] = calibrate_sn(test_pred[:,0], test_pred[:,1], test_pred[:,0])
test_df['PROB_Ia'] = calibrate_sn(test_pred[:,0], test_pred[:,1], test_pred[:,1])
test_df['PROB_KN'] = calibrate_kn(test_pred[:,2])
data_df['PROB_CC'] = calibrate_sn(data_pred[:,0], data_pred[:,1], data_pred[:,0])
data_df['PROB_Ia'] = calibrate_sn(data_pred[:,0], data_pred[:,1], data_pred[:,1])
data_df['PROB_KN'] = calibrate_kn(data_pred[:,2])


#output results
train_df.to_csv('%s/pred_train.csv' %event_dir, index=False)
test_df.to_csv('%s/pred_test.csv' %event_dir, index=False)
data_df.to_csv('%s/pred_data.csv' %event_dir, index=False)
