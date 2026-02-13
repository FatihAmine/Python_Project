"""E-Commerce Analytics Dashboard"""

import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="ShopVerse Analytics",
    page_icon="SV",
    layout="wide",
    initial_sidebar_state="expanded"
)


THEMES = {
    "Clean Light": {
        "main_bg": "#FAFAFA",
        "sidebar_bg": "#F7FAFC",
        "text_color": "#2D3748",
        "card_bg": "#FFFFFF",
        "card_border": "#E2E8F0",
        "metric_label": "#718096",
        "metric_value": "#4C51BF",
        "accent_color": "#4C51BF",
        "secondary_accent": "#48BB78",
        "plotly_template": "plotly_white"
    },
    "Midnight (Dark)": {
        "main_bg": "#0E1117",
        "sidebar_bg": "#161B22",
        "text_color": "#E5E7EB",
        "card_bg": "#1F2937",
        "card_border": "#374151",
        "metric_label": "#9CA3AF",
        "metric_value": "#818CF8",
        "accent_color": "#818CF8",
        "secondary_accent": "#34D399",
        "plotly_template": "plotly_dark"
    },
    "Ocean Blue": {
        "main_bg": "#0F172A",
        "sidebar_bg": "#1E293B",
        "text_color": "#F1F5F9",
        "card_bg": "#1E293B",
        "card_border": "#334155",
        "metric_label": "#94A3B8",
        "metric_value": "#38BDF8",
        "accent_color": "#38BDF8",
        "secondary_accent": "#2DD4BF",
        "plotly_template": "plotly_dark"
    }
}


if 'dashboard_theme' not in st.session_state:
    st.session_state.dashboard_theme = "Clean Light"

with st.sidebar:
    st.header("Appearance")
    selected_theme = st.selectbox(
        "Choose Theme",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.dashboard_theme)
    )
    st.session_state.dashboard_theme = selected_theme

current_theme = THEMES[selected_theme]


st.markdown(f"""
<style>

    .main, .stApp {{
        background-color: {current_theme['main_bg']};
    }}
    

    [data-testid="stSidebar"] {{
        background-color: {current_theme['sidebar_bg']};
        border-right: 1px solid {current_theme['card_border']};
    }}
    

    h1, h2, h3, h4, p, label, .stMarkdown, .stRadio label {{
        color: {current_theme['text_color']} !important;
        font-family: 'Segoe UI', sans-serif;
    }}
    

    [data-testid="stMetric"] {{
        background-color: {current_theme['card_bg']};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid {current_theme['card_border']};
    }}
    

    [data-testid="stMetricLabel"] p {{
        font-size: 1rem !important;
        color: {current_theme['metric_label']} !important;
        font-weight: 500;
    }}


    [data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        font-weight: 700;
        color: {current_theme['metric_value']} !important;
    }}
    

    .js-plotly-plot .plotly .modebar {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)


def get_data_path() -> Path:
    return Path(__file__).parent / 'output'

def get_ga_data_path() -> Path:
    return Path(__file__).parent / 'ga_output'


def load_summary() -> dict:
    path = get_data_path() / 'summary.json'
    if path.exists():
        with open(path, 'r') as f: return json.load(f)
    return {}

def load_ga_summary() -> dict:
    path = get_ga_data_path() / 'ga_summary.json'
    if path.exists():
        with open(path, 'r') as f: return json.load(f)
    return {}


def load_csv(filename: str, source='local') -> pd.DataFrame:
    base = get_data_path() if source == 'local' else get_ga_data_path()
    if source == 'ga':
        if filename == 'events_by_type.csv': filename = 'ga_events_by_type.csv'
        elif filename == 'events_over_time.csv': filename = 'ga_events_over_time.csv'
        elif filename == 'add_to_cart_by_product.csv': filename = 'ga_add_to_cart.csv'
    
    filepath = base / filename
    if filepath.exists():
        return pd.read_csv(filepath)
    return pd.DataFrame()


def render_metric_card(col, question, value, delta=None, help_text=None):
    col.metric(
        label=question,
        value=value,
        delta=delta,
        help=help_text
    )


def render_kpi_cards(summary: dict, ga_summary: dict = None, mode="local"):
    col1, col2, col3, col4 = st.columns(4)
    
    local_events = summary.get('total_events', 0)
    local_users = summary.get('unique_users', 0)
    local_cart = summary.get('add_to_cart_count', 0)
    local_visits = summary.get('total_page_visits', 0)
    
    if mode == "comparison" and ga_summary:
        ga_df = load_csv('events_by_type.csv', source='ga')
        ga_events = ga_df['count'].sum() if not ga_df.empty else 0
        ga_users = ga_summary.get('total_users', 0)
        ga_cart_df = load_csv('add_to_cart_by_product.csv', source='ga')
        ga_cart = ga_cart_df['add_to_cart_count'].sum() if not ga_cart_df.empty else 0
        

        render_metric_card(col1, "How many actions?", f"{local_events:,}", f"{local_events - ga_events:+d} vs Google", "Total clicks and views recorded by our server vs Google.")
        render_metric_card(col2, "How many people?", f"{local_users:,}", f"{local_users - ga_users:+d} vs Google", "Distinct visitors. Google often counts fewer due to ad blockers.")
        render_metric_card(col3, "Items added to cart?", f"{local_cart:,}", f"{local_cart - ga_cart:+d} vs Google", "Number of times a product was added to the basket.")
        render_metric_card(col4, "Pages viewed?", f"{local_visits:,}", None, "Total number of pages loaded by users.")
        
    elif mode == "ga":

        ga_df = load_csv('events_by_type.csv', source='ga')
        ga_events = ga_df['count'].sum() if not ga_df.empty else 0
        ga_users = ga_summary.get('total_users', 0)
        ga_cart_df = load_csv('add_to_cart_by_product.csv', source='ga')
        ga_cart = ga_cart_df['add_to_cart_count'].sum() if not ga_cart_df.empty else 0
        
        render_metric_card(col1, "Actions (Google)", f"{ga_events:,}")
        render_metric_card(col2, "People (Google)", f"{ga_users:,}")
        render_metric_card(col3, "Add to Cart (Google)", f"{ga_cart:,}")
        col4.info("Viewing Google Analytics Data")
        
    else:

        render_metric_card(col1, "How many actions?", f"{local_events:,}", None, "Total clicks and page views.")
        render_metric_card(col2, "How many people?", f"{local_users:,}", None, "Unique visitors tracked by our cookies.")
        render_metric_card(col3, "Items added to cart?", f"{local_cart:,}", None, "Purchase intent signals.")
        render_metric_card(col4, "Pages viewed?", f"{local_visits:,}", None, "Total page loads.")


def render_comparison_charts(local_type, ga_type, local_time, ga_time):
    st.subheader("Comparing the Numbers")
    st.markdown("Here's how our server logs (Local) compare to what Google sees.")
    
    if not local_type.empty: local_type['source'] = 'Local Server'
    if not ga_type.empty: ga_type['source'] = 'Google Analytics'
    
    if not ga_type.empty:
        ga_type['event_type'] = ga_type['event_type'].replace({
            'page_view': 'page_visit', 
            'view_item': 'view_details'
        })
    
    combined_type = pd.concat([local_type, ga_type], ignore_index=True)
    
    if not combined_type.empty:
        fig = px.bar(
            combined_type,
            x='event_type',
            y='count',
            color='source',
            barmode='group',
            title='Who captured more events?',
            color_discrete_map={'Local Server': current_theme['accent_color'], 'Google Analytics': current_theme['secondary_accent']},
            template=current_theme['plotly_template']
        )
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=current_theme['text_color']
        )
        st.plotly_chart(fig, use_container_width=True)


def render_standard_charts(df_time, df_products, funnel_data):
    st.markdown("### Traffic & Trends")
    

    if not df_time.empty:
        if 'datetime' in df_time.columns:
            df_time['datetime'] = pd.to_datetime(df_time['datetime'])
            
        fig = px.line(
            df_time, 
            x='datetime', 
            y='count', 
            title='When are people visiting?',
            template=current_theme['plotly_template']
        )
        fig.update_traces(line_color=current_theme['accent_color'], line_width=3)
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=current_theme['text_color'],
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
            
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Popular Products")
        if not df_products.empty:
            fig = px.bar(
                df_products.head(5), 
                y='product_id' if 'product_id' in df_products.columns else 'product_name', 
                x='add_to_cart_count', 
                orientation='h',
                title='Most added to cart',
                template=current_theme['plotly_template']
            )
            fig.update_traces(marker_color=current_theme['secondary_accent'])
            fig.update_layout(
                xaxis_title=None, 
                yaxis_title=None, 
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=current_theme['text_color']
            )
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.markdown("### Shopping Funnel")
        if funnel_data:
            stages = ['Home', 'View Product', 'Add to Cart', 'Checkout (Cart)']
            values = [
                funnel_data.get('home_visits', 0), 
                funnel_data.get('product_views', 0), 
                funnel_data.get('add_to_cart', 0), 
                funnel_data.get('cart_visits', 0)
            ]
            fig = go.Figure(go.Funnel(
                y=stages, 
                x=values, 
                textinfo="value+percent initial",
                marker={"color": [current_theme['accent_color'], current_theme['accent_color'], current_theme['secondary_accent'], current_theme['secondary_accent']]}
            ))
            fig.update_layout(
                title='Where do users drop off?',
                template=current_theme['plotly_template'],
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=current_theme['text_color']
            )
            st.plotly_chart(fig, use_container_width=True)


def load_ml_metrics():
    path = get_data_path() / 'ml_metrics.json'
    if path.exists():
        with open(path, 'r') as f: return json.load(f)
    return {}

def load_feature_importance():
    path = get_data_path() / 'feature_importance.csv'
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

def render_ml_dashboard():
    st.subheader("Machine Learning: Conversion Prediction")
    st.markdown("We trained a Random Forest model to predict if a user will visit the cart.")
    
    metrics = load_ml_metrics()
    if not metrics:
        st.warning("No ML model results found. Click 'Refresh Data' to train the model.")
        return

    # 1. Model Performance
    st.markdown("### Model Performance")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{metrics['accuracy']:.2%}", help="Percentage of correct predictions")
    m2.metric("Precision", f"{metrics['precision']:.2%}", help="Accuracy of positive predictions")
    m3.metric("Recall", f"{metrics['recall']:.2%}", help="Ability to find all positive instances")
    m4.metric("F1 Score", f"{metrics['f1_score']:.2%}", help="Harmonic mean of precision and recall")
    
    col1, col2 = st.columns([2, 1])
    
    # 2. Feature Importance
    with col1:
        st.markdown("### Creating Impact")
        st.caption("Which user behaviors drive conversion?")
        
        fi_df = load_feature_importance()
        if not fi_df.empty:
            fig = px.bar(
                fi_df,
                x='importance',
                y='feature',
                orientation='h',
                title='Feature Importance',
                template=current_theme['plotly_template']
            )
            fig.update_traces(marker_color=current_theme['accent_color'])
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=current_theme['text_color']
            )
            st.plotly_chart(fig, use_container_width=True)
            
  

def main():
    st.title("ShopVerse Analytics")
    st.caption("Understand your customers with simple, clear data.")
    st.markdown("---")
    

    st.sidebar.header("Controls")
    data_source = st.sidebar.radio(
        "Choose Data Source:",
        ("Local Logs", "Google Analytics", "Comparison View", "Predictions (ML)"),
        index=0
    )
    

    summary = load_summary()
    ga_summary = load_ga_summary()
    
    if not summary:
        st.info("Welcome! No data found yet. Browse the shop to generate events, then click Refresh.")
    

    if data_source == "Local Logs":
        render_kpi_cards(summary, mode="local")
        st.markdown("")
        render_standard_charts(
            load_csv('events_over_time.csv'),
            load_csv('add_to_cart_by_product.csv'),
            summary.get('funnel', {})
        )
        
    elif data_source == "Google Analytics":
        render_kpi_cards(summary, ga_summary, mode="ga")
    
        
    elif data_source == "Predictions (ML)":
        render_ml_dashboard()
        
    else:
        render_kpi_cards(summary, ga_summary, mode="comparison")
        render_comparison_charts(
            load_csv('events_by_type.csv'),
            load_csv('events_by_type.csv', source='ga'),
            load_csv('events_over_time.csv'),
            load_csv('events_over_time.csv', source='ga')
        )


    st.sidebar.markdown("---")
    if st.sidebar.button("Refresh Data"):
        with st.sidebar.status("Crunching new numbers..."):
            import subprocess
            subprocess.run(['python', 'generate_analytics.py'], cwd=str(Path(__file__).parent))
            st.write("Checked Local Logs")
            subprocess.run(['python', 'ga_fetcher.py'], cwd=str(Path(__file__).parent))
            st.write("Checked Google Analytics")
            subprocess.run(['python', 'ml_analysis.py'], cwd=str(Path(__file__).parent))
            st.write("Ran ML Models")
        st.rerun()

if __name__ == '__main__':
    main()
