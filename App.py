import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

# Page Layout
st.set_page_config(page_title="Crypto Pro Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("💹 Crypto Pro Intelligence")
st.write("Live Market Dashboard (Groww & Delta Style)")

# Top 5 Coins
top_coins = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"]

# Sidebar Settings
st.sidebar.header("⚙️ Settings")
timeframe = st.sidebar.selectbox("Interval", ["1d", "1h", "15m", "5m"])

# Section 1: Watchlist Cards
st.subheader("Market Watchlist")
cols = st.columns(5)

if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = "BTC-USD"

for i, ticker in enumerate(top_coins):
    with cols[i]:
        try:
            # Data fetch with auto_adjust
            data = yf.download(ticker, period="30d", interval="1d", auto_adjust=True, progress=False)
            if not data.empty:
                # Error Fix: .iloc[-1] ke saath .item() ya float use karna
                latest = float(data['Close'].iloc[-1])
                prev = float(data['Close'].iloc[-2])
                change = ((latest - prev) / prev) * 100
                
                if st.button(f"Analyze {ticker.replace('-USD', '')}"):
                    st.session_state.selected_ticker = ticker
                
                st.metric(label="", value=f"${latest:,.2f}", delta=f"{change:+.2f}%")
        except:
            st.error("Data Error")

st.divider()

# Section 2: Fixed Candlestick Chart
selected = st.session_state.selected_ticker
st.subheader(f"🕯️ {selected} Interactive Candle Chart")

try:
    detail_data = yf.download(selected, period="60d", interval=timeframe, auto_adjust=True)
    
    if not detail_data.empty:
        # Error Fix: Close data ko 1D series mein badalna
        close_series = detail_data['Close'].iloc[:, 0] if len(detail_data['Close'].shape) > 1 else detail_data['Close']
        close_series = pd.Series(close_series).ffill() # Handle missing values

        # Indicators Calculation
        detail_data['MA20'] = ta.trend.sma_indicator(close_series, window=20)
        rsi_series = ta.momentum.rsi(close_series, window=14)
        
        # Plotly Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=detail_data.index,
            open=detail_data['Open'],
            high=detail_data['High'],
            low=detail_data['Low'],
            close=detail_data['Close'],
            name='Market Price'
        ))
        
        if 'MA20' in detail_data:
            fig.add_trace(go.Scatter(x=detail_data.index, y=detail_data['MA20'], 
                                     line=dict(color='orange', width=1.2), name='MA20 Trend'))

        fig.update_layout(height=500, template="plotly_white", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Analytics Metrics
        latest_rsi = float(rsi_series.iloc[-1])
        m1, m2 = st.columns(2)
        
        m1.metric("RSI (14)", f"{latest_rsi:.2f}")
        if latest_rsi < 35: m2.success("Signal: 🟢 BUY")
        elif latest_rsi > 65: m2.error("Signal: 🔴 SELL")
        else: m2.warning("Signal: 🟡 NEUTRAL")

except Exception as e:
    st.error(f"Technical Fix Required: {e}")
    
