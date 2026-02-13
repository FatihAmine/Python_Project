
import os
import sys
import json
import random
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )
    GA_LIB_AVAILABLE = True
except ImportError:
    GA_LIB_AVAILABLE = False
    print("Warning: google-analytics-data library not found. Running in mock mode.")


SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_PATH = SCRIPT_DIR / 'ga_credentials.json'
OUTPUT_DIR = SCRIPT_DIR / 'ga_output'

PROPERTY_ID = '523449289'

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_real_fetch():
    if not GA_LIB_AVAILABLE:
        return False
        
    if not CREDENTIALS_PATH.exists():
        return False
        
    print(f"[Auth] Found credentials at {CREDENTIALS_PATH}")
    print("[Connect] Connecting to Google Analytics 4...")
    
    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(CREDENTIALS_PATH)
        client = BetaAnalyticsDataClient()
        
        print("   - Fetching events by type...")
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[Dimension(name="eventName")],
            metrics=[Metric(name="eventCount")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )
        response = client.run_report(request)
        
        events_data = []
        for row in response.rows:
            events_data.append({
                "event_type": row.dimension_values[0].value,
                "count": int(row.metric_values[0].value)
            })
        
        pd.DataFrame(events_data).to_csv(OUTPUT_DIR / 'ga_events_by_type.csv', index=False)
        
        print("   - Fetching events over time...")
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[Dimension(name="date"), Dimension(name="hour")],
            metrics=[Metric(name="eventCount")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
            order_bys=[{"dimension": {"dimension_name": "date"}}, {"dimension": {"dimension_name": "hour"}}]
        )
        response = client.run_report(request)
        
        time_data = []
        for row in response.rows:
            date_str = row.dimension_values[0].value
            hour_str = row.dimension_values[1].value
            dt_str = f"{date_str} {hour_str}:00:00"
            try:

                dt = datetime.strptime(dt_str, "%Y%m%d %H:%M:%S")
                time_data.append({
                    "datetime": dt,
                    "count": int(row.metric_values[0].value)
                })
            except ValueError:
                continue
                
        pd.DataFrame(time_data).to_csv(OUTPUT_DIR / 'ga_events_over_time.csv', index=False)
        
        print("   - Fetching add to cart data...")
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[Dimension(name="pageTitle")],
            metrics=[Metric(name="eventCount")],
            dimension_filter={
                "filter": {
                    "field_name": "eventName",
                    "string_filter": {"value": "add_to_cart"}
                }
            },
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )
        response = client.run_report(request)
        
        cart_data = []
        for row in response.rows:
            cart_data.append({
                "product_name": row.dimension_values[0].value,
                "add_to_cart_count": int(row.metric_values[0].value)
            })
            
        pd.DataFrame(cart_data).to_csv(OUTPUT_DIR / 'ga_add_to_cart.csv', index=False)
        
        print("[OK] Real data fetched successfully!")
        return True
        
    except Exception as e:
        print(f"[Error] fetching from GA4: {e}")
        return False

def run_mock_fetch():
    print("[Warn] No credentials found or API failed. Generating MOCK data...")
    
    # 1. Events by Type (Dynamic)
    events_by_type = [
        {"event_type": "page_view", "count": random.randint(10, 50)},
        {"event_type": "view_item", "count": random.randint(5, 30)},
        {"event_type": "add_to_cart", "count": random.randint(1, 15)},
        {"event_type": "remove_from_cart", "count": random.randint(0, 5)},
        {"event_type": "session_start", "count": random.randint(5, 20)},
        {"event_type": "first_visit", "count": random.randint(1, 10)}
    ]
    pd.DataFrame(events_by_type).to_csv(OUTPUT_DIR / 'ga_events_by_type.csv', index=False)
    
    # 2. Events Over Time (Dynamic)
    time_data = []
    now = datetime.now()
    for i in range(24):
        dt = now - timedelta(hours=i)
        # Random count with normal distribution
        count = max(0, int(random.gauss(5, 3)))
        time_data.append({
            "datetime": dt.strftime("%Y-%m-%d %H:00:00"),
            "count": count
        })
    time_data.sort(key=lambda x: x["datetime"])
    pd.DataFrame(time_data).to_csv(OUTPUT_DIR / 'ga_events_over_time.csv', index=False)
    
    # 3. Add to Cart (Dynamic)
    cart_data = [
        {"product_name": "Wireless Bluetooth Headphones", "add_to_cart_count": random.randint(1, 5)},
        {"product_name": "Smart Watch Pro", "add_to_cart_count": random.randint(0, 3)},
        {"product_name": "Canvas Backpack", "add_to_cart_count": random.randint(0, 4)},
        {"product_name": "Ergonomic Mouse", "add_to_cart_count": random.randint(0, 2)}
    ]
    pd.DataFrame(cart_data).to_csv(OUTPUT_DIR / 'ga_add_to_cart.csv', index=False)
    
    # 4. Summary (Dynamic)
    summary = {
        "total_users": random.randint(5, 20),
        "total_revenue": round(random.uniform(50.0, 500.0), 2),
        "mode": "MOCK",
        "generated_at": datetime.now().isoformat()
    }
    with open(OUTPUT_DIR / 'ga_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
        
    print("[OK] Mock data generated successfully (Randomized)!")

def main():  
    print("[Analytics] GA4 Data Fetcher") 
    ensure_output_dir()
    
    success = False
    if CREDENTIALS_PATH.exists():
        success = run_real_fetch()
    else:
        print("[Info] No 'ga_credentials.json' found.")
    
    if not success:
        run_mock_fetch()
        
    print(f"\n[Output] Files saved to: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
