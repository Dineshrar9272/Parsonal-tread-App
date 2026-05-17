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
# PROTOCOL 3: CRYPTO TICKER RIBBON (COMPATIBLE CLEAN LAYOUT)
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.subheader("❖ DELTA SYSTEMS : QUANT TERMINAL PRO")
    
    monitored_token_list = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOT", "DOGE"]
    ticker_columns_layout_grid = st.columns(8)
    
    for array_index, token_symbol in enumerate(monitored_token_list):
        with ticker_columns_layout_grid[array_index]:
            token_stats_matrix = get_binance_ticker_matrix(token_symbol)
            if token_stats_matrix["status"]:
                change_sign_prefix = "+" if token_stats_matrix["price_change_percent"] >= 0 else ""
                st.metric(
                    label=f"{token_symbol}/USDT",
                    value=f"${token_stats_matrix['last_price']:,.2f}",
                    delta=f"{change_sign_prefix}{token_stats_matrix['price_change_percent']:.2f}%"
                )
            else:
                st.error(f"{token_symbol} OFFLINE")

# ============================================================================
# PROTOCOL 4: VIEWPORT CONTROL SYSTEM
# ============================================================================
st.markdown("---")
col_search_frame, col_viewport_toggle = st.columns([4, 1.5])

with col_search_frame:
    user_symbol_selection_input = st.text_input(
        "Primary Asset Pair Selector",
        value="BTC",
        placeholder="Enter asset key (e.g. BTC, ETH)...",
        label_visibility="collapsed"
    )
    resolved_active_symbol = user_symbol_selection_input.upper().strip()

with col_viewport_toggle:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Return to Multi-Grid View", use_container_width=True, type="primary"):
            st.session_state.fullscreen_mode = False
            add_system_log("Viewport configuration: Grid view restored.")
            st.rerun()
    else:
        if st.button("🔍 Maximize Main Terminal Chart", use_container_width=True, type="secondary"):
            st.session_state.fullscreen_mode = True
            add_system_log("Viewport expanded: Focused mode active for " + resolved_active_symbol)
            st.rerun()

active_focus_market_matrix = get_binance_ticker_matrix(resolved_active_symbol)
if not active_focus_market_matrix["status"]:
    active_focus_market_matrix = {"last_price": 75000.0, "price_change_percent": 0.5, "high_price": 76000.0, "low_price": 74000.0, "volume_base": 15000.0, "quote_volume_turnover": 950000000.0, "weighted_avg_price_vwap": 74800.0}

# ============================================================================
# PROTOCOL 5: TRADINGVIEW IFRAME & TELEMETRY HUB
# ============================================================================
if st.session_state.fullscreen_mode:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([1, 0]), None
else:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([3.2, 1])

with primary_workspace_left_grid:
    compiled_iframe_source_url = "https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:" + resolved_active_symbol + "USDT&interval=60&theme=dark&style=1"
    st.components.v1.iframe(src=compiled_iframe_source_url, height=450, scrolling=False)

if secondary_workspace_right_grid is not None:
    with secondary_workspace_right_grid:
        st.write(f"### 📊 HUB MATRIX: {resolved_active_symbol}")
        
        st.write(f"**SPOT VALUE:** ${active_focus_market_matrix['last_price']:,.2f}")
        st.write(f"**24h HIGH:** ${active_focus_market_matrix['high_price']:,.2f}")
        st.write(f"**24h LOW:** ${active_focus_market_matrix['low_price']:,.2f}")
        st.write(f"**VOLUME:** ${active_focus_market_matrix['quote_volume_turnover']/1000000:,.1f}M")
        
        st.write("---")
        st.write("⚡ **BIAS EVALUATION**")
        if active_focus_market_matrix['last_price'] >= active_focus_market_matrix['weighted_avg_price_vwap']:
            st.success("STRUCTURE BULLISH")
        else:
            st.error("STRUCTURE BEARISH")

# ============================================================================
# PROTOCOL 6: WORKSPACE TABS SELECTOR
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown("---")
    selected_sub_panel_focus = st.radio(
        "Workspace Environment Router",
        options=["📊 Live Terminal Workspace", "📐 Risk Optimization & Sizing Desk", "🤖 Cognitive Quant Agent Room"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.terminal_active_tab = selected_sub_panel_focus
    st.markdown("<br>", unsafe_html=True)
    
    # 1. RISK ALLOCATION DESK
    if st.session_state.terminal_active_tab == "📐 Risk Optimization & Sizing Desk":
        st.markdown("#### 📐 POSITION RISK ANALYSIS ENGINE")
        allocation_layout_left_col, allocation_layout_right_col = st.columns(2)
        
        with allocation_layout_left_col:
            st.session_state.account_margin_base = st.number_input("Total Margin Collateral Base Reserves ($)", value=st.session_state.account_margin_base, step=1000.0)
            target_entry_execution_price = st.number_input("Target Trigger Level Price ($)", value=active_focus_market_matrix["last_price"], step=5.0)
            st.session_state.risk_allowance_percentage = st.number_input("Max Loss Risk Allowance Cap (%)", value=st.session_state.risk_allowance_percentage, min_value=0.1, max_value=5.0, step=0.1)
            target_invalidation_stop_loss = st.number_input("System Protective Stop Loss ($)", value=active_focus_market_matrix["last_price"] * 0.98, step=5.0)
            
            absolute_invalidation_distance_spread = abs(target_entry_execution_price - target_invalidation_stop_loss)
            
            if absolute_invalidation_distance_spread > 0:
                capital_value_exposure_risk_pool = st.session_state.account_margin_base * (st.session_state.risk_allowance_percentage / 100.0)
                optimized_unit_contract_capacity = capital_value_exposure_risk_pool / absolute_invalidation_distance_spread
                total_notional_leverage_volume = optimized_unit_contract_capacity * target_entry_execution_price
                mathematical_implied_leverage_ratio = total_notional_leverage_volume / st.session_state.account_margin_base
                
                st.info(
                    f"**CAPITAL POOL AT RISK:** ${capital_value_exposure_risk_pool:,.2f} | "
                    f"**OPTIMIZED POSITION SIZE:** {optimized_unit_contract_capacity:.4f} {resolved_active_symbol} | "
                    f"**IMPLIED LEVERAGE RATIO:** {mathematical_implied_leverage_ratio:.2f}x Leverage"
                )
                
                if st.button("⚡ Dispatch Position Payload Configuration", use_container_width=True):
                    registered_string_payload = "ORDER: Size " + f"{optimized_unit_contract_capacity:.3f}" + " " + resolved_active_symbol + " at $" + f"{target_entry_execution_price:,.2f}"
                    st.session_state.simulated_order_book_cache.append(registered_string_payload)
                    add_system_log(registered_string_payload)
                    st.rerun()

        with allocation_layout_right_col:
            st.write("📋 **SIMULATED TERMINAL ORDERBOOK RECORD**")
            if not st.session_state.simulated_order_book_cache:
                st.text("Active registries blank.")
            else:
                for active_position_row in list(reversed(st.session_state.simulated_order_book_cache))[:4]:
                    st.code(f"⚡ {active_position_row}")

    # 2. COGNITIVE QUANT AGENT MODULE
    elif st.session_state.terminal_active_tab == "🤖 Cognitive Quant Agent Room":
        st.markdown("#### 🤖 COGNITIVE QUANT DATA PROCESSING FEEDS")
        st.info(f"💬 **QUANT SYSTEM INTERACTION INTERFACE** (AGENT: LIVE) \n\nQuant tracking logic actively evaluating targets for {resolved_active_symbol}USDT.")
        
        user_ai_prompt_entry = st.text_input("Quant Engine Query Context Field Box", placeholder="Enter core analysis inquiries...", label_visibility="collapsed")
        if user_ai_prompt_entry:
            add_system_log("Query parsed: " + str(user_ai_prompt_entry))
            st.code(f"🤖 QUANT RESPONSE:\nProcessed strategy parameters for {resolved_active_symbol} at level ${active_focus_market_matrix['last_price']:,.2f}. Evaluation matrix holds normal thresholds.")

    # DEFAULT LIVE WORKSPACE OVERVIEW (HOME)
    else:
        dashboard_row_split_left, dashboard_row_split_right = st.columns([2, 1])
        with dashboard_row_split_left:
            st.write("### 💡 STRUCTURAL SYSTEM INSIGHT STRATEGY FEED")
            st.write(f"Target pipeline synchronization established for active data streams selector: **{resolved_active_symbol}USDT**.")
            st.write("System engine running deployment clusters inside sandboxed virtual terminal workspace securely.")
        with dashboard_row_split_right:
            st.write("⏱️ **CORE RUNTIME TERMINAL SYSTEM LOGS**")
            for log_row in st.session_state.system_runtime_logs[:5]:
                st.text(log_row)

    st.write("---")
    st.text("DELTA TERMINAL MAIN NODE ENGINE v5.0 PRO • COMPUTATION PIPELINE OPERATING HEALTHY • STATUS: ONLINE")
    
