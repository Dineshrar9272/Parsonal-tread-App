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
    if len(st.session_state.system_runtime_logs) > 30:
        st.session_state.system_runtime_logs.pop()

@st.cache_data(ttl=3)
def get_binance_ticker_matrix(ticker_symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={ticker_symbol}USDT"
        response_payload = requests.get(url, timeout=2).json()
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
# PROTOCOL 2: CLEAN CSS INJECTION
# ============================================================================
custom_css = """
<style>
    body, .stApp { background-color: #060709 !important; color: #d1d4dc !important; }
    div[data-testid='stMetricValue'] { font-size: 22px !important; font-weight: 700 !important; color: #ffffff !important; font-family: monospace; }
    .crypto-ticker-card { background-color: #111318; border: 1px solid #1f2229; padding: 10px; border-radius: 4px; text-align: center; font-family: monospace; }
    .ticker-name { color: #848e9c; font-size: 11px; font-weight: bold; margin-bottom: 2px; }
    .price-green { color: #0ecb81 !important; font-size: 15px; font-weight: bold; }
    .price-red { color: #f6465d !important; font-size: 15px; font-weight: bold; }
    .terminal-panel-frame { background-color: #12161a; border: 1px solid #232830; border-radius: 6px; padding: 15px; margin-bottom: 12px; }
    .terminal-title-bar { font-size: 11px; text-transform: uppercase; color: #7047eb; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px; border-bottom: 1px solid #1c2026; padding-bottom: 4px; }
    .log-terminal-output-container { background-color: #020304; border: 1px solid #171a21; border-radius: 4px; padding: 12px; font-family: 'Courier New', monospace; font-size: 11px; height: 180px; overflow-y: auto; color: #00ff66; line-height: 1.4; }
    .tag-bullish-indicator { background-color: rgba(14,203,129,0.1); color: #0ecb81; border: 1px solid #0ecb81; padding: 1px 4px; border-radius: 3px; font-size: 10px; }
    .tag-bearish-indicator { background-color: rgba(246,70,93,0.1); color: #f6465d; border: 1px solid #f6465d; padding: 1px 4px; border-radius: 3px; font-size: 10px; }
    hr { border-color: #1f242e !important; margin: 12px 0px !important; }
</style>
"""
st.markdown(custom_css, unsafe_html=True)

# ============================================================================
# PROTOCOL 3: CRYPTO TICKER RIBBON
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown('<h2 style="font-family:monospace; font-weight:bold; color:#0ecb81; margin-bottom:4px;">❖ DELTA SYSTEMS : QUANT TERMINAL PRO</h2>', unsafe_html=True)
    
    monitored_token_list = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOT", "DOGE"]
    ticker_columns_layout_grid = st.columns(8)
    
    for array_index, token_symbol in enumerate(monitored_token_list):
        with ticker_columns_layout_grid[array_index]:
            token_stats_matrix = get_binance_ticker_matrix(token_symbol)
            if token_stats_matrix["status"]:
                color_class_assignment = "price-green" if token_stats_matrix["price_change_percent"] >= 0 else "price-red"
                change_sign_prefix = "+" if token_stats_matrix["price_change_percent"] >= 0 else ""
                st.markdown(
                    f'<div class="crypto-ticker-card">'
                    f'<div class="ticker-name">{token_symbol}/USDT</div>'
                    f'<div class="{color_class_assignment}">${token_stats_matrix["last_price"]:,.2f}</div>'
                    f'<div class="{color_class_assignment}" style="font-size:11px;">{change_sign_prefix}{token_stats_matrix["price_change_percent"]:.2f}%</div>'
                    f'</div>', 
                    unsafe_html=True
                )
            else:
                st.markdown(f'<div class="crypto-ticker-card"><div class="ticker-name">{token_symbol}</div><div style="color:#e05638;">OFFLINE</div></div>', unsafe_html=True)
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_html=True)

# ============================================================================
# PROTOCOL 4: VIEWPORT CONTROL SYSTEM
# ============================================================================
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
            add_system_log("Viewport configuration sequence completed: Grid view restored.")
            st.rerun()
    else:
        if st.button("🔍 Maximize Main Terminal Chart", use_container_width=True, type="secondary"):
            st.session_state.fullscreen_mode = True
            add_system_log(f"Viewport expanded: Focused mode active for {resolved_active_symbol}USDT.")
            st.rerun()

active_focus_market_matrix = get_binance_ticker_matrix(resolved_active_symbol)
if not active_focus_market_matrix["status"]:
    active_focus_market_matrix = {"last_price": 65000.0, "price_change_percent": 0.5, "high_price": 66200.0, "low_price": 64100.0, "volume_base": 12000.0, "quote_volume_turnover": 780000000.0, "weighted_avg_price_vwap": 64850.0}

# ============================================================================
# PROTOCOL 5: TRADINGVIEW IFRAME & TELEMETRY HUB
# ============================================================================
if st.session_state.fullscreen_mode:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([1, 0]), None
else:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([3.2, 1])

dynamic_calculated_chart_pixel_height = 430

with primary_workspace_left_grid:
    compiled_iframe_source_url = f"https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:{resolved_active_symbol}USDT&interval=60&theme=dark&style=1&timezone=Exchange"
    st.components.v1.iframe(
        src=compiled_iframe_source_url,
        height=dynamic_calculated_chart_pixel_height,
        scrolling=False
    )

if secondary_workspace_right_grid is not None:
    with secondary_workspace_right_grid:
        st.markdown(f'<div class="terminal-panel-frame" style="height: {dynamic_calculated_chart_pixel_height}px; overflow-y: auto; margin-bottom: 0px;">'
                    f'<div class="terminal-title-bar">📊 HUB MATRIX: {resolved_active_symbol}</div>', unsafe_html=True)
        
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-family:monospace;'>"
            f"<span style='color:#848e9c;'>SPOT VALUE:</span>"
            f"<span style='color:#ffffff; font-weight:bold;'>${active_focus_market_matrix['last_price']:,.2f}</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-family:monospace;'>"
            f"<span style='color:#848e9c;'>24h HIGH:</span>"
            f"<span style='color:#e2e4e9;'>${active_focus_market_matrix['high_price']:,.2f}</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-family:monospace;'>"
            f"<span style='color:#848e9c;'>24h LOW:</span>"
            f"<span style='color:#e2e4e9;'>${active_focus_market_matrix['low_price']:,.2f}</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-family:monospace;'>"
            f"<span style='color:#848e9c;'>TURNOVER:</span>"
            f"<span style='color:#0ecb81;'>${active_focus_market_matrix['quote_volume_turnover']/1000000:,.2f}M</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:12px; font-size:12px; font-family:monospace;'>"
            f"<span style='color:#848e9c;'>VWAP MEAN:</span>"
            f"<span style='color:#7047eb;'>${active_focus_market_matrix['weighted_avg_price_vwap']:,.2f}</span>"
            f"</div>"
            f"<hr>", 
            unsafe_html=True
        )
        
        st.markdown('<div class="terminal-title-bar">⚡ BIAS EVALUATION</div>', unsafe_html=True)
        if active_focus_market_matrix['last_price'] >= active_focus_market_matrix['weighted_avg_price_vwap']:
            st.markdown('<div style="margin-bottom:8px;"><span class="tag-bullish-indicator">STRUCTURE BULLISH</span></div>', unsafe_html=True)
        else:
            st.markdown('<div style="margin-bottom:8px;"><span class="tag-bearish-indicator">STRUCTURE BEARISH</span></div>', unsafe_html=True)
            
        st.markdown('</div>', unsafe_html=True)

# ============================================================================
# PROTOCOL 6: WORKSPACE TABS SELECTOR
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown("---")
    
    selected_sub_panel_focus = st.radio(
        "Workspace Environment Router",
        options=["📊 Live Terminal Workspace", "📈 Advanced Algorithmic Calculations Engine", "📐 Risk Optimization & Leveraged Sizing Desk", "🤖 Cognitive Quant Agent Environment Room"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.terminal_active_tab = selected_sub_panel_focus
    st.markdown("<br>", unsafe_html=True)
    
    # 1. ADVANCED TECHNICALS ENGINE
    if st.session_state.terminal_active_tab == "📈 Advanced Algorithmic Calculations Engine":
        st.markdown("#### ⚙️ BACKEND ALGORITHMIC CALCULATION MATRIX ENGINE")
        
        np.random.seed(int(time.time()) % 1000)
        base_spot_anchor_price = active_focus_market_matrix["last_price"]
        simulated_data_points_count = 100
        
        programmatic_returns_array = np.random.normal(0.0001, 0.01, simulated_data_points_count)
        simulated_price_path_trajectory = base_spot_anchor_price * np.exp(np.cumsum(programmatic_returns_array))
        
        dataframe_generation_payload = pd.DataFrame({"Close": simulated_price_path_trajectory})
        dataframe_generation_payload["EMA_Fast"] = dataframe_generation_payload["Close"].ewm(span=12, adjust=False).mean()
        dataframe_generation_payload["EMA_Slow"] = dataframe_generation_payload["Close"].ewm(span=26, adjust=False).mean()
        
        latest_computed_index_row = dataframe_generation_payload.iloc[-1]
        
        math_ui_col1, math_ui_col2 = st.columns(2)
        with math_ui_col1:
            fast_delta_string = "Bullish Cross" if latest_computed_index_row['EMA_Fast'] > latest_computed_index_row['EMA_Slow'] else "Bearish Drop"
            st.metric(
                label="Algorithmic Fast Trend Line (EMA-12)",
                value=f"${latest_computed_index_row['EMA_Fast']:,.2f}",
                delta=fast_delta_string
            )
        with math_ui_col2:
            st.metric(
                label="Baseline Slow Support Structure (EMA-26)",
                value=f"${latest_computed_index_row['EMA_Slow']:,.2f}"
            )

    # 2. RISK ALLOCATION ENGINE
    elif st.session_state.terminal_active_tab == "📐 Risk Optimization & Leveraged Sizing Desk":
        st.markdown("#### 📐 POSITION RISK ANALYSIS ENGINE AND ALIGNMENT DESK")
        
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
                
                st.markdown(
                    f'<div style="background-color:#0b0d12; border:1px dashed #2d323f; padding:12px; border-radius:4px; font-family:monospace; font-size:12px; margin-top:10px;">'
                    f'<span style="color:#848e9c;">CAPITAL POOL AT MAXIMUM RISK  :</span> <span style="color:#f6465d; font-weight:bold;">${capital_value_exposure_risk_pool:,.2f}</span><br>'
                    f'<span style="color:#848e9c;">OPTIMIZED CONTRACT UNIT SIZE   :</span> <span style="color:#0ecb81; font-weight:bold;">{optimized_unit_contract_capacity:.4f} {resolved_active_symbol}</span><br>'
                    f'<span style="color:#848e9c;">NOTIONAL VALUE VALUE BRACKET  :</span> <span style="color:#ffffff; font-weight:bold;">${total_notional_leverage_volume:,.2f}</span><br>'
                    f'<span style="color:#848e9c;">IMPLIED CALCULATED LEVERAGE RATIO:</span> <span style="color:#7047eb; font-weight:bold;">{mathematical_implied_leverage_ratio:.2f}x Leverage</span>'
                    f'</div>',
                    unsafe_html=True
                )
                
                if st.button("⚡ Dispatch Position Payload Configuration to Logs", use_container_width=True):
                    registered_string_payload = f"ORDER DEPLOYED: Size {optimized_unit_contract_capacity:.3f} {resolved_active_symbol} at ${target_entry_execution_price:,.2f}"
                    st.session_state.simulated_order_book_cache.append(registered_string_payload)
                    add_system_log(f"Risk verification clear: {registered_string_payload}")
                    st.rerun()
            else:
                st.error("Execution parameters mismatch. Target Entry price must be different from Stop Loss boundary.")
                
        with allocation_layout_right_col:
            st.markdown('<div class="terminal-panel-frame" style="min-height:220px;">'
                        '<div class="terminal-title-bar">📋 SIMULATED TERMINAL ORDERBOOK RECORD</div>', unsafe_html=True)
            if not st.session_state.simulated_order_book_cache:
                st.markdown('<div style="text-align:center; padding:40px 10px; color:#5e6673; font-family:monospace; font-size:11px;">Active registries blank.</div>', unsafe_html=True)
            else:
                for active_position_row in list(reversed(st.session_state.simulated_order_book_cache))[:4]:
                    st.markdown(f'<div style="background-color:#07080b; border:1px solid #171b24; padding:6px; border-radius:3px; font-family:monospace; font-size:11px; margin-bottom:4px; color:#e2e4e9;">⚡ {active_position_row}</div>', unsafe_html=True)
                if st.button("Clear Log Matrices", use_container_width=True):
                    st.session_state.simulated_order_book_cache = []
                    add_system_log("Position simulation records cache cleared successfully.")
                    st.rerun()
            st.markdown('</div>', unsafe_html=True)

    # 3. COGNITIVE QUANT AGENT MODULE (FIXED ERROR STRINGS & CONDITIONS HERE)
    elif st.session_state.terminal_active_tab == "🤖 Cognitive Quant Agent Environment Room":
        st.markdown("#### 🤖 COGNITIVE QUANT DATA PROCESSING FEEDS")
        st.markdown(f'<div class="terminal-panel-frame">'
                    f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">'
                    f'<span style="color:#7047eb; font-weight:bold; font-size:12px; font-family:monospace;">💬 CORE SYSTEM INTERACTION INTERFACE</span>'
                    f'<span class="tag-bullish-indicator">AGENT: LIVE</span>'
                    f'</div>'
                    f'<p style="font-size:12px; color:#b7bdc6; line-height:1.5; margin:0px;">Quant tracking logic actively evaluating telemetry targets for <b>{resolved_active_symbol}USDT</b>.</p>'
                    f'</div>', unsafe_html=True)
        
        user_ai_prompt_entry = st.text_input("Quant Engine Query Context Field Box", placeholder="Enter core analysis inquiries...", label_visibility="collapsed")
        
        if user_ai_prompt_entry:
            add_system_log(f"Telemetry query parsed: {user_ai_prompt_entry}")
            response_html = f'<div style="background-color:#020304; border:1px solid #7047eb; padding:12px; border-radius:4px; font-family:monospace; font-size:12px; color:#e2e4e9; margin-top:8px;"><b style="color:#7047eb;">🤖 QUANT ENGINE RESPONSE:</b><br>Processed strategy context parameters for asset identifier {resolved_active_symbol} at terminal index level ${active_focus_market_matrix["last
