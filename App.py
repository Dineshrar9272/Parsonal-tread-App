import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Old Style Chart Analysis App", layout="wide")
st.title("📈 Stock Chart Analysis Dashboard")
st.write("Yeh app historical data fetch karke technical aur chart analysis dikhata hai.")

# --- SIDEBAR - INPUTS ---
st.sidebar.header("User Inputs")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, TSLA, RELIANCE.NS)", value="AAPL").upper().strip()

# Date settings (Pichle 1 saal ka data)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# --- DATA FETCHING ---
@st.cache_data
def load_data(stock_ticker):
    try:
        # Ticker object ka use karke history nikal rahe hain takki multi-index columns ka error na aaye
        ticker_obj = yf.Ticker(stock_ticker)
        data = ticker_obj.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        return pd.DataFrame()

df = load_data(ticker)

# Check if data is valid
if df.empty or len(df) < 20:
    st.warning(f"⏳ Ticker '{ticker}' ka data load ho raha hai ya fir symbol galat hai. Agar data nahi aata, toh sidebar mein sahi ticker dalein (Jaise: TSLA ya Indian stocks ke liye RELIANCE.NS).")
else:
    try:
        # --- TECHNICAL ANALYSIS CALCULATIONS ---
        # Naye yfinance mein columns capital hote hain (Open, High, Low, Close)
        df['20_SMA'] = df['Close'].rolling(window=20).mean()
        df['50_SMA'] = df['Close'].rolling(window=50).mean()

        # Latest day ki values nikalna analysis ke liye
        latest_close = float(df['Close'].iloc[-1])
        latest_open = float(df['Open'].iloc[-1])
        latest_high = float(df['High'].iloc[-1])
        latest_low = float(df['Low'].iloc[-1])
        sma_20 = float(df['20_SMA'].iloc[-1])

        # 2. Candlestick Chart Analysis Logic (Hammer Pattern)
        body_size = abs(latest_close - latest_open)
        
        if latest_open > latest_close:
            lower_wick = latest_close - latest_low
            upper_wick = latest_high - latest_open
        else:
            lower_wick = latest_open - latest_low
            upper_wick = latest_high - latest_close

        # Hammer check: Lower wick body se kam se kam 2 guna badi ho
        is_hammer = (lower_wick >= 2 * body_size) and (upper_wick <= 0.1 * body_size)

        # --- DISPLAY RESULTS (METRICS) ---
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Latest Close Price", value=f"${latest_close:,.2f}")
        col2.metric(label="20 Day SMA", value=f"${sma_20:,.2f}")
        
        # Trend status
        if latest_close > sma_20:
            trend = "🟢 Bullish (Above 20 SMA)"
        else:
            trend = "🔴 Bearish (Below 20 SMA)"
        col3.metric(label="Current Trend", value=trend)

        # --- CHART ANALYSIS REPORT BOX ---
        st.subheader("📋 Chart Analysis Report")
        if is_hammer:
            st.success("🎯 **Bullish Hammer Pattern Detected!** Yeh ek potential trend reversal (upmove) ka signal ho sakta hai.")
        else:
            st.info("ℹ️ Latest candle par koi specific Candlestick Pattern (जैसे Hammer) nahi mila. Market normal trend follow kar raha hai.")

        # --- VISUALIZATION (PLOTLY CHART) ---
        st.subheader("📊 Price Chart with Moving Averages")
        
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Market Price"
        ))
        
        # 20 SMA Line
        fig.add_trace(go.Scatter(
            x=df.index, y=df['20_SMA'], 
            mode='lines', name='20 SMA', 
            line=dict(color='orange', width=1.5)
        ))

        fig.update_layout(
            title=f"{ticker} Price Analysis",
            xaxis_rangeslider_visible=False,
            yaxis_title="Price",
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # --- DATA TABLE ---
        st.subheader("📂 Recent Historical Data")
        st.dataframe(df.tail(10))

    except Exception as e:
        st.error(f"Data processing mein dikkat aayi: {e}")
        
