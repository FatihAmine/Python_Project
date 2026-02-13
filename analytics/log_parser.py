"""Log parser - loads JSON event logs into a DataFrame."""

import os
import json
import glob
from datetime import datetime
from pathlib import Path
import pandas as pd


def parse_timestamp(timestamp_str: str) -> datetime:

    if len(timestamp_str) >= 17:  # With milliseconds
        return datetime.strptime(timestamp_str[:14], "%Y%m%d%H%M%S")
    elif len(timestamp_str) >= 14:
        return datetime.strptime(timestamp_str[:14], "%Y%m%d%H%M%S")
    else:

        return datetime.strptime(timestamp_str[:8], "%Y%m%d")


def load_single_event(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        event = json.load(f)
    

    if 'timestamp' in event:
        event['datetime'] = parse_timestamp(event['timestamp'])
        event['date'] = event['datetime'].date()
        event['hour'] = event['datetime'].hour
    

    event['source_file'] = os.path.basename(filepath)
    
    return event


def load_events_from_directory(logs_dir: str) -> pd.DataFrame:
    logs_path = Path(logs_dir)
    
    if not logs_path.exists():
        print(f"Warning: Logs directory not found: {logs_dir}")
        return pd.DataFrame()
    

    json_files = list(logs_path.glob('**/*.json'))
    
    if not json_files:
        print(f"Warning: No JSON files found in {logs_dir}")
        return pd.DataFrame()
    
    print(f"Found {len(json_files)} event files")
    

    events = []
    for filepath in json_files:
        try:
            event = load_single_event(str(filepath))
            events.append(event)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            continue
    

    df = pd.DataFrame(events)
    

    if not df.empty:

        if 'datetime' in df.columns:
            df = df.sort_values('datetime').reset_index(drop=True)
        

        categorical_cols = ['event_type', 'page', 'element']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')
    
    print(f"Loaded {len(df)} events into DataFrame")
    return df


def get_latest_events(logs_dir: str, hours: int = 24) -> pd.DataFrame:
    df = load_events_from_directory(logs_dir)
    
    if df.empty or 'datetime' not in df.columns:
        return df
    
    cutoff = datetime.now() - pd.Timedelta(hours=hours)
    return df[df['datetime'] >= cutoff].reset_index(drop=True)


if __name__ == '__main__':

    import sys
    
    logs_dir = sys.argv[1] if len(sys.argv) > 1 else '../logs'
    
    print(f"\n=== Testing Log Parser ===")
    print(f"Logs directory: {logs_dir}\n")
    
    df = load_events_from_directory(logs_dir)
    
    if not df.empty:
        print(f"\nDataFrame shape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nSample data:")
        print(df.head())
        print(f"\nEvent types: {df['event_type'].value_counts().to_dict()}")
        print(f"\nPages: {df['page'].value_counts().to_dict()}")
    else:
        print("No events loaded.")
