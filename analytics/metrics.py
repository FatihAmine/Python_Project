"""Metrics calculation from event data."""

import pandas as pd
from datetime import datetime
from typing import Dict, Any


def calculate_general_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {
            'total_events': 0,
            'total_page_visits': 0,
            'total_clicks': 0,
            'unique_users': 0,
            'events_by_type': {},
            'events_by_page': {}
        }
    
    return {
        'total_events': len(df),
        'total_page_visits': len(df[df['event_type'] == 'page_visit']),
        'total_clicks': len(df[df['event_type'] == 'click']),
        'unique_users': df['user_id'].nunique(),
        'events_by_type': df['event_type'].value_counts().to_dict(),
        'events_by_page': df['page'].value_counts().to_dict()
    }


def calculate_time_metrics(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    if df.empty or 'datetime' not in df.columns:
        return {
            'events_per_hour': pd.DataFrame(),
            'events_per_day': pd.DataFrame()
        }
    

    df_hourly = df.copy()
    df_hourly['hour_bucket'] = df_hourly['datetime'].dt.floor('H')
    events_per_hour = df_hourly.groupby('hour_bucket').size().reset_index(name='event_count')
    events_per_hour.columns = ['datetime', 'event_count']
    

    df_daily = df.copy()
    df_daily['day'] = df_daily['datetime'].dt.date
    events_per_day = df_daily.groupby('day').size().reset_index(name='event_count')
    events_per_day.columns = ['date', 'event_count']
    
    return {
        'events_per_hour': events_per_hour,
        'events_per_day': events_per_day
    }


def calculate_ecommerce_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {
            'add_to_cart_count': 0,
            'add_to_cart_by_product': pd.DataFrame(),
            'view_details_by_product': pd.DataFrame(),
            'top_products_added': []
        }
    

    add_to_cart_df = df[df['element'].isin(['add_to_cart_button', 'add_to_cart_detail_btn'])]
    add_to_cart_count = len(add_to_cart_df)
    

    if not add_to_cart_df.empty and 'product_id' in add_to_cart_df.columns:
        add_to_cart_by_product = add_to_cart_df.groupby('product_id').size().reset_index(name='add_to_cart_count')
        add_to_cart_by_product = add_to_cart_by_product.sort_values('add_to_cart_count', ascending=False)
    else:
        add_to_cart_by_product = pd.DataFrame(columns=['product_id', 'add_to_cart_count'])
    

    view_details_df = df[df['element'] == 'view_details_button']
    if not view_details_df.empty and 'product_id' in view_details_df.columns:
        view_details_by_product = view_details_df.groupby('product_id').size().reset_index(name='view_count')
        view_details_by_product = view_details_by_product.sort_values('view_count', ascending=False)
    else:
        view_details_by_product = pd.DataFrame(columns=['product_id', 'view_count'])
    

    top_products = add_to_cart_by_product.head(10)['product_id'].tolist() if not add_to_cart_by_product.empty else []
    
    return {
        'add_to_cart_count': add_to_cart_count,
        'add_to_cart_by_product': add_to_cart_by_product,
        'view_details_by_product': view_details_by_product,
        'top_products_added': top_products
    }


def calculate_conversion_funnel(df: pd.DataFrame) -> Dict[str, int]:
    if df.empty:
        return {
            'home_visits': 0,
            'product_views': 0,
            'add_to_cart': 0,
            'cart_visits': 0
        }
    

    home_visitors = set(df[df['page'] == 'home']['user_id'].unique())
    

    product_viewers = set(df[df['page'] == 'product']['user_id'].unique())
    

    add_to_cart_users = set(df[df['element'].isin(['add_to_cart_button', 'add_to_cart_detail_btn'])]['user_id'].unique())
    

    cart_visitors = set(df[df['page'] == 'cart']['user_id'].unique())
    
    return {
        'home_visits': len(home_visitors),
        'product_views': len(product_viewers),
        'add_to_cart': len(add_to_cart_users),
        'cart_visits': len(cart_visitors)
    }


def get_events_by_type_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=['event_type', 'count'])
    
    result = df.groupby('event_type').size().reset_index(name='count')
    return result.sort_values('count', ascending=False)


def get_events_by_page_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=['page', 'count'])
    
    result = df.groupby('page').size().reset_index(name='count')
    return result.sort_values('count', ascending=False)


def get_events_over_time_df(df: pd.DataFrame, granularity: str = 'hour') -> pd.DataFrame:
    if df.empty or 'datetime' not in df.columns:
        return pd.DataFrame(columns=['datetime', 'count'])
    
    df_copy = df.copy()
    
    if granularity == 'hour':
        df_copy['time_bucket'] = df_copy['datetime'].dt.floor('H')
    else:  # day
        df_copy['time_bucket'] = df_copy['datetime'].dt.floor('D')
    
    result = df_copy.groupby('time_bucket').size().reset_index(name='count')
    result.columns = ['datetime', 'count']
    return result


def calculate_all_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        'general': calculate_general_metrics(df),
        'time': calculate_time_metrics(df),
        'ecommerce': calculate_ecommerce_metrics(df),
        'funnel': calculate_conversion_funnel(df)
    }


if __name__ == '__main__':

    print("=== Testing Metrics Module ===")
    

    sample_data = [
        {'event_type': 'page_visit', 'page': 'home', 'element': 'page_load', 'product_id': None, 'user_id': 'user1', 'datetime': datetime.now()},
        {'event_type': 'click', 'page': 'home', 'element': 'add_to_cart_button', 'product_id': 'P001', 'user_id': 'user1', 'datetime': datetime.now()},
        {'event_type': 'page_visit', 'page': 'cart', 'element': 'page_load', 'product_id': None, 'user_id': 'user1', 'datetime': datetime.now()},
    ]
    
    df = pd.DataFrame(sample_data)
    
    metrics = calculate_all_metrics(df)
    
    print(f"\nGeneral metrics: {metrics['general']}")
    print(f"\nFunnel: {metrics['funnel']}")
    print(f"\nE-commerce: add_to_cart_count = {metrics['ecommerce']['add_to_cart_count']}")
