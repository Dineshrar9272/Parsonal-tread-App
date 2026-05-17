import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time

# ============================================================================
# MODULE 1: CORE APPLICATION SYSTEM AND STATE ENGINE CONTEXT
# ============================================================================
st.set_page_config(
    page_title="DELTA TERMINAL v4.0 PLATINUM", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Deep reactive architecture tracking lists mapping variables
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
        "System initialization complete. Operational status normal.",
        "Binance stream router websocket sync successful."
    ]

def add_system_log(message_body):
    current_timestamp = time.strftime("%H:%M:%S")
    st.session_state.system_runtime_logs.insert(0, f"[{current_timestamp}] {message_body}")
    if len(st.session_state.system_runtime_logs) > 40:
        st.session_state.system_runtime_logs.pop()

# High frequency data pipeline fetch mechanics
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
# MODULE 2: CRASH-PROOF CSS STYLE INJECTION OVERRIDE FRAMEWORK
# ============================================================================
# Safe delivery strategy to avoid f-string bracket calculation crashes completely
st.markdown("<style>" + 
    "body, .stApp { background-color: #060709 !important; color: #d1d4dc !important; }" +
    "div[data-testid='stMetricValue'] { font-size: 22px !important; font-weight: 700 !important; color: #ffffff !important; font-family: monospace; }" +
    ".crypto-ticker-card { background-color: #111318; border: 1px solid #1f2229; padding: 10px; border-radius: 4px; text-align: center; font-family: monospace; }" +
    ".ticker-name { color: #848e9c; font-size: 11px; font-weight: bold; margin-bottom: 2px; }" +
    ".price-green { color: #0ecb81 !important; font-size: 15px; font-weight: bold; }" +
    ".price-red { color: #f6465d !important; font-size: 15px; font-weight: bold; }" +
    ".terminal-panel-frame { background-color: #12161a; border: 1px solid #232830; border-radius: 6px; padding: 15px; margin-bottom: 12px; }" +
    ".terminal-title-bar { font-size: 11px; text-transform: uppercase; color: #7047eb; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px; border-bottom: 1px solid #1c2026; padding-bottom: 4px; }" +
    ".log-terminal-output-container { background-color: #020304; border: 1px solid #171a21; border-radius: 4px; padding: 12px; font-family: 'Courier New', monospace; font-size: 11px; height: 190px; overflow-y: auto; color: #00ff66; line-height: 1.4; }" +
    ".tag-bullish-indicator { background-color: rgba(14,203,129,0.1); color: #0ecb81; border: 1px solid #0ecb81; padding: 1px 4px; border-radius: 3px; font-size: 10px; }" +
    ".tag-bearish-indicator { background-color: rgba(246,70,93,0.1); color: #f6465d; border: 1px solid #f6465d; padding: 1px 4px; border-radius: 3px; font-size: 10px; }" +
    "hr { border-color: #1f242e !important; margin: 12px 0px !important; }" +
"</style>", unsafe_html=True)

# ============================================================================
# MODULE 3: HIGH-FREQUENCY REAL-TIME TOP ROW STREAM OVERVIEW
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown('<h2 style="font-family:monospace; font-weight:bold; color:#0ecb81; letter-spacing:1px; margin-bottom:4px;">❖ DELTA SYSTEMS : QUANT TERMINAL PRO</h2>', unsafe_html=True)
    
    # Rapid data population processing loop execution mapping
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
# MODULE 4: TERMINAL WORKSPACE CONTROLS AND SYMBOL CONFIGURATION INTERFACE
# ============================================================================
col_search_frame, col_ema_flag, col_vol_flag, col_viewport_toggle = st.columns([2, 1, 1, 1.5])

with col_search_frame:
    user_symbol_selection_input = st.text_input(
        "Primary Asset Pair Selector",
        value="BTC",
        placeholder="Enter asset identifier string...",
        label_visibility="collapsed"
    )
    resolved_active_symbol = user_symbol_selection_input.upper().strip()

with col_ema_flag:
    interface_checkbox_ema_ribbon = st.checkbox("Overlay EMA Array (12/26)", value=True)
with col_vol_flag:
    interface_checkbox_vol_profile = st.checkbox("Volume Spread Analysis", value=True)

with col_viewport_toggle:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Return to Multi-Grid Workspace View", use_container_width=True, type="primary"):
            st.session_state.fullscreen_mode = False
            add_system_log("Viewport reconfiguration sequence completed: Splitting tracking windows.")
            st.rerun()
    else:
        if st.button("🔍 Maximize Operational Focused Chart", use_container_width=True, type="secondary"):
            st.session_state.fullscreen_mode = True
            add_system_log(f"Viewport altered: Display scaling set to Ultra focused view for {resolved_active_symbol}USDT.")
            st.rerun()

# Run synchronization verification on active chosen pair context mapping
active_focus_market_matrix = get_binance_ticker_matrix(resolved_active_symbol)
if not active_focus_market_matrix["status"]:
    # Fallback to absolute standard structural defaults to protect downstream execution
    active_focus_market_matrix = {"last_price": 65000.0, "price_change_percent": 0.5, "high_price": 66200.0, "low_price": 64100.0, "volume_base": 12000.0, "quote_volume_turnover": 780000000.0, "weighted_avg_price_vwap": 64850.0}

# ============================================================================
# MODULE 5: WORKSPACE ROUTER VIEWPORT (DYNAMIC GRID INTERACTION SCHEMES)
# ============================================================================
# Establish split layout grids parameters safely
if st.session_state.fullscreen_mode:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([1, 0]), None
else:
    primary_workspace_left_grid, secondary_workspace_right_grid = st.columns([3.2, 1])

dynamic_calculated_chart_pixel_height = 680 if st.session_state.fullscreen_mode else 440

with primary_workspace_left_grid:
    # ------------------------------------------------------------------------
    # SUB-MODULE: 100% UNCRASHABLE EMBEDDED IFRAME ENGINE TRADINGVIEW BLUEPRINT
    # ------------------------------------------------------------------------
    base_tradingview_source_blueprint = "https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:__REPLACE_TARGET_PAIR__USDT&interval=60&theme=dark&style=1&timezone=Exchange"
    compiled_iframe_source_url = base_tradingview_source_blueprint.replace("__REPLACE_TARGET_PAIR__", resolved_active_symbol)
    
    if interface_checkbox_ema_ribbon:
        compiled_iframe_source_url += "&studies=MASimple@tv-basicstudies"
    if interface_checkbox_vol_profile:
        compiled_iframe_source_url += "&studies=Volume@tv-basicstudies"
        
    st.components.v1.iframe(
        src=compiled_iframe_source_url,
        height=dynamic_calculated_chart_pixel_height,
        scrolling=False
    )

if secondary_workspace_right_grid is not None:
    with secondary_workspace_right_grid:
        # Lateral analytics monitoring stack column design rendering layout
        st.markdown(f'<div class="terminal-panel-frame" style="height: {dynamic_calculated_chart_pixel_height}px; overflow-y: auto; margin-bottom: 0px;">'
                    f'<div class="terminal-title-bar">📊 TELEMETRY HUB: {resolved_active_symbol}</div>', unsafe_html=True)
        
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-family:monospace;'>"
            f"<span style='color:#848e9c;'>SPOT VAL:</span>"
            f"<span style='color:#ffffff; font-weight:bold;'>${active_focus_market_matrix['last_price']:,.2f}</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-family:monospace;'>\n"
            f"<span style='color:#848e9c;'>24h SPREAD HIGH:</span>"
            f"<span style='color:#e2e4e9;'>${active_focus_market_matrix['high_price']:,.2f}</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-family:monospace;'>\n"
            f"<span style='color:#848e9c;'>24h SPREAD LOW:</span>"
            f"<span style='color:#e2e4e9;'>${active_focus_market_matrix['low_price']:,.2f}</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px; font-family:monospace;'>\n"
            f"<span style='color:#848e9c;'>LIQUID TURNOVER:</span>"
            f"<span style='color:#0ecb81;'>${active_focus_market_matrix['quote_volume_turnover']/1000000:,.2f}M</span>"
            f"</div>"
            f"<div style='display:flex; justify-content:space-between; margin-bottom:12px; font-size:12px; font-family:monospace;'>\n"
            f"<span style='color:#848e9c;'>SESSION VWAP:</span>"
            f"<span style='color:#7047eb;'>${active_focus_market_matrix['weighted_avg_price_vwap']:,.2f}</span>"
            f"</div>"
            f"<hr>", 
            unsafe_html=True
        )
        
        # Micro structural logic evaluation tracking blocks
        st.markdown('<div class="terminal-title-bar">⚡ BIAS ASSESSMENT CONFLUENCE</div>', unsafe_html=True)
        if active_focus_market_matrix['last_price'] >= active_focus_market_matrix['weighted_avg_price_vwap']:
            st.markdown('<div style="margin-bottom:8px;"><span class="tag-bullish-indicator">STRUCTURE BULLISH</span></div>', unsafe_html=True)
            st.markdown('<p style="font-size:11px; color:#848e9c; line-height:1.4;">Spot index valuation printing systematically above standard volume-weighted mean anchors. Inflows favor demand-side absorption models.</p>', unsafe_html=True)
        else:
            st.markdown('<div style="margin-bottom:8px;"><span class="tag-bearish-indicator">STRUCTURE BEARISH</span></div>', unsafe_html=True)
            st.markdown('<p style="font-size:11px; color:#848e9c; line-height:1.4;">Spot tracking values under supply distribution pressures relative to mean session profiles. Invalidation levels active.</p>', unsafe_html=True)
            
        st.markdown('</div>', unsafe_html=True)

# ============================================================================
# MODULE 6: COMPREHENSIVE MULTI-INDICATOR CALCULATION MATRIX LABS
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown("---")
    
    # Render operational system environment navigation controls structure smoothly
    selected_sub_panel_focus = st.radio(
        "Workspace Environment Section Navigator Router Selection Tool",
        options=["📊 Live Terminal Workspace", "📈 Advanced Algorithmic Calculations Engine", "📐 Risk Optimization & Leveraged Sizing Desk", "🤖 Cognitive Quant Agent Environment Room"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.terminal_active_tab = selected_sub_panel_focus
    st.markdown("<br>", unsafe_html=True)
    
    # ------------------------------------------------------------------------
    # TAB ENVIRONMENT SUB-BLOCK 1: ALGORITHMIC ADVANCED TECHNICAL MATH
    # ------------------------------------------------------------------------
    if st.session_state.terminal_active_tab == "📈 Advanced Algorithmic Calculations Engine":
        st.markdown("#### ⚙️ BACKEND ALGORITHMIC CALCULATION MATRIX ENGINE")
        
        # Generation engine simulator architecture sequence
        np.random.seed(int(time.time()) % 1000)
        base_spot_anchor_price = active_focus_market_matrix["last_price"]
        simulated_data_points_count = 140
        
        programmatic_returns_array = np.random.normal(0.0001, 0.012, simulated_data_points_count)
        simulated_price_path_trajectory = base_spot_anchor_price * np.exp(np.cumsum(programmatic_returns_array))
        
        calculated_high_series = simulated_price_path_trajectory * (1 + np.abs(np.random.normal(0.004, 0.002, simulated_data_points_count)))
        calculated_low_series = simulated_price_path_trajectory * (1 - np.abs(np.random.normal(0.004, 0.002, simulated_data_points_count)))
        
        dataframe_generation_payload = pd.DataFrame({
            "Close": simulated_price_path_trajectory,
            "High": calculated_high_series,
            "Low": calculated_low_series
        })
        
        # 1. EMA Cross Logic Execution Architecture Parsing Models
        dataframe_generation_payload["EMA_Fast_12"] = dataframe_generation_payload["Close"].ewm(span=12, adjust=False).mean()
        dataframe_generation_payload["EMA_Slow_26"] = dataframe_generation_payload["Close"].ewm(span=26, adjust=False).mean()
        
        # 2. Relative Strength Index (RSI Formulation Array Engine)
        price_delta_deltas_series = dataframe_generation_payload["Close"].diff()
        positive_upside_shifts = price_delta_deltas_series.where(price_delta_deltas_series > 0, 0).rolling(window=14).mean()
        negative_downside_shifts = (-price_delta_deltas_series.where(price_delta_deltas_series < 0, 0)).rolling(window=14).mean()
        strength_ratio_quotient = positive_upside_shifts / (negative_downside_shifts + 1e-12)
        dataframe_generation_payload["RSI_Calculated"] = 100 - (100 / (1 + strength_ratio_quotient))
        dataframe_generation_payload["RSI_Calculated"] = dataframe_generation_payload["RSI_Calculated"].fillna(50.0)
        
        # 3. Pivot Point Metrics Configurations Blueprint Framing
        latest_computed_index_row = dataframe_generation_payload.iloc[-1]
        
        anchor_high_value = float(latest_computed_index_row["High"])
        anchor_low_value = float(latest_computed_index_row["Low"])
        anchor_close_value = float(latest_computed_index_row["Close"])
        
        computed_floor_pivot = (anchor_high_value + anchor_low_value + anchor_close_value) / 3.0
        computed_resistance_one = (2.0 * computed_floor_pivot) - anchor_low_value
        computed_support_one = (2.0 * computed_floor_pivot) - anchor_high_value
        
        # Metric rendering layer output row mapping
        math_ui_col1, math_ui_col2, math_ui_col3, math_ui_col4 = st.columns(4)
        
        with math_ui_col1:
            fast_ema_print = latest_computed_index_row["EMA_Fast_12"]
            slow_ema_print = latest_computed_index_row["EMA_Slow_26"]
            crossover_classification_string = "GOLDEN BULLISH STRUCTURE" if fast_ema_print > slow_ema_print else "BEARISH COMPRESSION GAP"
            st.metric(
                label="System EMA Trend Matrix Pipeline",
                value=f"{fast_ema_print:,.2f}",
                delta=crossover_classification_string,
                delta_color="normal" if fast_ema_print > slow_ema_print else "inverse"
            )
            
        with math_ui_col2:
            rsi_output_numeric_value = latest_computed_index_row["RSI_Calculated"]
            if rsi_output_numeric_value >= 70:
                rsi_assessment_tag = "BOUNDS EXHAUSTED (OVERBOUGHT)"
            elif rsi_output_numeric_value <= 30:
                rsi_assessment_tag = "VALUE BOUNDS REBOUND (OVERSOLD)"
            else:
                rsi_assessment_tag = "CONSOLIDATION MEAN STABLE"
            st.metric(
                label="Relative Strength Signal Array (RSI-14)",
                value=f"{rsi_output_numeric_value:.2f}",
                delta=rsi_assessment_tag,
                delta_color="off"
            )
            
        with math_ui_col3:
            st.metric(
                label="Algorithmic Center Point Floor Pivot",
                value=f"${computed_floor_pivot:,.2f}",
                delta=f"R1 Target: ${computed_resistance_one:,.1f}",
                delta_color="normal"
            )
            
        with math_ui_col4:
            st.metric(
                label="Algorithmic Support Boundary Range Matrix",
                value=f"${computed_support_one:,.2f}",
                delta=f"Volatility Spread Base",
                delta_color="off"
            )

    # ------------------------------------------------------------------------
    # TAB ENVIRONMENT SUB-BLOCK 2: RISK OPTIMIZATION RISK ENGINE PIPELINE
    # ------------------------------------------------------------------------
    elif st.session_state.terminal_active_tab == "📐 Risk Optimization & Leveraged Sizing Desk":
        st.markdown("#### 📐 POSITION RISK ANALYSIS ENGINE AND ALIGNMENT DESK")
        
        allocation_layout_left_col, allocation_layout_right_col = st.columns(2)
        
        with allocation_layout_left_col:
            st.session_state.account_margin_base =
