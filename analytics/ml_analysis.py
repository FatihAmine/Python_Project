"""
Machine Learning Analysis - Conversion Prediction
"""

import pandas as pd
import numpy as np
import warnings
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from termcolor import colored

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

try:
    from log_parser import load_events_from_directory
except ImportError:
    # Handle direct execution vs module import
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from log_parser import load_events_from_directory

def prepare_features(df):
    """
    Groups events by user_id to create session-level features.
    Target: did the user visit 'cart'?
    """
    if df.empty:
        return pd.DataFrame(), pd.Series()

    # Sort by time
    df = df.sort_values(['user_id', 'timestamp'])

    # Group by user_id
    user_groups = df.groupby('user_id')

    features = []
    targets = []

    for user_id, user_data in user_groups:
        # Feature: Total Events
        total_events = len(user_data)

        # Feature: Unique Pages
        unique_pages = user_data['page'].nunique()

        # Feature: Product View Count
        product_views = len(user_data[user_data['page'] == 'product'])

        # Feature: Session Duration (seconds)
        if 'datetime' in user_data.columns:
            start_time = user_data['datetime'].min()
            end_time = user_data['datetime'].max()
            duration = (end_time - start_time).total_seconds()
        else:
            duration = 0

        # Feature: Clicks
        clicks = len(user_data[user_data['event_type'] == 'click'])

        features.append({
            'total_events': total_events,
            'unique_pages': unique_pages,
            'product_views': product_views,
            'duration': duration,
            'clicks': clicks
        })

        # Target: Converted? (Visited Cart)
        is_converted = 1 if 'cart' in user_data['page'].values else 0
        targets.append(is_converted)

    X = pd.DataFrame(features)
    y = pd.Series(targets)

    return X, y

def train_and_evaluate(X, y):
    """
    Trains a Random Forest model and evaluates it.
    """
    if len(X) < 5:
        print(colored("Not enough data to train a model (need at least 5 sessions).", "red"))
        return None

    # Split Data (80% Train, 20% Test)
    # Use stratify to maintain class balance
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    except ValueError:
        # Fallback if classes are too imbalanced for stratification
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training set: {len(X_train)} sessions")
    print(f"Testing set: {len(X_test)} sessions")

    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    
    y_pred = model.predict(X_test)

    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(colored("\n--- Model Evaluation ---", "cyan"))
    print(f"Accuracy:  {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall:    {recall:.2f}")
    print(f"F1 Score:  {f1:.2f}")

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }

    return model, metrics, X_test, y_test, y_pred

def show_feature_importance(model, feature_names):
    if model is None: return

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    print(colored("\n--- Feature Importance ---", "cyan"))
    for f in range(len(feature_names)):
        print(f"{f+1}. {feature_names[indices[f]]}: {importances[indices[f]]:.4f}")

def main():
    print(colored("\n=== Machine Learning Analysis: Conversion Prediction ===", "green"))
    
    
    print("Loading data...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, '..', 'logs')
    
    df = load_events_from_directory(logs_dir)
    if df.empty:
        print(colored("No data found. Exiting.", "red"))
        return

    
    print("Preparing features...")
    X, y = prepare_features(df)
    
    print(f"Total Sessions: {len(X)}")
    print(f"Conversion Rate: {y.mean():.2%}")

    if len(X) == 0:
        print("No sessions extracted.")
        return

    
    print("Training model...")
    model, metrics, X_test, y_test, y_pred = train_and_evaluate(X, y)

    
    if model:
        output_dir = os.path.join(script_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        
        metrics_file = os.path.join(output_dir, 'ml_metrics.json')
        import json
        
        
        cm_list = metrics['confusion_matrix'].tolist()
        metrics['confusion_matrix'] = cm_list
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"Metrics saved to {metrics_file}")
        
        
        feature_importance_file = os.path.join(output_dir, 'feature_importance.csv')
        importances = model.feature_importances_
        feature_df = pd.DataFrame({
            'feature': X.columns,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        feature_df.to_csv(feature_importance_file, index=False)
        print(f"Feature importance saved to {feature_importance_file}")

        show_feature_importance(model, X.columns)
        
    print(colored("\n=== Analysis Complete ===", "green"))

if __name__ == '__main__':
    main()
