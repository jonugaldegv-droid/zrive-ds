from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, auc, roc_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def split_features_target(
        df: pd.DataFrame
    ):
    target_col = 'outcome'
    info_cols = ['variant_id', 'order_id', 'user_id', 'created_at', 'order_date']
    cat_cols = ['product_type', 'vendor']
    binary_cols = ['ordered_before', 'abandoned_before', 'active_snoozed', 'set_as_regular']
    exclude_cols = ['days_since_purchase_variant_id', 'days_since_purchase_product_type']

    feature_cols = [col for col in df.columns if col not in info_cols + [target_col] + exclude_cols]
    numeric_cols = [col for col in feature_cols if col not in cat_cols + binary_cols]

    train_cols = numeric_cols + binary_cols

    X = df[train_cols]
    y = df[target_col]

    return X, y

def plot_metrics(
        model_name : str,
        y_pred : pd.Series,
        y_test : pd.Series,
        figure: tuple[matplotlib.figure.Figure, np.array] = None
    ):
    
    precision_, recall_, _ = precision_recall_curve(y_test, y_pred)
    pr_auc = auc(recall_, precision_)

    fpr, tpr, _ = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)

    if figure is None:
        fig, ax = plt.subplots(1, 2, figsize = (14, 8))
    else:
        fig, ax = figure

    ax[0].plot(recall_, precision_, label = f'{model_name} -> AUC={pr_auc:.3f}')
    ax[0].set_xlabel('Recall')
    ax[0].set_ylabel('Precision')
    ax[0].set_title(f'Precision-Recall Curve')
    ax[0].legend()

    ax[1].plot(fpr, tpr, label = f'{model_name} -> AUC={roc_auc:.3f}')
    ax[1].set_xlabel('FPR')
    ax[1].set_ylabel('TPR')
    ax[1].set_title(f'ROC Curve')
    ax[1].legend()

    fig.show()

def train_model(
        df_train: pd.DataFrame,
        df_val: pd.DataFrame,
    ):

    X_train, y_train = split_features_target(df_train)
    X_val, y_val = split_features_target(df_val)

    XGB = make_pipeline(
        StandardScaler(),
        GradientBoostingClassifier()
    )

    XGB.fit(X_train, y_train)

    val_proba = XGB.predict_proba(X_val)[:,1]

    plot_metrics('Gradient Boosting', y_pred = val_proba, y_test = y_val)

    return XGB