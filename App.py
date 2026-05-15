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
    .stMetric { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); cursor: pointer; }
    div[data-testid="stMetricDelta"] svg { display: none; } /* Hide default arrows */
    </style>
    """, unsafe_allow_html=True)

st.title("💹 Crypto Pro Intelligence")
st.write("Live Market Dashboard (Groww & Delta Style)")

# Top 5 Coins
top_coins = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"]

# Sidebar for User Interaction
st.sidebar.header("⚙️ Settings")
timeframe = st.sidebar.selectbox("Interval", ["1d", "1h", "15m", "5m"])
period = "60d" if timeframe in ["1h", "15m", "5m"] else "max"

# Section 1: Groww-style Market Cards
st.subheader("Market Watchlist")
cols = st.columns(5)

# Selection state maintain karne ke liye
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = "BTC-USD"

for i, ticker in enumerate(top_coins):
    with cols[i]:
        try:
            # Chota data download signals ke liye
            data = yf.download(ticker, period="30d", interval="1d", progress=False)
            if not data.empty:
                latest = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2]
                change = ((latest - prev) / prev) * 100
                
                # Card button to select coin
                if st.button(f"{ticker.replace('-USD', '')}"):
                    st.session_state.selected_ticker = ticker
                
                st.metric(label="", value=f"${float(latest):,.2f}", delta=f"{float(change):+.2f}%")
        except:
            st.error("Error")

st.divider()

# Section 2: Delta Exchange-style Candlestick Chart
selected = st.session_state.selected_ticker
st.subheader(f"🕯️ {selected} Interactive Candle Chart")

try:
    # Detailed Data download
    detail_data = yf.download(selected, period="60d", interval=timeframe, auto_adjust=False)
    
    if not detail_data.empty:
        # Indicators
        detail_data['MA20'] = ta.trend.sma_indicator(detail_data['Close'], window=20)
        
        # Plotly Candlestick Chart
        fig = go.Figure()
        
        # Adding Candlesticks
        fig.add_trace(go.Candlestick(
            x=detail_data.index,
            open=detail_data['Open'],
            high=detail_data['High'],
            low=detail_data['Low'],
            close=detail_data['Close'],
            name='Price'
        ))
        
        # Adding MA20 Line
        fig.add_trace(go.Scatter(x=detail_data.index, y=detail_data['MA20'], 
                                 line=dict(color='orange', width=1.5), name='MA20'))
        
        # Chart Design Improvement
        fig.update_layout(
            height=600,
            template="plotly_white",
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Logic Summary
        rsi = ta.momentum.rsi(detail_data['Close'], window=14).iloc[-1]
        
        m1, m2, m3 = st.columns(3)
        m1.info(f"**Current RSI:** {float(rsi):.2f}")
        
        if rsi < 35:
            m2.success("Signal: 🟢 STRONG BUY")
        elif rsi > 65:
            m2.error("Signal: 🔴 STRONG SELL")
        else:
            m2.warning("Signal: 🟡 NEUTRAL / WAIT")
            
        m3.write(f"**Last Close:** ${float(detail_data['Close'].iloc[-1]):,.2f}")

except Exception as e:
    st.error(f"Chart Load Error: {e}")
    
