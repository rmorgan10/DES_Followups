# Classifier for PSNID + RFC method

import numpy as np
import pandas as pd
import sys
from scipy.interpolate import interp1d

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve

event_name = sys.argv[1]
event_dir = '../../events/%s/PSNID' %event_name
signal = sys.argv[2]
background = sys.argv[3] #comma-separated list of background objects
sim_include = signal + ',' + background

#load training and testing sets
train_df = pd.read_csv('%s/training_set.csv' %event_dir)
test_df = pd.read_csv('%s/testing_set.csv' %event_dir)

#load full sim_dfs
sig_df = pd.read_csv('%s/full_feat_df_%s.csv' %(event_dir, signal))  

bkg_info = {'df': {}, 'pred':{}}
for obj in background.split(','):
    bkg_info['df'][obj] = pd.read_csv('%s/full_feat_df_%s.csv' %(event_dir, obj))

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
## note labels are in alphabetical order: e.g. (CC = 0, Ia = 1, KN = 2)
train_pred = rfc.predict_proba(train_df[feats])
test_pred = rfc.predict_proba(test_df[feats])
data_pred = rfc.predict_proba(data_df[feats])

sig_pred = rfc.predict_proba(sig_df[feats])
for obj in background.split(','):
    bkg_info['pred'][obj] = rfc.predict_proba(bkg_info['df'][obj][feats])

#calibrate KN probabilities to Purity of test set
test_labels_binary = [int(x == signal) for x in test_df['CLASS'].values]
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

def calibrate_sig(probs, calibrate=calibrate):
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


def calibrate_bkg(bkg_prob_list, probs, calibrate_sig=calibrate):
    calibrated_probs = []
    for bkg_probs, prob in zip(bkg_prob_list, probs):
        if sum(bkg_probs) == 0.0:
            calibrated_probs.append(0.0)
        else:
            sig_prob = 1.0 - sum(bkg_probs)
            calibrated_sig_prob = calibrate_sig(sig_prob)
            calibrated_bkg_prob = 1.0 - calibrated_sig_prob
            subclass_fraction = prob / sum(bkg_probs)
            calibrated_subclass_prob = subclass_fraction * calibrated_bkg_prob

            calibrated_probs.append(calibrated_subclass_prob)
            #if calibrated_subclass_prob < 0.0:
            #    calibrated_probs.append(0.0)
            #elif calibrated_subclass_prob > 1.0:
            #    calibrated_probs.append(1.0)
            #else:
            #    calibrated_probs.append(calibrated_subclass_prob)

    return calibrated_probs

# bkg_prob_list
#[[obj1_ia_prob, obj_1_cc_prob, ...], [obj2_ia_prob, obj2_cc_prob, ...], ...]
# the generation of this list is currently not very efficient

#save results
sorted_bkg = sorted(background.split(','))
sorted_sim_include = sorted(sim_include.split(','))
train_bkg_prob_list = [[train_pred[obj_idx, class_idx] for class_idx in [sorted_sim_include.index(x) for x in sorted_bkg]] for obj_idx in range(len(train_pred))]
for obj in background.split(','):
    obj_probs = train_pred[:, sorted_sim_include.index(obj)]
    train_df['PROB_%s' %obj] = calibrate_bkg(train_bkg_prob_list, obj_probs)
train_df['PROB_%s' %signal] = calibrate_sig(train_pred[:, sorted_sim_include.index(signal)])

#train_df['PROB_CC'] = calibrate_sn(train_pred[:,0], train_pred[:,1], train_pred[:,0])
#train_df['PROB_Ia'] = calibrate_sn(train_pred[:,0], train_pred[:,1], train_pred[:,1])
#train_df['PROB_KN'] = calibrate_kn(train_pred[:,2])

test_bkg_prob_list = [[test_pred[obj_idx, class_idx] for class_idx in [sorted_sim_include.index(x) for x in sorted_bkg]] for obj_idx in range(len(test_pred))]
for obj in background.split(','):
    obj_probs = test_pred[:, sorted_sim_include.index(obj)]
    test_df['PROB_%s' %obj] = calibrate_bkg(test_bkg_prob_list, obj_probs)
test_df['PROB_%s' %signal] = calibrate_sig(test_pred[:, sorted_sim_include.index(signal)])

#test_df['PROB_CC'] = calibrate_sn(test_pred[:,0], test_pred[:,1], test_pred[:,0])
#test_df['PROB_Ia'] = calibrate_sn(test_pred[:,0], test_pred[:,1], test_pred[:,1])
#test_df['PROB_KN'] = calibrate_kn(test_pred[:,2])

data_bkg_prob_list = [[data_pred[obj_idx, class_idx] for class_idx in [sorted_sim_include.index(x) for x in sorted_bkg]] for obj_idx in range(len(data_pred))]
for obj in background.split(','):
    obj_probs = data_pred[:, sorted_sim_include.index(obj)]
    data_df['PROB_%s' %obj] = calibrate_bkg(data_bkg_prob_list, obj_probs)
data_df['PROB_%s' %signal] = calibrate_sig(data_pred[:, sorted_sim_include.index(signal)])

#data_df['PROB_CC'] = calibrate_sn(data_pred[:,0], data_pred[:,1], data_pred[:,0])
#data_df['PROB_Ia'] = calibrate_sn(data_pred[:,0], data_pred[:,1], data_pred[:,1])
#data_df['PROB_KN'] = calibrate_kn(data_pred[:,2])

sig_bkg_prob_list = [[sig_pred[obj_idx, class_idx] for class_idx in [sorted_sim_include.index(x) for x in sorted_bkg]] for obj_idx in range(len(sig_pred))]
for obj in background.split(','):
    obj_probs = sig_pred[:, sorted_sim_include.index(obj)]
    sig_df['PROB_%s' %obj] = calibrate_bkg(sig_bkg_prob_list, obj_probs)
sig_df['PROB_%s' %signal] = calibrate_sig(sig_pred[:, sorted_sim_include.index(signal)]) 

#kn_df['PROB_CC'] = calibrate_sn(kn_pred[:,0], kn_pred[:,1], kn_pred[:,0])
#kn_df['PROB_Ia'] = calibrate_sn(kn_pred[:,0], kn_pred[:,1], kn_pred[:,1])
#kn_df['PROB_KN'] = calibrate_kn(kn_pred[:,2])

for mainobj in bkg_info['pred'].keys():
    mainobj_bkg_prob_list = [[bkg_info['pred'][mainobj][obj_idx, class_idx] for class_idx in [sorted_sim_include.index(x) for x in sorted_bkg]] for obj_idx in range(len(bkg_info['pred'][mainobj]))]
    for obj in background.split(','):
        obj_probs = bkg_info['pred'][mainobj][:, sorted_sim_include.index(obj)]
        bkg_info['df'][mainobj]['PROB_%s' %obj] = calibrate_bkg(mainobj_bkg_prob_list, obj_probs)
    bkg_info['df'][mainobj]['PROB_%s' %signal] = calibrate_sig(bkg_info['pred'][mainobj][:,sorted_sim_include.index(signal)])

#ia_df['PROB_CC'] = calibrate_sn(ia_pred[:,0], ia_pred[:,1], ia_pred[:,0])
#ia_df['PROB_Ia'] = calibrate_sn(ia_pred[:,0], ia_pred[:,1], ia_pred[:,1])
#ia_df['PROB_KN'] = calibrate_kn(ia_pred[:,2])
#cc_df['PROB_CC'] = calibrate_sn(cc_pred[:,0], cc_pred[:,1], cc_pred[:,0])
#cc_df['PROB_Ia'] = calibrate_sn(cc_pred[:,0], cc_pred[:,1], cc_pred[:,1])
#cc_df['PROB_KN'] = calibrate_kn(cc_pred[:,2])

#output results
train_df.to_csv('%s/pred_train.csv' %event_dir, index=False)
test_df.to_csv('%s/pred_test.csv' %event_dir, index=False)
data_df.to_csv('%s/pred_data.csv' %event_dir, index=False)

sig_df.to_csv('%s/pred_full_%s.csv' %(event_dir, signal), index=False)
#kn_df.to_csv('%s/pred_full_KN.csv' %event_dir, index=False)

for mainobj in bkg_info['df'].keys():
    bkg_info['df'][mainobj].to_csv('%s/pred_full_%s.csv' %(event_dir, mainobj), index=False)
#ia_df.to_csv('%s/pred_full_Ia.csv' %event_dir, index=False)
#cc_df.to_csv('%s/pred_full_CC.csv' %event_dir, index=False)
