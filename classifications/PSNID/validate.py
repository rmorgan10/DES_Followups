# A module to validate classification results by making plots

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.utils.multiclass import unique_labels

from matplotlib import rcParams
rcParams['font.family'] = 'serif'

np.set_printoptions(precision=2)

event_name = sys.argv[1]
event_dir = '../../events/%s/PSNID' %event_name
signal = sys.argv[2]
background = sys.argv[3] #comma-separated list of background objects
sim_include = signal + ',' + background

#One-hot encoding
encode = {obj: idx for idx, obj in enumerate(sorted(sim_include.split(',')))}

data = pd.read_csv('%s/opt_pred_data.csv' %event_dir)
test = pd.read_csv('%s/opt_pred_test.csv' %event_dir)
train = pd.read_csv('%s/opt_pred_train.csv' %event_dir)
feat_df = pd.read_csv('%s/opt_feat_importances.csv' %event_dir).sort_values(by='IMPORTANCE', ascending=False).reset_index(drop=True)


candidate_cut_res_df = pd.read_csv('../../events/%s/cut_results/LightCurvesReal_candidate_summary.txt' %event_name)
candidate_snids = np.array(candidate_cut_res_df['SNID'].values, dtype=int)



def get_operating_threshold(fpr, tpr, thresholds):
    fpr_tolerance = 0.01
    cond = (fpr < fpr_tolerance)
    
    trimmed_fpr = fpr[cond]
    trimmed_tpr = tpr[cond]
    trimmed_thresholds = thresholds[cond]
    
    return trimmed_thresholds[np.argmax(trimmed_tpr)], trimmed_fpr[np.argmax(trimmed_tpr)], np.max(trimmed_tpr)

def apply_color_map(names):
    colors = []
    for name in names:
        colors.append(apply_color_map_single(name))
    return colors

def apply_color_map_single(name):
    if name.find('Ia') != -1:
        return '#66c2a5'
    elif name.find('Ibc') != -1:
        return '#fc8d62'
    elif name.find('II') != -1:
        return '#8da0cb'
    else:
        return 'gray'

def apply_name_map(names):
    labels = []
    for name in names:
        labels.append(apply_name_map_single(name))
    return labels

def apply_name_map_single(name):
    if name.find('Ia') != -1:
        return 'Ia-Based Feature'
    elif name.find('Ibc') != -1:
        return 'Ibc-Based Feature'
    elif name.find('II') != -1:
        return 'II-Based Feature'
    else:
        return 'Other Feature'

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title='',
                          cmap=plt.cm.Blues, event_dir=event_dir):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #print("Normalized confusion matrix")
    else:
        #print('Confusion matrix, without normalization')
        pass

    #print(cm)

    fig, ax = plt.subplots(figsize=(6,4), dpi=120)
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    #ax.set(xticks=np.arange(cm.shape[1]),
    #       yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
    #       xticklabels=classes, yticklabels=classes,
    #       title=title,
    #       ylabel='True Class',
    #       xlabel='Predicted Class')
    
    ax.set_xticks(np.arange(cm.shape[1]))
    ax.set_yticks(np.arange(cm.shape[0]))
    ax.set_xticklabels(classes, fontsize=12)
    ax.set_yticklabels(classes, fontsize=12)
    ax.set_xlabel('Predicted Class', fontsize=14)
    ax.set_ylabel('True Class', fontsize=14)

    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black", fontsize=12)
    fig.tight_layout()
    fig.savefig('%s/res_confusion_matrix.pdf' %event_dir)

    plt.close()

    return 
        


# ROC Curve

binary_labels = np.array([int(x == signal) for x in test['CLASS'].values])
binary_scores = np.array(test['PROB_%s' %signal].values, dtype=float)

fpr, tpr, thresholds = roc_curve(binary_labels, binary_scores)
auc = roc_auc_score(binary_labels, binary_scores)

fpr = np.array([0.0] + list(fpr) + [1.0])
tpr = np.array([0.0] + list(tpr) + [1.0])
thresholds = np.array([1.0] + list(thresholds) + [0.0])

op_threshold, op_fpr, op_tpr = get_operating_threshold(fpr, tpr, thresholds)

out_dict = {'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds}
np.save('%s/ml_curves.npy' %event_dir, out_dict)


plt.figure(figsize=(6,4), dpi=120)

cm = plt.get_cmap('viridis') 

garb = plt.scatter(fpr + 80, tpr + 80, c=thresholds)

plt.plot([0,0,1], [0,1,1], ls='dotted', lw=2, color='black', label='Perfect Performance (AUC = 1.0)')

for i in range(len(fpr) -1):
    if i > len(fpr) - 3:
        plt.plot([fpr[i], fpr[i+1]], [tpr[i], tpr[i+1]], c=cm(thresholds[i]), lw=2, zorder=20, label='PSNID+RFC (AUC = %.3f)' %auc)
    else:
        plt.plot([fpr[i], fpr[i+1]], [tpr[i], tpr[i+1]], c=cm(thresholds[i]), lw=2, zorder=20, label=None)
        
        
plt.plot([0,1], [0,1], ls='--', lw=2, color='gray', label='Random Guessing (AUC = 0.5)')

plt.scatter([op_fpr], [op_tpr], marker='*', color='black', s=80, zorder=40, label='Operating Threshold = %.3f' %op_threshold)

plt.xlabel("%s False Positive Rate" %signal, fontsize=14)
plt.ylabel("%s True Positive Rate" %signal, fontsize=14)

plt.colorbar(garb, label='%s Probability Threshold' %signal)

plt.legend()

plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)

plt.tight_layout()

plt.savefig('%s/res_roc.pdf' %event_dir)

plt.close()

# Feature Importances

feat_df['INDEX'] = np.arange(feat_df.shape[0])
feat_df['COLOR'] = apply_color_map(feat_df['FEATURE'])
feat_df['LABEL'] = apply_name_map(feat_df['FEATURE'])

plt.figure(figsize=(6,4), dpi=120)

plt.bar(feat_df['INDEX'], feat_df['IMPORTANCE'], alpha=0.7, color=feat_df['COLOR'], label=None)

plt.xlabel("PSNID Feature", fontsize=14)
plt.ylabel("Relative Importance", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

#hack to fill in lengend
for color in np.unique(feat_df['COLOR']):
    label = feat_df['LABEL'].values[feat_df['COLOR'].values == color][0]
    plt.fill_between([0,2], [2,2], [3,3], color=color, alpha=0.7, label=label)


plt.ylim(0.0, np.max(feat_df['IMPORTANCE'].values) + 0.01)

plt.legend(fontsize=14)

plt.tight_layout()

plt.savefig('%s/res_feat_importances.pdf' %event_dir)

plt.close()

# Confusion Matrix

class_names = np.array(sorted(sim_include.split(',')))
y_test_label = [encode[x] for x in test['CLASS'].values]
y_test_pred = []
for index, row in test.iterrows():
    y_test_pred.append(class_names[np.argmax(np.array([row['PROB_%s' %obj] for obj in sorted(sim_include.split(','))]))])
y_test_pred_label = [encode[x] for x in y_test_pred]

plot_confusion_matrix(y_test_label, y_test_pred_label, classes=class_names, normalize=True)


# Candidate probabilities
confirmed_spec = []

for index, row in data.iterrows():
    if int(row['CID']) not in candidate_snids:
        confirmed_spec.append(1)
    else:
        confirmed_spec.append(0)
data['SPEC'] = confirmed_spec
        
sorted_data = data.sort_values(by='PROB_%s' %signal, ascending=False)
sorted_data['INDEX'] = np.arange(data.shape[0])

plt.figure(figsize=(6,4), dpi=120)

plt.bar(sorted_data['INDEX'].values[sorted_data['SPEC'].values == 1], 
        sorted_data['PROB_%s' %signal].values[sorted_data['SPEC'].values == 1],
        color='#d95f02', label=None)
plt.bar(sorted_data['INDEX'].values[sorted_data['SPEC'].values == 0], 
        sorted_data['PROB_%s' %signal].values[sorted_data['SPEC'].values == 0], 
        color='#7570b3', label=None)

color_dict = {0:'#7570b3', 1:'#d95f02'}
for index, row in sorted_data.iterrows():
    if row['PROB_%s' %signal] == 0.0:
        plt.arrow(row['INDEX'], 0.15, 0, -0.1,
                  color=color_dict[row['SPEC']], head_length=0.025, width=0.1,
                  length_includes_head=True)

plt.axhline(y=op_threshold, color='black', ls='--', lw=2)

plt.xticks(sorted_data['INDEX'], sorted_data['CID'], rotation=45, fontsize=12)

plt.ylabel("PSNID+RFC %s Probability" %signal, fontsize=14)
plt.xlabel("DESGW Candidate", fontsize=14)

plt.text(np.max(sorted_data['INDEX']) + 0.5, op_threshold + 0.01, 'Operating Threshold = %.3f' %op_threshold, 
         fontsize=12, horizontalalignment='right')

plt.ylim(0.0, op_threshold + 0.05)

plt.fill_between([0,1], [200, 200], [300, 300], color='#7570b3', label='No Spectroscopic Information')
plt.fill_between([0,1], [200, 200], [300, 300], color='#d95f02', label='Spectroscopic Confirmed SN')


plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=[0.99, 0.8])

plt.tight_layout()

plt.savefig('%s/res_candidate_probabilities.pdf' %event_dir)

plt.close()

# Numeric metrics
tp = float(np.sum(np.ones(test.shape[0])[(test['CLASS'].values == signal) & (test['PROB_%s' %signal].values > op_threshold)]))
fp = float(np.sum(np.ones(test.shape[0])[(test['CLASS'].values != signal) & (test['PROB_%s' %signal].values > op_threshold)]))
tn = float(np.sum(np.ones(test.shape[0])[(test['CLASS'].values != signal) & (test['PROB_%s' %signal].values < op_threshold)]))
fn = float(np.sum(np.ones(test.shape[0])[(test['CLASS'].values == signal) & (test['PROB_%s' %signal].values < op_threshold)]))

purity = tp / (tp + fp)
completeness = tp / (tp + fn)
accuracy = (tp + tn) / (tp + tn + fp + fn)
false_positive_rate = fp / (tn + fp)
true_positive_rate = tp / (tp + fn)
false_discovery_rate = fp / (fp + tp)
false_omission_rate = fn / (fn + tn)

info_to_write = []
info_to_write.append("Operating Threshold: %.5f" %op_threshold)
info_to_write.append("Purity: %.5f" %purity)
info_to_write.append("Completeness: %.5f" %completeness)
info_to_write.append("Accuracy: %.5f" %accuracy)
info_to_write.append("False Positive Rate: %.5f" % false_positive_rate)
info_to_write.append("True Positive Rate: %.5f" % true_positive_rate)
info_to_write.append("False Discovery Rate: %.5f" %false_discovery_rate)
info_to_write.append("False Omission Rate: %.5f" %false_omission_rate)

stream = open('%s/res_numeric_metrics.txt' %event_dir, 'w+')
stream.writelines([x + '\n' for x in info_to_write])
stream.close()

# feature names
feat_df.to_csv('%s/res_feat_names.csv' %event_dir)
