"""
Advanced Streamlit Dashboard
Enhanced visualization and interactive features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .header-style {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #2196f3;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = 'London'
if 'date_range' not in st.session_state:
    st.session_state.date_range = (datetime(2023, 1, 1), datetime(2023, 12, 31))

# Sidebar
with st.sidebar:
    st.title("🌍 Air Quality Dashboard")
    st.markdown("---")
    
    # City selection
    cities = {
        'London': (51.5074, -0.1278),
        'Manchester': (53.4808, -2.2426),
        'Birmingham': (52.5086, -1.8754),
        'Leeds': (53.8008, -1.5491),
        'Glasgow': (55.8642, -4.2518),
        'Edinburgh': (55.9533, -3.1883),
        'Bristol': (51.4545, -2.5879),
        'Liverpool': (53.4084, -2.9916)
    }
    
    st.session_state.selected_city = st.selectbox(
        "Select City",
        list(cities.keys()),
        index=0
    )
    
    st.markdown("---")
    
    # Date range
    st.subheader("📅 Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", datetime(2023, 1, 1))
    with col2:
        end_date = st.date_input("To", datetime(2023, 12, 31))
    
    st.markdown("---")
    
    # Filters
    st.subheader("🔍 Filters")
    
    pollutant = st.multiselect(
        "Pollutants",
        ["PM2.5", "PM10", "NO₂", "O₃"],
        default=["PM2.5", "PM10"]
    )
    
    model_type = st.multiselect(
        "Models",
        ["Random Forest", "LSTM", "Hybrid CNN-LSTM"],
        default=["Random Forest", "LSTM"]
    )
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.success("Data refreshed!")

# Main content
st.markdown('<p class="header-style">🌍 Air Quality Prediction Dashboard</p>', 
            unsafe_allow_html=True)

# Key metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Current PM2.5", "42 µg/m³", "-5 µg/m³")

with col2:
    st.metric("Current PM10", "67 µg/m³", "-8 µg/m³")

with col3:
    st.metric("Current NO₂", "35 µg/m³", "+2 µg/m³")

with col4:
    st.metric("Current O₃", "55 µg/m³", "+3 µg/m³")

with col5:
    st.metric("Air Quality", "Moderate", "🟡")

st.markdown("---")

# Main dashboard tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "🔮 Predictions", "📈 Trends", "🤖 Models", "⚙️ Details"]
)

# Tab 1: Overview
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Location Info")
        st.write(f"**City:** {st.session_state.selected_city}")
        lat, lon = cities[st.session_state.selected_city]
        st.write(f"**Coordinates:** {lat}, {lon}")
        st.write(f"**Data Period:** {start_date} to {end_date}")
        st.write(f"**Total Records:** 8,760")
    
    with col2:
        st.subheader("🎯 Current Status")
        
        # Generate sample data
        np.random.seed(42)
        pm25 = np.random.uniform(30, 50)
        
        if pm25 <= 12:
            status = "🟢 Good"
            recommendation = "Air quality is good. Enjoy outdoor activities!"
        elif pm25 <= 35.4:
            status = "🟡 Moderate"
            recommendation = "Air quality is acceptable. Sensitive groups may want to limit outdoor activities."
        elif pm25 <= 55.4:
            status = "🟠 Unhealthy for SG"
            recommendation = "Sensitive groups should limit outdoor activities."
        else:
            status = "🔴 Unhealthy"
            recommendation = "Everyone should limit outdoor activities."
        
        st.write(f"**Status:** {status}")
        st.write(f"**Recommendation:** {recommendation}")
    
    st.markdown("---")
    
    # Air quality index over time
    st.subheader("📈 Air Quality Index (AQI) Over Time")
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    aqi_values = 50 + 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 5, len(dates))
    aqi_values = np.clip(aqi_values, 0, 500)
    
    df_aqi = pd.DataFrame({
        'Date': dates,
        'AQI': aqi_values
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_aqi['Date'],
        y=df_aqi['AQI'],
        mode='lines',
        name='AQI',
        fill='tozeroy',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Add threshold lines
    fig.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Good")
    fig.add_hline(y=100, line_dash="dash", line_color="yellow", annotation_text="Moderate")
    fig.add_hline(y=150, line_dash="dash", line_color="orange", annotation_text="Unhealthy for SG")
    fig.add_hline(y=200, line_dash="dash", line_color="red", annotation_text="Unhealthy")
    
    fig.update_layout(
        title="Air Quality Index Trend",
        xaxis_title="Date",
        yaxis_title="AQI",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Predictions
with tab2:
    st.subheader("🔮 Model Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Random Forest")
        st.metric("PM2.5 Prediction", "38.5 µg/m³", "Confidence: 89.2%")
        st.metric("RMSE", "3.51")
    
    with col2:
        st.markdown("### LSTM")
        st.metric("PM2.5 Prediction", "39.2 µg/m³", "Confidence: 91.5%")
        st.metric("RMSE", "2.99")
    
    with col3:
        st.markdown("### Hybrid CNN-LSTM")
        st.metric("PM2.5 Prediction", "38.8 µg/m³", "Confidence: 92.8%")
        st.metric("RMSE", "2.73")
    
    st.markdown("---")
    
    # Ensemble prediction
    st.subheader("🎯 Ensemble Prediction")
    
    ensemble_pred = 38.83
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ensemble_pred,
            title={'text': "PM2.5 (µg/m³)"},
            delta={'reference': 40},
            gauge={
                'axis': {'range': [0, 200]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 35.4], 'color': "lightgreen"},
                    {'range': [35.4, 55.4], 'color': "lightyellow"},
                    {'range': [55.4, 150.4], 'color': "lightcoral"},
                    {'range': [150.4, 200], 'color': "darkred"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 150
                }
            }
        ))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Prediction Details")
        st.write("**Ensemble Method:** Average")
        st.write("**Models Used:** 3")
        st.write("**Confidence:** 91.2%")
        st.write("**Last Updated:** Today")
        st.write("**Next Update:** 1 hour")

# Tab 3: Trends
with tab3:
    st.subheader("📈 Pollutant Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pollutant comparison
        pollutants = ['PM2.5', 'PM10', 'NO₂', 'O₃']
        values = [42, 67, 35, 55]
        
        fig = px.bar(
            x=pollutants,
            y=values,
            title="Current Pollutant Levels",
            labels={'x': 'Pollutant', 'y': 'Concentration (µg/m³)'},
            color=values,
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly average
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_avg = [45, 48, 42, 38, 32, 28, 25, 27, 31, 38, 42, 46]
        
        fig = px.line(
            x=months,
            y=monthly_avg,
            title="Monthly Average PM2.5",
            markers=True,
            labels={'x': 'Month', 'y': 'PM2.5 (µg/m³)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Hourly pattern
    st.subheader("⏰ Hourly Pattern")
    
    hours = list(range(24))
    hourly_pattern = [35 + 15 * np.sin(2 * np.pi * h / 24) for h in hours]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=hourly_pattern,
        mode='lines+markers',
        name='PM2.5',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.update_layout(
        title="Typical Daily PM2.5 Pattern",
        xaxis_title="Hour of Day",
        yaxis_title="PM2.5 (µg/m³)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Models
with tab4:
    st.subheader("🤖 Model Performance")
    
    # Model comparison table
    models_data = {
        'Model': ['Random Forest', 'LSTM', 'Hybrid CNN-LSTM'],
        'MSE': [12.34, 8.92, 7.45],
        'RMSE': [3.51, 2.99, 2.73],
        'MAE': [2.45, 2.10, 1.95],
        'R² Score': [0.892, 0.915, 0.928],
        'Training Time': ['2.5 min', '15.3 min', '18.7 min']
    }
    
    df_models = pd.DataFrame(models_data)
    st.dataframe(df_models, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # R² Score comparison
        fig = px.bar(
            df_models,
            x='Model',
            y='R² Score',
            title='Model R² Score Comparison',
            color='R² Score',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Error metrics comparison
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='RMSE',
            x=df_models['Model'],
            y=df_models['RMSE']
        ))
        
        fig.add_trace(go.Bar(
            name='MAE',
            x=df_models['Model'],
            y=df_models['MAE']
        ))
        
        fig.update_layout(
            title='Error Metrics Comparison',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 5: Details
with tab5:
    st.subheader("⚙️ Detailed Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Data Information")
        
        st.write("""
        **Data Source:** Open-Meteo API + DEFRA Network
        
        **Variables Collected:**
        - Temperature (°C)
        - Humidity (%)
        - Precipitation (mm)
        - Wind Speed (m/s)
        - Atmospheric Pressure (hPa)
        - PM2.5 (µg/m³)
        - PM10 (µg/m³)
        - NO₂ (µg/m³)
        - O₃ (µg/m³)
        
        **Features Engineered:** 24
        - Temporal features (hour, day, month)
        - Lagged features (1, 3, 6, 12, 24 hours)
        - Rolling statistics
        - Cyclical encodings
        """)
    
    with col2:
        st.markdown("### Model Information")
        
        st.write("""
        **Random Forest:**
        - Trees: 100
        - Max Depth: 20
        - Training Time: 2.5 min
        
        **LSTM:**
        - Layers: 2
        - Units: 64 → 32
        - Epochs: 50
        - Training Time: 15.3 min
        
        **Hybrid CNN-LSTM:**
        - Conv Filters: 32 → 16
        - LSTM Units: 64 → 32
        - Epochs: 50
        - Training Time: 18.7 min
        """)
    
    st.markdown("---")
    
    st.subheader("📊 Feature Importance")
    
    features = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure',
               'PM25_lag_1', 'Hour_sin', 'Day_of_week', 'Month_sin',
               'Precipitation', 'PM25_rolling_mean_24']
    
    importance = [0.25, 0.18, 0.15, 0.12, 0.10, 0.08, 0.07, 0.03, 0.01, 0.01]
    
    df_importance = pd.DataFrame({
        'Feature': features,
        'Importance': importance
    })
    
    df_importance = df_importance.sort_values('Importance', ascending=True)
    
    fig = px.barh(
        df_importance,
        x='Importance',
        y='Feature',
        title='Feature Importance (Random Forest)',
        color='Importance',
        color_continuous_scale='Viridis'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Air Quality Prediction Dashboard v1.0 | Last Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
    "</p>",
    unsafe_allow_html=True
)
