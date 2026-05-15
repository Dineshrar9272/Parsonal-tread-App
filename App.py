import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

# Page Layout (Wide mode for Desktop & Mobile)
st.set_page_config(page_title="Crypto Pro Dashboard", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; border: 1px solid #ddd; background-color: white; font-weight: bold; }
    .stMetric { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("💹 Crypto Intelligence Dashboard")
st.write("Live Top 5 Coins - Delta Exchange Style")

# Top 5 Coins
top_coins = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"]

# Selection state maintain karne ke liye
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = "BTC-USD"

# Section 1: Top Watchlist (Horizontal Cards)
cols = st.columns(5)
for i, ticker in enumerate(top_coins):
    with cols[i]:
        try:
            # Chota data fetch signals ke liye
            data = yf.download(ticker, period="5d", interval="1h", auto_adjust=True, progress=False)
            if not data.empty:
                # Error Fix: Always use the first column if data is multidimensional
                latest_price = float(data['Close'].iloc[-1].iloc[0] if isinstance(data['Close'].iloc[-1], pd.Series) else data['Close'].iloc[-1])
                prev_price = float(data['Close'].iloc[-2].iloc[0] if isinstance(data['Close'].iloc[-2], pd.Series) else data['Close'].iloc[-2])
                pct_change = ((latest_price - prev_price) / prev_price) * 100
                
                # Button to select coin
                if st.button(f"{ticker.replace('-USD', '')}"):
                    st.session_state.selected_ticker = ticker
                
                st.metric(label="", value=f"${latest_price:,.2f}", delta=f"{pct_change:+.2f}%")
        except:
            st.error("Data Error")

st.divider()

# Section 2: Interactive Candlestick Chart
selected = st.session_state.selected_ticker
st.subheader(f"🕯️ {selected} Real-Time Candle Chart")

# Sidebar for timeframe control
timeframe = st.sidebar.selectbox("Select Chart Timeframe", ["1d", "1h", "15m", "5m"], index=1)

try:
    # Detailed Data download
    detail_data = yf.download(selected, period="60d", interval=timeframe, auto_adjust=True)
    
    if not detail_data.empty:
        # Error Fix: Ensuring 1D Series for Indicators
        close_series = detail_data['Close'].iloc[:, 0] if len(detail_data['Close'].shape) > 1 else detail_data['Close']
        
        # Indicators
        detail_data['MA20'] = ta.trend.sma_indicator(close_series, window=20)
        rsi_
        
