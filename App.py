import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Personal Trading AI", layout="centered")
st.title("📈 My Personal AI Trader")

ticker = st.text_input("Coin ka naam (e.g., BTC-USD):", "BTC-USD")
timeframe = st.selectbox("Timeframe:", ["1d", "1h", "15m"])

if ticker:
    try:
        # Period ko 'max' kiya hai taaki indicator ban sake
        data = yf.download(ticker, period="max", interval=timeframe)
        
        if data is not None and len(data) > 30:
            # Calculation
            data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
            data['MA20'] = ta.trend.sma_indicator(data['Close'], window=20)
            
            # Sirf aakhiri 100 din ka chart dikhane ke liye
            chart_data = data.tail(100)
            
            latest_price = float(data['Close'].iloc[-1])
            st.metric("Live Price", f"${latest_price:,.2f}")
            
            st.subheader("Price Chart")
            st.line_chart(chart_data['Close'])
            
            st.subheader("🤖 AI Signal")
            latest_rsi = data['RSI'].iloc[-1]
            if latest_rsi < 40:
                st.success("Signal: 🟢 BUY")
            elif latest_rsi > 60:
                st.error("Signal: 🔴 SELL")
            else:
                st.warning("Signal: 🟡 HOLD")
        else:
            st.info("Data load ho raha hai... Kripya thoda intezar karein ya ticker check karein.")
            
    except Exception as e:
        st.error(f"Error: {e}")
        
