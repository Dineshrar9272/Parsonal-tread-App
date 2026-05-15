import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Crypto Intelligence", layout="wide")

st.title("💹 Crypto Intelligence Dashboard")
st.write("Live Top 5 Coins - Delta Exchange Style")

# 2. Coins List
top_coins = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"]

# 3. Sidebar for Timeframe
timeframe = st.sidebar.selectbox("Select Timeframe", ["1d", "1h", "15m", "5m"], index=1)

# Initialize Session State
if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = "BTC-USD"

# 4. Top Watchlist Section
cols = st.columns(5)
for i, ticker in enumerate(top_coins):
    with cols[i]:
        if st.button(f"Analyze {ticker.replace('-USD', '')}"):
            st.session_state.selected_coin = ticker
        
        try:
            # Sirf latest price fetch karne ke liye simple call
            price_data = yf.Ticker(ticker).history(period="2d")
            if not price_data.empty:
                current_p = price_data['Close'].iloc[-1]
                prev_p = price_data['Close'].iloc[-2]
                diff = ((current_p - prev_p) / prev_p) * 100
                st.metric(label="", value=f"${current_p:,.2f}", delta=f"{diff:+.2f}%")
        except:
            st.write("Loading...")

st.divider()

# 5. Candlestick Chart Section
sel_ticker = st.session_state.selected_coin
st.subheader(f"🕯️ {sel_ticker} Candle Chart")

try:
    # Chart data fetch
    df = yf.download(sel_ticker, period="30d", interval=timeframe, auto_adjust=True)
    
    if not df.empty:
        # Candle Chart Create
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        )])
        
        fig.update_layout(
            height=500, 
            template="plotly_white", 
            xaxis_rangeslider_visible=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Simple Logic Analysis
        last_close = df['Close'].iloc[-1]
        st.info(f"Last Closing Price: **${last_close:,.2f}**")
    else:
        st.warning("Data not available for this timeframe. Try '1d' or '1h'.")

except Exception as e:
    st.error("Connection slow hai, कृपया 'Rerun' बटन दबाएं।")
    
