
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
        data = yf.download(ticker, period="60d", interval=timeframe)
        if data.empty or len(data) < 20:
            st.error("Data nahi mil raha! Symbol check karein.")
        else:
            data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
            data['MA20'] = ta.trend.sma_indicator(data['Close'], window=20)
            
            latest_price = float(data['Close'].iloc[-1])
            latest_rsi = float(data['RSI'].iloc[-1])
            latest_ma = float(data['MA20'].iloc[-1])
            
            st.metric("Live Price", f"${latest_price:,.2f}")
            st.metric("RSI (14)", f"{latest_rsi:.2f}")
            
            st.subheader("Price & MA20 Chart")
            st.line_chart(data[['Close', 'MA20']])
            
            st.subheader("🤖 AI Signal")
            if latest_rsi < 35 and latest_price > latest_ma:
                st.success("Signal: 🟢 BUY")
            elif latest_rsi > 65 or latest_price < latest_ma:
                st.error("Signal: 🔴 SELL")
            else:
                st.warning("Signal: 🟡 HOLD")
    except Exception as e:
        st.info("Sahi ticker dalein.")
