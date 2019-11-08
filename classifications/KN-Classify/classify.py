# A module to perform ML classification on a single dataset

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

def classify(train_df, test_df, n_jobs=-1):
    # Encode KN vs All scheme
    kn_truth = [1 if x == 'KN' else 0 for x in train_df['OBJ'].values]
    train_df['KN'] = kn_truth

    # Force numeric features
    metadata_cols = ['OBJ', 'KN']
    numeric_cols = [x for x in train_df.columns if x not in metadata_cols]
    train_df[numeric_cols] = train_df[numeric_cols].apply(pd.to_numeric)

    # Break train_df in training and validation sets
    all_features = [x for x in numeric_cols if x not in ['CID', 'SNID']]
    X = train_df[all_features]
    y = train_df['KN']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6, stratify=y)

    # Instantiate classifier
    rfc = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=6, criterion='gini')
    
    # Perform a grid search to find the best hyperparameters
    param_grid = {'criterion': ['gini', 'entropy'],
                  'n_estimators': [10, 50, 100, 500],
                  'max_depth': [5, 10, 20, 50],
                  'class_weight': ['balanced', [{0: 1, 1: 1}, {0: 5, 1:5}]]}
    gs = GridSearchCV(rfc, param_grid, n_jobs=n_jobs, cv=5)
    gs.fit(X_train, y_train)

    # Instantiate a new RFC with the best parameters
    rfc = RandomForestClassifier(gs.best_params_)

    # Determine which features are prone to overfitting
    rfc.fit(X_train, y_train)
    
    #^consider histogramming the feature importances
