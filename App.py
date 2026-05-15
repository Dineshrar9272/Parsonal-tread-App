import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# Page Configuration
st.set_page_config(page_title="Personal Trading AI", layout="centered")
st.title("📈 My Personal AI Trader")

# User Input
ticker = st.text_input("Coin ka naam (e.g., BTC-USD):", "BTC-USD")
timeframe = st.selectbox("Timeframe:", ["1d", "1h", "15m"])

if ticker:
    try:
        # Data fetch karna (period 'max' rakha hai taaki indicators sahi bane)
        data = yf.download(ticker, period="max", interval=timeframe, auto_adjust=True)
        
        if data is not None and len(data) > 30:
            # Error Fix: .squeeze() ka use karke data shape sahi karna
            close_prices = data['Close'].squeeze()
            
            # Indicators Calculation
            data['RSI'] = ta.momentum.rsi(close_prices, window=14)
            data['MA20'] = ta.trend.sma_indicator(close_prices, window=20)
            
            # Sirf aakhiri 100 entries dikhane ke liye taaki chart saaf dikhe
            chart_data = data.tail(100)
            
            # Current Price Display
            latest_price = float(close_prices.iloc[-1])
            st.metric("Live Price", f"${latest_price:,.2f}")
            
            # Chart Display
            st.subheader("Price Chart (Last 100 periods)")
            st.line_chart(chart_data['Close'].squeeze())
            
            # AI Signals based on RSI
            st.subheader("🤖 AI Signal")
            latest_rsi = float(data['RSI'].iloc[-1])
            
            if latest_rsi < 35:
                st.success(f"Signal: 🟢 BUY (RSI: {latest_rsi:.2f} - Market is Oversold)")
            elif latest_rsi > 65:
                st.error(f"Signal: 🔴 SELL (RSI: {latest_rsi:.2f} - Market is Overbought)")
            else:
                st.warning(f"Signal: 🟡 HOLD (RSI: {latest_rsi:.2f} - Wait for trend)")
                
        else:
            st.info("Data load ho raha hai ya ticker galat hai. Kripya check karein.")
            
    except Exception as e:
        # User ko error ki wajah saaf dikhegi
        st.error(f"Technical Error: {e}")
