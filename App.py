import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# Groww-style Page Config (Wide Mode)
st.set_page_config(page_title="Crypto AI Dashboard", layout="wide")

# Custom Styling for Groww Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #111; }
    </style>
    """, unsafe_allow_html=True)

st.title("💹 My Pro Crypto Dashboard")
st.write("Top 5 Coins Live Analysis (Groww & Delta Style)")

# List of Top 5 Coins
top_coins = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"]

# Sidebar Settings
st.sidebar.header("📊 Settings")
timeframe = st.sidebar.selectbox("Select Timeframe", ["1d", "1h", "15m"])
chart_points = st.sidebar.slider("Chart Data Points", 50, 300, 100)

def get_signal(rsi):
    if rsi < 35: return "🟢 BUY", "success"
    elif rsi > 65: return "🔴 SELL", "error"
    else: return "🟡 HOLD", "warning"

# Section 1: Dashboard Cards (Groww Style)
st.subheader("Market Overview")
cols = st.columns(5)

for i, ticker in enumerate(top_coins):
    with cols[i]:
        try:
            # Data fetch
            data = yf.download(ticker, period="60d", interval=timeframe, auto_adjust=True, progress=False)
            if not data.empty:
                close_prices = data['Close'].squeeze()
                latest_price = float(close_prices.iloc[-1])
                prev_price = float(close_prices.iloc[-2])
                price_change = latest_price - prev_price
                pct_change = (price_change / prev_price) * 100

                # Metric Display (Price & Percentage)
                st.metric(label=ticker.replace("-USD", ""), 
                          value=f"${latest_price:,.2f}", 
                          delta=f"{pct_change:+.2f}%")
                
                # Signal logic
                rsi_val = ta.momentum.rsi(close_prices, window=14).iloc[-1]
                sig_text, sig_style = get_signal(rsi_val)
                
                if sig_style == "success": st.success(sig_text)
                elif sig_style == "error": st.error(sig_text)
                else: st.warning(sig_text)
        except Exception:
            st.error(f"{ticker} Offline")

st.divider()

# Section 2: Detailed Analysis (Delta Exchange Style)
st.subheader("🔍 Detailed Analysis")
selected_coin = st.selectbox("Select a coin for deep analysis:", top_coins)

if selected_coin:
    # Large Data Fetch
    detail_data = yf.download(selected_coin, period="max", interval=timeframe, auto_adjust=True)
    detail_close = detail_data['Close'].squeeze()
    
    # Advanced Indicators
    detail_data['MA20'] = ta.trend.sma_indicator(detail_close, window=20)
    detail_data['RSI'] = ta.momentum.rsi(detail_close, window=14)
    
    # Columns for Chart and Stats
    c1, c2 = st.columns([3, 1])
    
    with c1:
        st.write(f"**{selected_coin} Interactive Chart**")
        st.line_chart(detail_data[['Close', 'MA20']].tail(chart_points))
        
    with c2:
        st.write("**Technical Stats**")
        current_rsi = detail_data['RSI'].iloc[-1]
        st.write(f"**Current RSI:** `{current_rsi:.2f}`")
        st.write(f"**20 Day Moving Avg:** `${detail_data['MA20'].iloc[-1]:,.2f}`")
        
        if current_rsi < 30:
            st.info("Market Condition: **Oversold** (Price might bounce back)")
        elif current_rsi > 70:
            st.info("Market Condition: **Overbought** (Price might fall)")
