import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

# ============================================================================
# PROTOCOL 1: SYSTEM PROPERTIES & STABLE SESSION INITIALIZATION
# ============================================================================
st.set_page_config(
    page_title="DELTA TERMINAL v5.0", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Sessions state initialization
if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False
if "terminal_active_tab" not in st.session_state:
    st.session_state.terminal_active_tab = "📊 Live Terminal Workspace"
if "account_margin_base" not in st.session_state:
    st.session_state.account_margin_base = 25000.0
if "risk_allowance_percentage" not in st.session_state:
    st.session_state.risk_allowance_percentage = 1.5
if "simulated_order_book_cache" not in st.session_state:
    st.session_state.simulated_order_book_cache = []
if "system_runtime_logs" not in st.session_state:
    st.session_state.system_runtime_logs = [
        "System core modules compiled successfully.",
        "Binance market data pipeline initialized."
    ]

def add_system_log(message_body):
    current_timestamp = time.strftime("%H:%M:%S")
    st.session_state.system_runtime_logs.insert(0, f"[{current_timestamp}] {message_body}")
    if len(st.session_state.system_runtime_logs) > 20:
        st.session_state.system_runtime_logs.pop()

@st.cache_data(ttl=5)
def get_binance_ticker_matrix(ticker_symbol):
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=" + str(ticker_symbol) + "USDT"
        response_payload = requests.get(url, timeout=3).json()
        return {
            "status": True,
            "last_price": float(response_payload['lastPrice']),
            "price_change_percent": float(response_payload['priceChangePercent']),
            "high_price": float(response_payload['highPrice']),
            "low_price": float(response_payload['lowPrice']),
            "volume_base": float(response_payload['volume']),
            "quote_volume_turnover": float(response_payload['quoteVolume']),
            "weighted_avg_price_vwap": float(response_payload['weightedAvgPrice'])
        }
    except:
        return {"status": False, "last_price": 0.0, "price_change_percent": 0.0, "high_price": 0.0, "low_price": 0.0, "volume_base": 0.0, "quote_volume_turnover": 0.0, "weighted_avg_price_vwap": 0.0}

# ============================================================================
# PROTOCOL 2: CLEAN CSS INJECTION (FIXED PARAMETER)
# ============================================================================
st.markdown("""
<style>
    .stApp { background-color: #060709 !important; color: #d1d4dc !important; }
    .crypto-ticker-card { background-color: #111318; border: 1px solid #1f2229; padding: 10px; border-radius: 4px; text-align: center; }
    .terminal-panel-frame { background-color: #12161a; border: 1px solid #232830; border-radius: 6px; padding: 15px; margin-bottom: 12px; }
    .tag-bullish-indicator { color: #0ecb81; font-weight: bold; border: 1px solid #0ecb81; padding: 2px 5px; border-radius: 3px; }
    .tag-bearish-indicator { color: #f6465d; font-weight: bold; border: 1px solid #f6465d; padding: 2px 5px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True) # FIXED: changed unsafe_html to unsafe_allow_html

# ============================================================================
# PROTOCOL 3: CRYPTO TICKER RIBBON
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown('<h2 style="font-family:monospace; font-weight:bold; color:#0ecb81; margin-bottom:4px;">❖ DELTA SYSTEMS : QUANT TERMINAL PRO</h2>', unsafe_allow_html=True)
    
    monitored_token_list = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOT", "DOGE"]
    ticker_columns_layout_grid = st.columns(8)
    
    for array_index, token_symbol in enumerate(monitored_token_list):
        with ticker_columns_layout_grid[array_index]:
            token_stats_matrix = get_binance_ticker_matrix(token_symbol)
            if token_stats_matrix["status"]:
                change_sign_prefix = "+" if token_stats_matrix["price_change_percent"] >= 0 else ""
                st.metric(
                    label=token_symbol + "/USDT",
                    value=f"${token_stats_matrix['last_price']:,.2f}",
                    delta=f"{change_sign_prefix}{token_stats_matrix['price_change_percent']:.2f}%"
                )
            else:
                st.error(token_symbol + " OFFLINE")

# ============================================================================
# PROTOCOL 4: VIEWPORT CONTROL SYSTEM
# ============================================================================
st.markdown("<br>", unsafe_allow_html=True)
col_search_frame, col_viewport_toggle = st.columns([4, 1.5])

with col_search_frame:
    user_symbol_selection_input = st.text_input(
        "Primary Asset Selector",
        value="BTC",
        label_visibility="collapsed"
    )
    resolved_active_symbol = user_symbol_selection_input.upper().strip()

with col_viewport_toggle:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Multi-Grid View", use_container_width=True):
            st.session_state.fullscreen_mode = False
            st.rerun()
    else:
        if st.button("🔍 Maximize Chart", use_container_width=True):
            st.session_state.fullscreen_mode = True
            st.rerun()

active_focus_market_matrix = get_binance_ticker_matrix(resolved_active_symbol)

# ============================================================================
# PROTOCOL 5: ADVANCED LIVE CHART VIEW (TRADINGVIEW INTEGRATION)
# ============================================================================
if st.session_state.fullscreen_mode:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([1, 0]), None
else:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([3.2, 1])

with primary_workspace_left_grid:
    # This URL is the truly live Advanced Chart Widget
    live_chart_url = "https://s.tradingview.com/widgetembed/?frameElementId=tradingview_762ae&symbol=BINANCE:" + resolved_active_symbol + "USDT&interval=1&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=%5B%5D&theme=dark&style=1&timezone=Etc%2FUTC&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=en&utm_source=www.tradingview.com&utm_medium=widget&utm_campaign=chart&utm_term=BINANCE%3ABTCUSDT"
    
    st.components.v1.iframe(src=live_chart_url, height=550, scrolling=False)

if secondary_workspace_right_grid is not None:
    with secondary_workspace_right_grid:
        st.markdown(f'<div class="terminal-panel-frame" style="height: 550px;">'
                    f'<h3>📊 HUB MATRIX: {resolved_active_symbol}</h3>'
                    f'<hr>'
                    f'<p><b>SPOT:</b> ${active_focus_market_matrix["last_price"]:,.2f}</p>'
                    f'<p><b>24h HIGH:</b> ${active_focus_market_matrix["high_price"]:,.2f}</p>'
                    f'<p><b>24h LOW:</b> ${active_focus_market_matrix["low_price"]:,.2f}</p>'
                    f'<p><b>VOL:</b> ${active_focus_market_matrix["quote_volume_turnover"]/1000000:,.1f}M</p>'
                    f'<hr>'
                    f'<h4>⚡ BIAS EVALUATION</h4>'
                    + ('<span class="tag-bullish-indicator">BULLISH</span>' if active_focus_market_matrix['last_price'] >= active_focus_market_matrix['weighted_avg_price_vwap'] else '<span class="tag-bearish-indicator">BEARISH</span>') +
                    '</div>', unsafe_allow_html=True)

# ============================================================================
# PROTOCOL 6: WORKSPACE TABS SELECTOR
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown("---")
    selected_sub_panel_focus = st.radio(
        "Workspace Environment Router",
        options=["📊 Workspace", "📐 Risk Desk", "🤖 Quant Agent"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.terminal_active_tab = selected_sub_panel_focus

    if st.session_state.terminal_active_tab == "📐 Risk Desk":
        st.markdown("#### 📐 POSITION RISK ANALYSIS")
        l_col, r_col = st.columns(2)
        with l_col:
            st.session_state.account_margin_base = st.number_input("Margin Reserves ($)", value=st.session_state.account_margin_base)
            risk_pct = st.number_input("Risk (%)", value=st.session_state.risk_allowance_percentage)
            sl_price = st.number_input("Stop Loss ($)", value=active_focus_market_matrix["last_price"] * 0.98)
            
            dist = abs(active_focus_market_matrix["last_price"] - sl_price)
            if dist > 0:
                pos_size = (st.session_state.account_margin_base * (risk_pct/100)) / dist
                st.success(f"Optimized Position: {pos_size:.4f} {resolved_active_symbol}")
        with r_col:
            st.write("📋 **ORDER LOGS**")
            for log in list(reversed(st.session_state.simulated_order_book_cache))[:5]:
                st.code(log)

    elif st.session_state.terminal_active_tab == "🤖 Quant Agent":
        st.info("🤖 **COGNITIVE QUANT AGENT** (ONLINE)")
        query = st.text_input("Ask Quant Engine...")
        if query:
            st.code(f"AGENT RESPONSE: Analyzing {resolved_active_symbol} data... Market looks steady at ${active_focus_market_matrix['last_price']}.")

    else:
        st.write(f"### 💡 SYSTEM FEED: {resolved_active_symbol}USDT")
        st.write("Live data streaming from Binance API. Chart integrated via TradingView PRO.")

    st.markdown("---")
    st.text("DELTA TERMINAL v5.0 • STATUS: ONLINE")
            
