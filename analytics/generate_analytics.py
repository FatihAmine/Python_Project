"""Generates analytics CSV files from event logs."""

import os
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from log_parser import load_events_from_directory
from metrics import (
    calculate_all_metrics,
    get_events_by_type_df,
    get_events_by_page_df,
    get_events_over_time_df,
    calculate_ecommerce_metrics
)


def ensure_output_dir(output_dir: str) -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def generate_analytics(logs_dir: str, output_dir: str) -> dict:
    print("[Analytics] E-Commerce Analytics Generator")
  
    ensure_output_dir(output_dir)
    

    print(f"[Load] Loading events from: {logs_dir}")
    df = load_events_from_directory(logs_dir)
    
    if df.empty:
        print("[Error] No events found. Exiting.")
        return {}
    
    print(f"[OK] Loaded {len(df)} events\n")
    

    print("[Calc] Calculating metrics...")
    all_metrics = calculate_all_metrics(df)
    

    print("  -> Generating events_by_type.csv")
    events_by_type = get_events_by_type_df(df)
    events_by_type.to_csv(os.path.join(output_dir, 'events_by_type.csv'), index=False)
    

    print("  -> Generating events_by_page.csv")
    events_by_page = get_events_by_page_df(df)
    events_by_page.to_csv(os.path.join(output_dir, 'events_by_page.csv'), index=False)
    

    print("  -> Generating events_over_time.csv")
    events_over_time = get_events_over_time_df(df, granularity='hour')
    events_over_time.to_csv(os.path.join(output_dir, 'events_over_time.csv'), index=False)
    

    print("  -> Generating add_to_cart_by_product.csv")
    ecom_metrics = calculate_ecommerce_metrics(df)
    ecom_metrics['add_to_cart_by_product'].to_csv(
        os.path.join(output_dir, 'add_to_cart_by_product.csv'), 
        index=False
    )
    

    print("  -> Generating summary.json")
    summary = {
        'total_events': all_metrics['general']['total_events'],
        'total_page_visits': all_metrics['general']['total_page_visits'],
        'total_clicks': all_metrics['general']['total_clicks'],
        'unique_users': all_metrics['general']['unique_users'],
        'add_to_cart_count': ecom_metrics['add_to_cart_count'],
        'events_by_type': all_metrics['general']['events_by_type'],
        'events_by_page': all_metrics['general']['events_by_page'],
        'funnel': all_metrics['funnel'],
        'generated_at': str(df['datetime'].max()) if 'datetime' in df.columns else None
    }
    
    with open(os.path.join(output_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    

    print("[OK] Analytics generation complete!")

    print(f"\n[Output] Files saved to: {output_dir}")
    print(f"\n[Summary]")
    print(f"   - Total Events: {summary['total_events']}")
    print(f"   - Unique Users: {summary['unique_users']}")
    print(f"   - Page Visits: {summary['total_page_visits']}")
    print(f"   - Clicks: {summary['total_clicks']}")
    print(f"   - Add to Cart: {summary['add_to_cart_count']}")
    
    return summary


if __name__ == '__main__':

    script_dir = Path(__file__).parent
    logs_dir = script_dir.parent / 'logs'
    output_dir = script_dir / 'output'
    

    if len(sys.argv) > 1:
        logs_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    
    generate_analytics(str(logs_dir), str(output_dir))
