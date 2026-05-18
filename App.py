import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime

# ============================================================================
# SYSTEM CORE PROPERTIES & MULTI-PAGE VIEWPORT CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="DELTA TERMINAL v6.0 • ADVANCED TRADING DESK", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Persistent Session state modules for live trading state
if "account_margin_base" not in st.session_state:
    st.session_state.account_margin_base = 25000.0
if "risk_allowance_percentage" not in st.session_state:
    st.session_state.risk_allowance_percentage = 1.5
if "simulated_order_book_cache" not in st.session_state:
    st.session_state.simulated_order_book_cache = [
        "SYSTEM: Execution matrix online.",
        "ORDER: Long BTC at $68,450.00 | Target hit +$420.00",
        "ORDER: Short ETH at $3,510.00 | SL triggered -$110.00"
    ]
if "global_active_symbol" not in st.session_state:
    st.session_state.global_active_symbol = "BTC"

# Core styling injection across sub-panels
st.markdown("""
<style>
    .stApp { background-color: #060709 !important; color: #d1d4dc !important; }
    .sidebar .sidebar-content { background-color: #0b0e11 !important; }
    .crypto-card-container { background-color: #12161a; border: 1px solid #232830; padding: 12px; border-radius: 6px; margin-bottom: 10px; }
    .news-card-frame { background-color: #111318; border-left: 4px solid #0ecb81; padding: 15px; border-radius: 4px; margin-bottom: 12px; }
    .news-impact-high { color: #f6465d; font-weight: bold; background: rgba(246, 70, 93, 0.1); padding: 2px 6px; border-radius: 3px; }
    .news-impact-bullish { color: #0ecb81; font-weight: bold; background: rgba(14, 203, 129, 0.1); padding: 2px 6px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Helper function to query live parameters securely with fallback stability
def query_ticker_safe(token_symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={token_symbol}USDT"
        res = requests.get(url, timeout=2).json()
        return {
            "last": float(res['lastPrice']),
            "change": float(res['priceChangePercent']),
            "high": float(res['highPrice']),
            "low": float(res['lowPrice']),
            "vol": float(res['quoteVolume'])
        }
    except:
        mock_data = {
            "BTC": {"last": 67845.50, "change": 1.45, "high": 68500.00, "low": 66200.00, "vol": 1240000000},
            "ETH": {"last": 3485.20, "change": -0.82, "high": 3560.00, "low": 3410.00, "vol": 680000000},
            "SOL": {"last": 142.75, "change": 4.12, "high": 145.00, "low": 135.20, "vol": 410000000},
            "BNB": {"last": 575.40, "change": 0.25, "high": 582.00, "low": 570.10, "vol": 150000000},
            "XRP": {"last": 0.52, "change": -1.15, "high": 0.54, "low": 0.51, "vol": 90000000},
            "ADA": {"last": 0.44, "change": 0.08, "high": 0.46, "low": 0.43, "vol": 45000000},
            "DOT": {"last": 6.15, "change": 2.31, "high": 6.30, "low": 5.95, "vol": 32000000},
            "DOGE": {"last": 0.14, "change": 5.84, "high": 0.15, "low": 0.13, "vol": 21000000}
        }
        return mock_data.get(token_symbol, {"last": 100.0, "change": 0.0, "high": 105.0, "low": 95.0, "vol": 5000000})

# ============================================================================
# NAVIGATION ENGINE (SIDEBAR ROUTER)
# ============================================================================
st.sidebar.markdown('<h2 style="color:#0ecb81; font-family:monospace; margin-bottom:0px;">❖ DELTA V6.0</h2>', unsafe_allow_html=True)
st.sidebar.text("QUANT TRADING DESK")
st.sidebar.markdown("---")

app_navigation_panel = st.sidebar.radio(
    "NAVIGATION HUB",
    ["🏠 Home (Market Matrix)", "📈 Advanced Live Charts", "📰 AI Live News Room", "💰 Profit & PnL Ledger"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Global Focus Asset")
user_input_symbol = st.sidebar.text_input("Change target global tracking asset pair:", value=st.session_state.global_active_symbol)
st.session_state.global_active_symbol = user_input_symbol.upper().strip()

# ============================================================================
# PANEL 1: HOME PAGE (CRYPTO MARKET MATRIX)
# ============================================================================
if app_navigation_panel == "🏠 Home (Market Matrix)":
    st.markdown("## 🏠 CRYPTO ASSET MANAGEMENT SYSTEM")
    st.write("Real-time pricing matrix from international high-frequency processing pipelines.")
    st.markdown("---")
    
    monitored_tokens = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOT", "DOGE"]
    
    st.markdown("### ❖ CORE MARKET WATCHLIST")
    row1_cols = st.columns(4)
    row2_cols = st.columns(4)
    all_view_cols = row1_cols + row2_cols
    
    for idx, sym in enumerate(monitored_tokens):
        with all_view_cols[idx]:
            metrics = query_ticker_safe(sym)
            sign = "+" if metrics["change"] >= 0 else ""
            
            st.markdown(f"""
            <div class="crypto-card-container">
                <h4 style="margin:0px; color:#848e9c;">{sym}/USDT</h4>
                <h2 style="margin:8px 0px; color:#ffffff;">${metrics['last']:,.2f}</h2>
                <p style="margin:0px; font-size:14px;">24h Change: <span style="color:{'#0ecb81' if metrics['change'] >=0 else '#f6465d'}">{sign}{metrics['change']:.2f}%</span></p>
                <p style="margin:4px 0px 0px 0px; font-size:11px; color:#5e6673;">Vol: ${metrics['vol']/1000000:.1f}M | High: ${metrics['high']:,.1f}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info(f"💡 Currently target focus pipeline is mapped across **{st.session_state.global_active_symbol}USDT**. Head over to 'Advanced Live Charts' panel to view active visual setups.")

# ============================================================================
# PANEL 2: CHART PAGE (TRADINGVIEW LIVE WORKSPACE INTERFACE)
# ============================================================================
elif app_navigation_panel == "📈 Advanced Live Charts":
    st.markdown(f"## 📈 ADVANCED LIVE CHARTS INFRASTRUCTURE")
    st.write(f"Focus Asset Vector Pipeline: **{st.session_state.global_active_symbol}/USDT**")
    st.markdown("---")
    
    chart_layout_left, chart_layout_right = st.columns([3.5, 1])
    active_metrics = query_ticker_safe(st.session_state.global_active_symbol)
    
    with chart_layout_left:
        tv_widget_url = f"https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:{st.session_state.global_active_symbol}USDT&interval=15&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=111318&theme=dark&style=1&timezone=Asia%2FKolkata"
        st.components.v1.iframe(src=tv_widget_url, height=580, scrolling=False)
        
    with chart_layout_right:
        st.markdown(f"""
        <div style="background-color:#12161a; padding:15px; border-radius:6px; border:1px solid #232830; height:580px;">
            <h3 style="margin-top:0px; color:#0ecb81;">📊 TELEMETRY HUB</h3>
            <p style="font-size:12px; color:#848e9c;">SYMBOL CORE IDENTIFIER</p>
            <h2 style="margin-top:0px;">{st.session_state.global_active_symbol}USDT</h2>
            <hr style="border-color:#232830;">
            <p><b>LAST MARKET VALUE:</b><br><span style="font-size:20px; color:#ffffff;">${active_metrics['last']:,.2f}</span></p>
            <p><b>24H SPREAD HIGH:</b><br>${active_metrics['high']:,.2f}</p>
            <p><b>24H SPREAD LOW:</b><br>${active_metrics['low']:,.2f}</p>
            <p><b>TURNOVER VOLUME:</b><br>${active_metrics['vol']/1000000:,.2f}M</p>
            <hr style="border-color:#232830;">
            <h4>🤖 AI MOMENTUM BIAS</h4>
            {"<span class='news-impact-bullish'>🎯 STRONGLY BULLISH</span>" if active_metrics['change'] >= 0 else "<span class='news-impact-high'>⚠️ BEARISH MOMENTUM</span>"}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PANEL 3: NEWS PAGE (AI LIVE INTEGRATION FEEDS MATRIX)
# ============================================================================
elif app_navigation_panel == "📰 AI Live News Room":
    st.markdown("## 📰 AI ADVANCED NEWS FEED & QUANT DECODER")
    st.write("Automated natural language parsing tracking macro volatility markers impacting asset systems.")
    st.markdown("---")
    
    news_feed_database = [
        {"time": "Just Now", "title": "US CPI Data Printing Lower Than Projections; Implied Fed Rate Cuts Imminent", "impact": "HIGH IMPACT / HIGHLY BULLISH", "type": "bullish", "desc": "AI Parse: Core Inflation drops to 3.1%. Liquidity flows immediately surging capital indexes toward risk assets. Bitcoin volatility spikes upward +3.4% within 180 seconds."},
        {"time": "14 mins ago", "title": "Binance Deploys Comprehensive Institutional Liquidity Vault Protocols across SOL Ecosystem Assets", "impact": "MID IMPACT / BULLISH", "type": "bullish", "desc": "AI Parse: Automated orderbooks across decentralized rails observe thick bid-side deployment setups."},
        {"time": "1 hour ago", "title": "Regulatory Compliance Audits Targeted Across Major Stablecoin Reserves Interrupted by Sudden Investigations", "impact": "CRITICAL RISK / BEARISH", "type": "high", "desc": "AI Parse: Temporary fear indicators trigger quick capital outflows into cash reserves. Scaling short-term risk models recommended."},
        {"time": "3 hours ago", "title": "Whale Order Monitoring Systems Track Outsized Spot Accumulation Patterns Near Support Channels", "impact": "LOW IMPACT / STABLE", "type": "bullish", "desc": "AI Parse: Over 4,200 BTC transferred out of exchanges into cold storage systems. Selling pressure drops dramatically."}
    ]
    
    for item in news_feed_database:
        impact_tag = f'<span class="news-impact-bullish">{item["impact"]}</span>' if item["type"] == "bullish" else f'<span class="news-impact-high">{item["impact"]}</span>'
        st.markdown(f"""
        <div class="news-card-frame">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:12px; color:#848e9c; font-family:monospace;">🕒 {item['time']}</span>
                {impact_tag}
            </div>
            <h4 style="margin:5px 0px; color:#ffffff; font-size:16px;">{item['title']}</h4>
            <p style="margin:5px 0px 0px 0px; color:#b7bdc6; font-size:13px; line-height:1.4;">{item['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PANEL 4: PROFIT PAGE (FINANCIAL DESK LEDGER)
# ============================================================================
elif app_navigation_panel == "💰 Profit & PnL Ledger":
    st.markdown("## 💰 TRADING ACCOUNT BALANCES & RISK MANAGEMENT ENGINE")
    st.write("Track capital allocation math, record simulated executions, and configure margin lines.")
    st.markdown("---")
    
    pnl_metrics_left, pnl_metrics_right = st.columns([1.8, 2])
    
    with pnl_metrics_left:
        st.markdown("### 📐 CAPITAL ENGINE CONFIGURATOR")
        st.session_state.account_margin_base = st.number_input("Global Available Collateral Capital Reserve Base ($)", value=st.session_state.account_margin_base, step=500.0)
        st.session_state.risk_allowance_percentage = st.number_input("Max Allowable Stop Loss Allocation Threshold (%)", value=st.session_state.risk_allowance_percentage, min_value=0.1, max_value=5.0, step=0.1)
        
        target_entry = st.number_input("Calculated Asset Execution Setup Trigger Entry Price ($)", value=query_ticker_safe(st.session_state.global_active_symbol)["last"])
        target_sl = st.number_input("Calculated Invalid Target Stop Loss Protection Price ($)", value=query_ticker_safe(st.session_state.global_active_symbol)["last"] * 0.98)
        
        price_spread_distance = abs(target_entry - target_sl)
        if price_spread_distance > 0:
            total_cash_risk_pool = st.session_state.account_margin_base * (st.session_state.risk_allowance_percentage / 100.0)
            calculated_units = total_cash_risk_pool / price_spread_distance
            notional_value = calculated_units * target_entry
            mathematical_leverage = notional_value / st.session_state.account_margin_base
            
            st.markdown(f"""
            <div style="background-color:rgba(14, 203, 129, 0.05); border:1px dashed #0ecb81; padding:15px; border-radius:5px; margin:15px 0px;">
                <p style="margin:0px; color:#0ecb81; font-weight:bold;">⚡ RISK ALLOCATION RESULTS:</p>
                <p style="margin:4px 0px;"><b>Total Cash Loss Risk Cap:</b> ${total_cash_risk_pool:,.2f}</p>
                <p style="margin:4px 0px;"><b>Max Position Volume Size:</b> {calculated_units:.4f} {st.session_state.global_active_symbol}</p>
                <p style="margin:4px 0px;"><b>Required Systematic Leverage Ratio:</b> {mathematical_leverage:.2f}x</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Log Position Execution Parameters", use_container_width=True):
                current_time_string = time.strftime("%H:%M:%S")
                logged_trade_string = f"[{current_time_string}] EXECUTED: Buy {calculated_units:.3f} {st.session_state.global_active_symbol} at ${target_entry:,.2f} | Risk Pool Cap: ${total_cash_risk_pool:,.2f}"
                st.session_state.simulated_order_book_cache.insert(0, logged_trade_string)
                st.success("Trade state registered across session databases.")
                st.rerun()

    with pnl_metrics_right:
        st.markdown("### 📋 REAL-TIME ACCOUNT ACTIVITY LOGS")
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("TOTAL ACCOUNT RESERVE VALUE", f"${st.session_state.account_margin_base:,.2f}", "+$310.50 Today")
        with metric_col2:
            st.metric("NET PERFORMANCE WIN RATE", "68.4%", "+2.1% This Week")
            
        st.markdown("<br><b>HISTORICAL RECENT ORDER LOG ACTIONS</b>", unsafe_allow_html=True)
        for log_entry in st.session_state.simulated_order_book_cache[:6]:
            st.code(log_entry)

# ============================================================================
# SYSTEM RENDER BOTTOM PANEL STATUS FOOTER
# ============================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:11px; font-family:monospace; color:#474f5c;'>DELTA QUANT NETWORK PIPELINE RENDER ENGINE v6.0 PRO • ALL MODULE SYSTEMS STATUS: OPERATIONAL ONLINE</p>", unsafe_allow_html=True)
            
