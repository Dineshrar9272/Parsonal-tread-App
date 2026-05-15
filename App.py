import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

# Page Layout
st.set_page_config(page_title="Crypto Intelligence Dashboard", layout="wide")

# Custom CSS
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

if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = "BTC-USD"

# Section 1: Watchlist
cols = st.columns(5)
for i, ticker in enumerate(top_coins):
    with cols[i]:
        try:
            data = yf.download(ticker, period="5d", interval="1h", auto_adjust=True, progress=False)
            if not data.empty:
                latest_price = float(data['Close'].iloc[-1])
                prev_price = float(data['Close'].iloc[-2])
                pct_change = ((latest_price - prev_price) / prev_price) * 100
                
                if st.button(f"{ticker.replace('-USD', '')}"):
                    st.session_state.selected_ticker = ticker
                
                st.metric(label="", value=f"${latest_price:,.2f}", delta=f"{pct_change:+.2f}%")
        except Exception:
            st.error("Error")

st.divider()

# Section 2: Chart & Signals
selected = st.session_state.selected_ticker
st.subheader(f"🕯️ {selected} Real-Time Candle Chart")
timeframe = st.sidebar.selectbox("Select Chart Timeframe", ["1d", "1h", "15m", "5m"], index=1)

try:
    detail_data = yf.download(selected, period="60d", interval=timeframe, auto_adjust=True)
    if not detail_data.empty:
        # Indicator calculation fix
        close_series = detail_data['Close'].squeeze()
        if isinstance(close_series, pd.DataFrame): 
            close_series = close_series.iloc[:, 0]
            
        detail_data['MA20'] = ta.trend.sma_indicator(close_series, window=20)
        rsi_series = ta.momentum.rsi(close_series, window=14)
        
        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(x=detail_data.index,
                        open=detail_data['Open'], high=detail_data['High'],
                        low=detail_data['Low'], close=detail_data['Close'], name='Price')])
        
        fig.add_trace(go.Scatter(x=detail_data.index, y=detail_data['MA20'], line=dict(color='orange', width=1.5), name='MA20'))
        fig.update_layout(height=500, template="plotly_white", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Signals
        m1, m2 = st.columns(2)
        latest_rsi = float(rsi_series.iloc[-1])
        m1.metric("Current RSI (14)", f"{latest_rsi:.2f}")
        
        if latest_rsi < 35: m2.success("AI Signal: 🟢 STRONG BUY")
        elif latest_rsi > 65: m2.error("AI Signal: 🔴 STRONG SELL")
        else: m2.warning("AI Signal: 🟡 NEUTRAL / HOLD")
except Exception as e:
    st.error(f"Error loading chart: {e}")
