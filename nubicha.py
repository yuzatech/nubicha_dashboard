import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import base64
from fpdf import FPDF
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="NubiCha Media Intelligence",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide duplicate header */
    .block-container .main .block-container h1:first-child {
        display: none;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    /* SIDEBAR ROMBAK TOTAL - NEW DESIGN */
    
    /* Sidebar container - Modern Glass Effect */
    .css-1d391kg, .css-1aumxhk, [data-testid="stSidebar"] {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        backdrop-filter: blur(20px) !important;
        border-right: none !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
    }
    
    /* Sidebar content wrapper */
    .css-1d391kg > div, .css-1aumxhk > div {
        padding: 1.5rem !important;
    }
    
    /* Reset all sidebar text to dark */
    .css-1d391kg *, .css-1aumxhk *, [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    
    /* Custom sidebar headers */
    .sidebar-header {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
        margin: -1.5rem -1.5rem 1.5rem -1.5rem !important;
        border-radius: 0 0 16px 16px !important;
        text-align: center !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .sidebar-section {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .sidebar-section:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        border-color: #3b82f6 !important;
    }
    
    .sidebar-section-title {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #e2e8f0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    
    /* Custom file uploader styling */
    .custom-file-upload {
        border: 2px dashed #3b82f6 !important;
        border-radius: 12px !important;
        padding: 2rem 1rem !important;
        text-align: center !important;
        background: linear-gradient(135deg, #f0f9ff, #dbeafe) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .custom-file-upload:hover {
        border-color: #1d4ed8 !important;
        background: linear-gradient(135deg, #dbeafe, #bfdbfe) !important;
    }
    
    /* Stats box styling */
    .sidebar-stats {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
    }
    
    .sidebar-stats * {
        color: white !important;
    }
    
    .stat-item {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 0.5rem 0 !important;
        border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    .stat-item:last-child {
        border-bottom: none !important;
    }
    
    .stat-label {
        font-size: 0.875rem !important;
        opacity: 0.9 !important;
    }
    
    .stat-value {
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    /* Filter controls styling */
    .css-1d391kg .stSelectbox, .css-1aumxhk .stSelectbox,
    .css-1d391kg .stMultiSelect, .css-1aumxhk .stMultiSelect,
    .css-1d391kg .stDateInput, .css-1aumxhk .stDateInput {
        margin-bottom: 1rem !important;
    }
    
    .css-1d391kg .stSelectbox > label, .css-1aumxhk .stSelectbox > label,
    .css-1d391kg .stMultiSelect > label, .css-1aumxhk .stMultiSelect > label,
    .css-1d391kg .stDateInput > label, .css-1aumxhk .stDateInput > label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input field styling */
    .css-1d391kg input, .css-1aumxhk input,
    .css-1d391kg .stSelectbox > div > div, .css-1aumxhk .stSelectbox > div > div,
    .css-1d391kg .stMultiSelect > div > div, .css-1aumxhk .stMultiSelect > div > div {
        background: white !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        transition: all 0.2s ease !important;
    }
    
    .css-1d391kg input:focus, .css-1aumxhk input:focus,
    .css-1d391kg .stSelectbox > div > div:hover, .css-1aumxhk .stSelectbox > div > div:hover,
    .css-1d391kg .stMultiSelect > div > div:hover, .css-1aumxhk .stMultiSelect > div > div:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Info and warning boxes */
    .css-1d391kg .stInfo, .css-1aumxhk .stInfo {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe) !important;
        border: 1px solid #0ea5e9 !important;
        border-radius: 8px !important;
        color: #0c4a6e !important;
        padding: 1rem !important;
    }
    
    .css-1d391kg .stInfo *, .css-1aumxhk .stInfo * {
        color: #0c4a6e !important;
    }
    
    /* Text selection fix */
    .css-1d391kg ::selection, .css-1aumxhk ::selection, [data-testid="stSidebar"] ::selection {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    .css-1d391kg ::-moz-selection, .css-1aumxhk ::-moz-selection, [data-testid="stSidebar"] ::-moz-selection {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* Sidebar dividers */
    .sidebar-divider {
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        margin: 1.5rem 0;
        border-radius: 1px;
    }
    
    /* Sidebar icon styling */
    .sidebar-icon {
        display: inline-block;
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3b82f6;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        border-radius: 16px 16px 0 0;
    }
    
    .kpi-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'Inter', sans-serif;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    .kpi-delta {
        font-size: 0.875rem;
        font-weight: 500;
        color: #059669;
        background: #d1fae5;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        display: inline-block;
        font-family: 'Inter', sans-serif;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-left: 6px solid #3b82f6;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
        color: #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .section-header {
        font-size: 1.875rem;
        font-weight: 600;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        font-family: 'Inter', sans-serif;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-header::before {
        content: '';
        width: 4px;
        height: 2rem;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 2px;
    }
    
    .chart-container {
        background: white;
        border: 2px solid #f1f5f9;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    .status-success {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 2px solid #10b981;
        color: #047857;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    .status-info {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid #64748b;
        color: #475569;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .fresh-button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .fresh-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0, #3b82f6, #e2e8f0);
        margin: 3rem 0;
        border-radius: 1px;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("OPENROUTER_API_KEY", "demo-mode")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

# Main header - only once
st.markdown('<h1 class="main-header">🧋 NubiCha Media Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Dashboard Analisis Media Sosial Professional</p>', unsafe_allow_html=True)

# Enhanced Sidebar with New Design
with st.sidebar:
    # Custom Header
    st.markdown("""
    <div class="sidebar-header">
        🧋 Dashboard Control Center
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-section-title">
            📁 Data Upload
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type="csv",
        help="Upload your social media data (Max: 200MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is None:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0f9ff, #dbeafe); border: 1px solid #3b82f6; padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
        <strong style='color: #1e40af;'>📋 Required Format:</strong><br>
        <span style='color: #1e40af;'>• Date, Platform, Sentiment</span><br>
        <span style='color: #1e40af;'>• Location, Engagements, Media_Type</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 Please upload a CSV file to start analysis")
        st.stop()
    
    st.markdown("</div>", unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data(uploaded_file)
    
    required_columns = ['Date', 'Platform', 'Sentiment', 'Location', 'Engagements', 'Media_Type']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_columns)}")
        st.info("Pastikan file CSV memiliki kolom: Date, Platform, Sentiment, Location, Engagements, Media_Type")
        st.stop()
    
    # Success message
    st.markdown('<div class="status-success">✅ Data berhasil dimuat: {:,} baris data siap dianalisis</div>'.format(len(df)), unsafe_allow_html=True)
    
    # Enhanced Sidebar Filters with New Design
    with st.sidebar:
        # Filter Section
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                🎛️ Data Filters
            </div>
        """, unsafe_allow_html=True)
        
        date_range = st.date_input(
            "📅 Date Range",
            value=(df['Date'].min(), df['Date'].max()),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
        
        platforms = st.multiselect(
            "🌐 Platforms",
            options=sorted(df['Platform'].unique()),
            default=sorted(df['Platform'].unique())
        )
        
        sentiments = st.multiselect(
            "😊 Sentiment",
            options=sorted(df['Sentiment'].unique()),
            default=sorted(df['Sentiment'].unique())
        )
        
        locations = st.multiselect(
            "📍 Locations",
            options=sorted(df['Location'].unique()),
            default=sorted(df['Location'].unique())
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Stats Section
        st.markdown(f"""
        <div class="sidebar-stats">
            <div style='text-align: center; margin-bottom: 1rem; font-weight: 600; font-size: 1rem;'>
                📊 Dataset Overview
            </div>
            <div class="stat-item">
                <span class="stat-label">📈 Total Records</span>
                <span class="stat-value">{len(df):,}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">🌐 Platforms</span>
                <span class="stat-value">{len(df['Platform'].unique())}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">🌍 Locations</span>
                <span class="stat-value">{len(df['Location'].unique())}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">📅 Time Span</span>
                <span class="stat-value">{(df['Date'].max() - df['Date'].min()).days} days</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter data
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[
            (df['Date'] >= pd.to_datetime(start_date)) &
            (df['Date'] <= pd.to_datetime(end_date)) &
            (df['Platform'].isin(platforms)) &
            (df['Sentiment'].isin(sentiments)) &
            (df['Location'].isin(locations))
        ]
    else:
        df_filtered = df[
            (df['Platform'].isin(platforms)) &
            (df['Sentiment'].isin(sentiments)) &
            (df['Location'].isin(locations))
        ]
    
    if df_filtered.empty:
        st.warning("❌ Tidak ada data yang sesuai dengan filter yang dipilih")
        st.stop()
    
    # Calculate metrics
    total_posts = len(df_filtered)
    total_engagement = df_filtered['Engagements'].sum()
    avg_engagement = df_filtered['Engagements'].mean()
    positive_sentiment = (df_filtered['Sentiment'] == 'Positive').sum()
    top_platform = df_filtered.groupby('Platform')['Engagements'].sum().idxmax()
    
    # Dashboard Overview
    st.markdown('<div class="section-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-grid">
        <div class="kpi-card">
            <div class="kpi-title">Total Postingan</div>
            <div class="kpi-value">{:,}</div>
            <div class="kpi-delta">{:.1f}% dari dataset</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Engagement</div>
            <div class="kpi-value">{:,}</div>
            <div class="kpi-delta">{:.1f}K interaksi</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Rata-rata Engagement</div>
            <div class="kpi-value">{:,.0f}</div>
            <div class="kpi-delta">per postingan</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Sentimen Positif</div>
            <div class="kpi-value">{}</div>
            <div class="kpi-delta">{:.1f}% positive vibes</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Platform Terbaik</div>
            <div class="kpi-value">{}</div>
            <div class="kpi-delta">engagement tertinggi</div>
        </div>
    </div>
    """.format(
        total_posts,
        (total_posts/len(df)*100),
        total_engagement,
        (total_engagement/1000),
        avg_engagement,
        positive_sentiment,
        (positive_sentiment/total_posts*100),
        top_platform
    ), unsafe_allow_html=True)
    
    # Visual Analysis
    st.markdown('<div class="section-header">📈 Analisis Visual</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        sentiment_data = df_filtered['Sentiment'].value_counts()
        colors = ['#3b82f6', '#8b5cf6', '#ef4444']
        
        fig_sentiment = go.Figure(data=[go.Pie(
            labels=sentiment_data.index,
            values=sentiment_data.values,
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=13,
            marker=dict(line=dict(color='#ffffff', width=3))
        )])
        
        fig_sentiment.update_layout(
            title="Distribusi Sentimen",
            showlegend=True,
            height=400,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=18, color='#1e293b', family="Inter"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_sentiment, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        dominant_sentiment = sentiment_data.index[0]
        st.markdown(f'<div class="status-info">💡 <strong>Insight:</strong> Sentimen {dominant_sentiment} mendominasi dengan {sentiment_data.iloc[0]} postingan ({(sentiment_data.iloc[0]/len(df_filtered)*100):.1f}%)</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        platform_engagement = df_filtered.groupby('Platform')['Engagements'].sum().sort_values(ascending=True)
        
        fig_platform = go.Figure(data=[go.Bar(
            y=platform_engagement.index,
            x=platform_engagement.values,
            orientation='h',
            marker=dict(
                color=platform_engagement.values,
                colorscale='Viridis',
                line=dict(color='rgba(255,255,255,0.8)', width=1)
            ),
            text=[f'{val:,}' for val in platform_engagement.values],
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        )])
        
        fig_platform.update_layout(
            title="Performa Platform",
            xaxis_title="Total Engagement",
            yaxis_title="Platform",
            height=400,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=18, color='#1e293b', family="Inter"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#f1f5f9'),
            yaxis=dict(gridcolor='#f1f5f9')
        )
        
        st.plotly_chart(fig_platform, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        winner_engagement = platform_engagement.iloc[-1]
        improvement = ((winner_engagement - platform_engagement.iloc[0]) / platform_engagement.iloc[0] * 100)
        st.markdown(f'<div class="status-info">🏆 <strong>Insight:</strong> {top_platform} unggul {improvement:.0f}% dari platform terendah dengan {winner_engagement:,} total engagement</div>', unsafe_allow_html=True)
    
    # Timeline and Media Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        daily_engagement = df_filtered.groupby('Date')['Engagements'].sum().reset_index()
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=daily_engagement['Date'],
            y=daily_engagement['Engagements'],
            mode='lines+markers',
            line=dict(color='#3b82f6', width=2),
            marker=dict(size=6, color='#3b82f6'),
            name='Daily Engagement'
        ))
        
        fig_timeline.update_layout(
            title="Timeline Engagement",
            xaxis_title="Tanggal",
            yaxis_title="Engagement",
            height=400,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=16, color='#1f2937'),
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=False
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        if not daily_engagement.empty:
            peak_day = daily_engagement.loc[daily_engagement['Engagements'].idxmax()]
            st.markdown(f'<div class="status-info">📅 Hari terbaik: <strong>{peak_day["Date"].strftime("%d %B %Y")}</strong> ({peak_day["Engagements"]:,} engagement)</div>', unsafe_allow_html=True)
    
    with col2:
        media_performance = df_filtered.groupby('Media_Type')['Engagements'].agg(['sum', 'mean']).reset_index()
        
        fig_media = go.Figure()
        fig_media.add_trace(go.Bar(
            name='Total Engagement',
            x=media_performance['Media_Type'],
            y=media_performance['sum'],
            marker_color='#3b82f6',
            yaxis='y'
        ))
        
        fig_media.add_trace(go.Scatter(
            name='Rata-rata Engagement',
            x=media_performance['Media_Type'],
            y=media_performance['mean'],
            mode='lines+markers',
            line=dict(color='#6b7280', width=2),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig_media.update_layout(
            title="Analisis Tipe Media",
            xaxis_title="Tipe Media",
            yaxis=dict(title="Total Engagement", side="left"),
            yaxis2=dict(title="Rata-rata Engagement", side="right", overlaying="y"),
            height=400,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=16, color='#1f2937'),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_media, use_container_width=True)
        
        best_media = media_performance.loc[media_performance['mean'].idxmax(), 'Media_Type']
        st.markdown(f'<div class="status-info">🎯 Tipe media terbaik: <strong>{best_media}</strong></div>', unsafe_allow_html=True)
    
    # Geographic Analysis
    st.markdown("### 🗺️ Analisis Geografis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        location_stats = df_filtered.groupby('Location').agg({
            'Engagements': ['sum', 'count', 'mean']
        }).round(0)
        location_stats.columns = ['Total_Engagement', 'Post_Count', 'Avg_Engagement']
        location_stats = location_stats.sort_values('Total_Engagement', ascending=False).head(10)
        
        fig_location = go.Figure(data=[go.Bar(
            x=location_stats.index,
            y=location_stats['Total_Engagement'],
            marker_color='#3b82f6',
            text=[f'{val:,.0f}' for val in location_stats['Total_Engagement']],
            textposition='auto'
        )])
        
        fig_location.update_layout(
            title="Top 10 Kota dengan Engagement Tertinggi",
            xaxis_title="Kota",
            yaxis_title="Total Engagement",
            height=400,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=16, color='#1f2937'),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_location, use_container_width=True)
    
    with col2:
        sentiment_platform = df_filtered.groupby(['Platform', 'Sentiment']).size().unstack(fill_value=0)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=sentiment_platform.values,
            x=sentiment_platform.columns,
            y=sentiment_platform.index,
            colorscale='Blues',
            text=sentiment_platform.values,
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        
        fig_heatmap.update_layout(
            title="Peta Panas Sentimen per Platform",
            xaxis_title="Sentimen",
            yaxis_title="Platform",
            height=400,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=16, color='#1f2937'),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # AI Analysis Section
    st.markdown("### 🤖 Analisis AI")
    
    def generate_ai_insight(data):
        summary_stats = {
            'total_posts': len(data),
            'total_engagement': data['Engagements'].sum(),
            'avg_engagement': data['Engagements'].mean(),
            'top_platform': data.groupby('Platform')['Engagements'].sum().idxmax(),
            'top_sentiment': data['Sentiment'].mode().iloc[0],
            'top_location': data.groupby('Location')['Engagements'].sum().idxmax(),
            'best_media_type': data.groupby('Media_Type')['Engagements'].mean().idxmax(),
            'platform_breakdown': data['Platform'].value_counts().to_dict(),
            'sentiment_breakdown': data['Sentiment'].value_counts().to_dict()
        }
        
        if API_KEY == "demo-mode":
            return f"""
**🔍 Insight Utama:**

1. **Platform Performance:** {summary_stats['top_platform']} menunjukkan performa terbaik dengan total {summary_stats['total_engagement']:,} engagement.

2. **Sentiment Analysis:** Sentimen {summary_stats['top_sentiment']} mendominasi dengan distribusi yang menunjukkan respons audiens yang baik.

3. **Geographic Insights:** {summary_stats['top_location']} menjadi lokasi dengan engagement tertinggi, menunjukkan potensi pasar yang kuat.

**💡 Rekomendasi:**

• Fokuskan strategi konten pada platform {summary_stats['top_platform']}
• Optimalisasi tipe konten {summary_stats['best_media_type']} yang menunjukkan engagement rate terbaik
• Pertimbangkan ekspansi geografis berdasarkan performa {summary_stats['top_location']}

**📊 Metrik Kinerja:**
- Rata-rata engagement: {summary_stats['avg_engagement']:,.0f} per postingan
- Total reach: {summary_stats['total_posts']:,} postingan
"""
        
        prompt = f"""
        Analisis data media sosial NubiCha dengan statistik berikut:
        
        Total postingan: {summary_stats['total_posts']:,}
        Total engagement: {summary_stats['total_engagement']:,}
        Rata-rata engagement: {summary_stats['avg_engagement']:,.0f}
        Platform terbaik: {summary_stats['top_platform']}
        Sentimen dominan: {summary_stats['top_sentiment']}
        Lokasi terbaik: {summary_stats['top_location']}
        Tipe media terbaik: {summary_stats['best_media_type']}
        
        Breakdown platform: {summary_stats['platform_breakdown']}
        Breakdown sentimen: {summary_stats['sentiment_breakdown']}
        
        Berikan analisis professional dengan:
        1. Tiga insight utama yang paling signifikan
        2. Rekomendasi strategis yang actionable
        3. Analisis performa dan peluang optimasi
        
        Gunakan format yang formal dan professional.
        """
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "NubiCha Dashboard"
        }
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Anda adalah analis media sosial professional yang memberikan insights berbasis data dengan gaya formal dan actionable."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except:
            return f"""
**📈 Analisis Performance Media Sosial:**

**Key Insights:**
• Platform {summary_stats['top_platform']} menghasilkan engagement terbaik
• Sentimen {summary_stats['top_sentiment']} mendominasi respons audiens  
• Lokasi {summary_stats['top_location']} menunjukkan penetrasi pasar tertinggi

**Strategic Recommendations:**
• Alokasikan budget lebih besar untuk {summary_stats['top_platform']}
• Tingkatkan produksi konten {summary_stats['best_media_type']}
• Fokus targeting geografis di {summary_stats['top_location']}

**Performance Metrics:**
• Engagement rate: {summary_stats['avg_engagement']:,.0f} per post
• Total reach: {summary_stats['total_posts']:,} publikasi
"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 Generate Analisis AI", type="primary", use_container_width=True):
            with st.spinner("🔄 Menganalisis data..."):
                insight = generate_ai_insight(df_filtered)
                st.session_state.ai_insight = insight
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            if "ai_insight" in st.session_state:
                del st.session_state.ai_insight
            st.rerun()
    
    if "ai_insight" in st.session_state and st.session_state.ai_insight:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("#### 🤖 Hasil Analisis AI")
        st.markdown(st.session_state.ai_insight)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            insight_text = st.session_state.ai_insight
            b64 = base64.b64encode(insight_text.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="nubicha_insights.txt"><button style="background: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">📄 Download Insights (TXT)</button></a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            if st.button("📊 Generate Laporan PDF", use_container_width=True):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=16)
                    pdf.cell(200, 10, txt="NubiCha Media Intelligence Report", ln=True, align='C')
                    pdf.ln(10)
                    
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.cell(200, 10, txt="Executive Summary", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(200, 8, txt=f"Total Posts: {total_posts:,}", ln=True)
                    pdf.cell(200, 8, txt=f"Total Engagement: {total_engagement:,}", ln=True)
                    pdf.cell(200, 8, txt=f"Average Engagement: {avg_engagement:,.0f}", ln=True)
                    pdf.cell(200, 8, txt=f"Top Platform: {top_platform}", ln=True)
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.cell(200, 10, txt="AI Analysis", ln=True)
                    pdf.set_font("Arial", size=10)
                    
                    clean_insight = st.session_state.ai_insight.replace("**", "").replace("•", "-")
                    lines = clean_insight.split('\n')
                    for line in lines[:25]:
                        if line.strip():
                            pdf.multi_cell(0, 6, line.strip())
                    
                    pdf_bytes = pdf.output(dest='S').encode('latin-1')
                    
                    st.download_button(
                        label="📑 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"nubicha_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
    
    # Q&A Section
    st.markdown("### 💬 Tanya AI")
    user_question = st.text_input(
        "🤔 Ajukan pertanyaan tentang data Anda:",
        placeholder="Contoh: 'Platform mana yang memberikan ROI terbaik?'"
    )
    
    if user_question:
        with st.spinner("🔄 Memproses pertanyaan..."):
            context = f"""
            Data context: {len(df_filtered)} posts, {df_filtered['Engagements'].sum():,} total engagement.
            Platforms: {', '.join(df_filtered['Platform'].unique())}
            Locations: {', '.join(df_filtered['Location'].unique())}
            Date range: {df_filtered['Date'].min()} to {df_filtered['Date'].max()}
            """
            
            if API_KEY == "demo-mode":
                demo_answers = {
                    "roi": f"Berdasarkan data, {top_platform} memberikan ROI terbaik dengan engagement rate tertinggi.",
                    "platform": f"{top_platform} adalah platform dengan performa terbaik ({df_filtered.groupby('Platform')['Engagements'].sum().max():,} engagement).",
                    "engagement": f"Rata-rata engagement Anda adalah {avg_engagement:,.0f} per postingan, yang menunjukkan performa yang solid.",
                    "sentiment": f"Sentimen {df_filtered['Sentiment'].mode().iloc[0]} mendominasi dengan {df_filtered['Sentiment'].value_counts().iloc[0]} postingan."
                }
                
                answer = "**💡 Jawaban:**\n\n"
                if any(word in user_question.lower() for word in ["roi", "return"]):
                    answer += demo_answers["roi"]
                elif any(word in user_question.lower() for word in ["platform"]):
                    answer += demo_answers["platform"]
                elif any(word in user_question.lower() for word in ["engagement"]):
                    answer += demo_answers["engagement"]
                elif any(word in user_question.lower() for word in ["sentiment"]):
                    answer += demo_answers["sentiment"]
                else:
                    answer += f"Berdasarkan analisis data, fokuskan strategi pada {top_platform} dan tingkatkan produksi konten {df_filtered.groupby('Media_Type')['Engagements'].mean().idxmax()} untuk optimalisasi performa."
                
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(f"**❓ Pertanyaan:** {user_question}")
                st.markdown(answer)
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                qa_prompt = f"{context}\n\nPertanyaan: {user_question}\n\nBerikan jawaban yang spesifik dan berdasarkan data dengan format professional."
                
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "NubiCha Dashboard"
                }
                
                payload = {
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": "Anda adalah analis media sosial expert. Jawab pertanyaan berdasarkan konteks data dengan gaya professional."},
                        {"role": "user", "content": qa_prompt}
                    ]
                }
                
                try:
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                    response.raise_for_status()
                    answer = response.json()["choices"][0]["message"]["content"].strip()
                    
                    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                    st.markdown(f"**❓ Pertanyaan:** {user_question}")
                    st.markdown(f"**💡 Jawaban:** {answer}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Export Section
    st.markdown("### 📊 Export & Download")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📊 Download Data CSV",
            data=csv,
            file_name=f"nubicha_filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("📋 Generate Summary", use_container_width=True):
            summary = f"""NubiCha Media Intelligence Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
=================
Total Posts: {total_posts:,}
Total Engagement: {total_engagement:,}
Average Engagement: {avg_engagement:,.0f}
Top Platform: {top_platform}
Positive Sentiment: {positive_sentiment}

PLATFORM BREAKDOWN
==================
{df_filtered.groupby('Platform')['Engagements'].sum().to_string()}

SENTIMENT ANALYSIS
==================
{df_filtered['Sentiment'].value_counts().to_string()}

TOP LOCATIONS
=============
{df_filtered.groupby('Location')['Engagements'].sum().sort_values(ascending=False).head().to_string()}

MEDIA TYPE PERFORMANCE
======================
{df_filtered.groupby('Media_Type')['Engagements'].agg(['sum', 'mean']).round(0).to_string()}

KEY INSIGHTS
============
- Best performing platform: {top_platform}
- Most effective content type: {df_filtered.groupby('Media_Type')['Engagements'].mean().idxmax()}
- Highest engagement location: {df_filtered.groupby('Location')['Engagements'].sum().idxmax()}
- Average engagement rate: {(total_engagement/total_posts):,.0f} per post

Generated by NubiCha Media Intelligence Dashboard
"""
            
            st.download_button(
                label="📄 Download Summary",
                data=summary,
                file_name=f"nubicha_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col3:
        if st.button("👁️ Preview Data", use_container_width=True):
            st.session_state.show_data = not st.session_state.get('show_data', False)
    
    if st.session_state.get('show_data', False):
        st.markdown("#### 👀 Preview Data")
        st.dataframe(
            df_filtered.sort_values('Engagements', ascending=False).head(20),
            use_container_width=True,
            height=300
        )
        st.markdown(f'<div class="status-info">📊 Menampilkan 20 dari {len(df_filtered):,} data. Download CSV untuk data lengkap.</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.markdown("""
    **🔧 Troubleshooting:**
    
    • Pastikan file CSV memiliki kolom: Date, Platform, Sentiment, Location, Engagements, Media_Type
    • Periksa format tanggal (YYYY-MM-DD atau DD/MM/YYYY)
    • Pastikan encoding file adalah UTF-8
    • Ukuran file maksimal 200MB
    """)

# Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border: 2px solid #3b82f6; padding: 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;'>
    <h3 style='color: #1f2937; margin-bottom: 1rem; font-family: Inter, sans-serif;'>🧋 NubiCha Media Intelligence Dashboard</h3>
    <p style='color: #6b7280; margin-bottom: 1rem; font-family: Inter, sans-serif;'>
        Professional Social Media Analytics Platform
    </p>
    <div style='display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;'>
        <span style='background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; font-family: Inter, sans-serif;'>
            🚀 Advanced Analytics
        </span>
        <span style='background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; font-family: Inter, sans-serif;'>
            🤖 AI-Powered Insights
        </span>
        <span style='background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; font-family: Inter, sans-serif;'>
            ⚡ Real-time Processing
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
