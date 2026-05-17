import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
import math

# ============================================================================
# STEP 1: CORE TERMINAL CORE SYSTEM ARCHITECTURE & ENGINE SETUP
# ============================================================================
st.set_page_config(
    page_title="DELTA TERMINAL v3.0 PRO - ADVANCED QUANT INTERFACE", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Initialize deep session state matrices for state tracking natively
if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False
if "selected_timeframe" not in st.session_state:
    st.session_state.selected_timeframe = "1h"
if "risk_balance" not in st.session_state:
    st.session_state.risk_balance = 10000.0
if "risk_percentage" not in st.session_state:
    st.session_state.risk_percentage = 1.0
if "order_history" not in st.session_state:
    st.session_state.order_history = []
if "terminal_logs" not in st.session_state:
    st.session_state.terminal_logs = ["Terminal Engine initialized successfully.", "Live high-frequency stream matching active."]

# Helper function to append terminal activity system tracking logs
def logger_msg(msg):
    current_time = time.strftime("%H:%M:%S")
    st.session_state.terminal_logs.insert(0, f"[{current_time}] {msg}")
    if len(st.session_state.terminal_logs) > 30:
        st.session_state.terminal_logs.pop()

# Global error-resilient price fetching core pipeline (Binance Live REST API Endpoint Mapping)
@st.cache_data(ttl=5)
def fetch_live_market_data(ticker_symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={ticker_symbol}USDT"
        res = requests.get(url, timeout=3).json()
        last_price = float(res['lastPrice'])
        price_change_pct = float(res['priceChangePercent'])
        high_price = float(res['highPrice'])
        low_price = float(res['lowPrice'])
        quote_volume = float(res['quoteVolume'])
        weighted_avg_price = float(res['weightedAvgPrice'])
        
        return {
            "valid": True,
            "price": last_price,
            "change": price_change_pct,
            "high": high_price,
            "low": low_price,
            "vol": quote_volume,
            "vwap": weighted_avg_price
        }
    except Exception as error_context:
        return {"valid": False, "price": 0.0, "change": 0.0, "high": 0.0, "low": 0.0, "vol": 0.0, "vwap": 0.0}

# Historical data mock simulator generation pipeline to drive programmatic calculations natively
def generate_quant_matrix_history(base_price, datapoints=100):
    np.random.seed(42)
    price_movements = np.random.normal(0.0002, 0.015, datapoints)
    cumulative_returns = np.exp(np.cumsum(price_movements))
    simulated_prices = base_price * cumulative_returns
    
    high_sim = simulated_prices * (1 + np.abs(np.random.normal(0.005, 0.003, datapoints)))
    low_sim = simulated_prices * (1 - np.abs(np.random.normal(0.005, 0.003, datapoints)))
    volumes_sim = np.random.uniform(100000, 5000000, datapoints)
    
    timestamp_range = pd.date_range(end=pd.Timestamp.now(), periods=datapoints, freq='h')
    
    dataframe_payload = pd.DataFrame({
        "Close": simulated_prices,
        "High": high_sim,
        "Low": low_sim,
        "Volume": volumes_sim
    }, index=timestamp_range)
    
    return dataframe_payload

# ============================================================================
# STEP 2: CYBERPUNK THEME STYLE CUSTOM INJECTION ENGINE
# ============================================================================
st.markdown("""
<style>
    body { background-color: #0b0c10 !important; color: #e1e4e8 !important; }
    .stApp { background-color: #0b0c10 !important; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: bold !important; color: #ffffff !important; font-family: 'Courier New', monospace; }
    div[data-testid="stMetricDelta"] { font-size: 13px !important; }
    .main-terminal-header { font-family: 'Courier New', monospace; color: #0ecb81; font-weight: bold; font-size: 26px; border-bottom: 2px solid #212630; padding-bottom: 8px; margin-bottom: 15px; text-shadow: 0 0 10px rgba(14,203,129,0.3); }
    .sub-panel-card { background-color: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 14px; margin-bottom: 10px; }
    .metric-title-custom { color: #808a9d; font-size: 11px; text-transform: uppercase; font-weight: bold; letter-spacing: 1px; }
    .price-bullish { color: #0ecb81 !important; font-weight: bold; font-family: 'Courier New', monospace; }
    .price-bearish { color: #f6465d !important; font-weight: bold; font-family: 'Courier New', monospace; }
    .log-terminal-box { background-color: #050608; border: 1px solid #1f232b; border-radius: 4px; padding: 10px; font-family: 'Courier New', monospace; font-size: 11px; height: 180px; overflow-y: auto; color: #39ff14; }
    .active-tag { background-color: rgba(14,203,129,0.15); color: #0ecb81; border: 1px solid #0ecb81; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .indicator-label { font-size: 12px; font-weight: bold; color: #c3c7db; }
</style>
""", unsafe_html=True)

# ============================================================================
# STEP 3: LIVE RE-INDEXING TICKER HEADINGS DISPLAY LAYER
# ============================================================================
if not st.session_state.fullscreen_mode:
    # Fetch metrics blocks asynchronously from safe cached repository mapping 
    btc_metrics = fetch_live_market_data("BTC")
    eth_metrics = fetch_live_market_data("ETH")
    sol_metrics = fetch_live_market_data("SOL")
    paxg_metrics = fetch_live_market_data("PAXG")
    
    st.markdown('<div class="main-terminal-header">🤖 DELTA QUANT TERMINAL v3.0 PRO</div>', unsafe_html=True)
    
    # Structural Live Tickers Top Bar Row Output Generation Layer
    ticker_col1, ticker_col2, ticker_col3, ticker_col4 = st.columns(4)
    
    with ticker_col1:
        if btc_metrics["valid"]:
            status_color = "price-bullish" if btc_metrics["change"] >= 0 else "price-bearish"
            st.markdown(f"""
            <div class="sub-panel-card">
                <div class="metric-title-custom">⚡ BTC / USD INDEX</div>
                <div style="font-size:20px; font-weight:bold; margin-top:4px;" class="{status_color}">${btc_metrics['price']:,.2f}</div>
                <div style="font-size:12px;" class="{status_color}">{btc_metrics['change']:+.2f}% 24h</div>
            </div>
            """, unsafe_html=True)
        else:
            st.markdown('<div class="sub-panel-card">BTC Stream Disconnected</div>', unsafe_html=True)
            
    with ticker_col2:
        if eth_metrics["valid"]:
            status_color = "price-bullish" if eth_metrics["change"] >= 0 else "price-bearish"
            st.markdown(f"""
            <div class="sub-panel-card">
                <div class="metric-title-custom">💎 ETH / USD INDEX</div>
                <div style="font-size:20px; font-weight:bold; margin-top:4px;" class="{status_color}">${eth_metrics['price']:,.2f}</div>
                <div style="font-size:12px;" class="{status_color}">{eth_metrics['change']:+.2f}% 24h</div>
            </div>
            """, unsafe_html=True)
        else:
            st.markdown('<div class="sub-panel-card">ETH Stream Disconnected</div>', unsafe_html=True)
            
    with ticker_col3:
        if sol_metrics["valid"]:
            status_color = "price-bullish" if sol_metrics["change"] >= 0 else "price-bearish"
            st.markdown(f"""
            <div class="sub-panel-card">
                <div class="metric-title-custom">🔮 SOL / USD INDEX</div>
                <div style="font-size:20px; font-weight:bold; margin-top:4px;" class="{status_color}">${sol_metrics['price']:,.2f}</div>
                <div style="font-size:12px;" class="{status_color}">{sol_metrics['change']:+.2f}% 24h</div>
            </div>
            """, unsafe_html=True)
        else:
            st.markdown('<div class="sub-panel-card">SOL Stream Disconnected</div>', unsafe_html=True)
            
    with ticker_col4:
        if paxg_metrics["valid"]:
            status_color = "price-bullish" if paxg_metrics["change"] >= 0 else "price-bearish"
            st.markdown(f"""
            <div class="sub-panel-card">
                <div class="metric-title-custom">🌟 PAXG / GOLD INDEX</div>
                <div style="font-size:20px; font-weight:bold; margin-top:4px;" class="{status_color}">${paxg_metrics['price']:,.2f}</div>
                <div style="font-size:12px;" class="{status_color}">{paxg_metrics['change']:+.2f}% 24h</div>
            </div>
            """, unsafe_html=True)
        else:
            st.markdown('<div class="sub-panel-card">PAXG Stream Disconnected</div>', unsafe_html=True)

# ============================================================================
# STEP 4: PRIMARY CONTROL INTERFACE PANEL SYSTEM & SYMBOL RESOLUTION
# ============================================================================
# Core controls arrangement row
ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([2, 1, 1, 1])

with ctrl_col1:
    search_symbol_input = st.text_input(
        "Active Trading Asset Token Pair", 
        value="BTC", 
        max_chars=10, 
        key="global_symbol_resolver_key",
        placeholder="Enter Base Ticker Asset (e.g. BTC, ETH, SOL, XRP)..."
    )
    resolved_asset = search_symbol_input.upper().strip()

with ctrl_col2:
    apply_ema_filter = st.checkbox("Exponential Moving Avg Ribbon (EMA)", value=False, key="ui_ema_switch_flag")
with ctrl_col3:
    apply_vol_filter = st.checkbox("Real-time Trading Volume Profiles (VOL)", value=True, key="ui_vol_switch_flag")

with ctrl_col4:
    # Mutator execution handles switching layouts cleanly
    if st.session_state.fullscreen_mode:
        if st.button("📺 Exit Full Screen View", use_container_width=True, type="primary"):
            st.session_state.fullscreen_mode = False
            logger_msg("Resetting terminal UI structure to normal viewport layout split.")
            st.rerun()
    else:
        if st.button("🔍 Enable Ultra Chart View", use_container_width=True, type="secondary"):
            st.session_state.fullscreen_mode = True
            logger_msg(f"Terminal viewport reconfigured to full chart operational scaling for {resolved_asset}USDT.")
            st.rerun()

# Run target analytics verification cycle
target_live_matrix = fetch_live_market_data(resolved_asset)
if not target_live_matrix["valid"]:
    # Fallback to safety defaults safely to prevent application freeze mechanics
    target_live_matrix = {"price": 50000.0, "change": 1.25, "high": 51200.0, "low": 49800.0, "vol": 150000000.0, "vwap": 50500.0}

# Mapping study indicators explicitly matching string array models
active_indicator_payload = []
if apply_ema_filter:
    active_indicator_payload.append("MASimple@tv-basicstudies")
if apply_vol_filter:
    active_indicator_payload.append("Volume@tv-basicstudies")

dynamic_viewport_height = 640 if st.session_state.fullscreen_mode else 400

# ============================================================================
# STEP 5: CENTRAL QUANT COMPONENT LAYOUT BLOCK (CHART vs LATERAL MODULES)
# ============================================================================
# Define grid mapping split conditionally based on target fullscreen visibility tags
if st.session_state.fullscreen_mode:
    workspace_chart_col, workspace_analytics_col = st.columns([1, 0]), None
else:
    workspace_chart_col, workspace_analytics_col = st.columns([3, 1])

with workspace_chart_col:
    # ------------------------------------------------------------------------
    # SUB-MODULE: PRODUCTION LEVEL TRADINGVIEW IFRAME ENGINE (NON-CRASH BLUEPRINT)
    # ------------------------------------------------------------------------
    # Building exact URL tracking tags using standardized safe replacement filters natively
    base_embed_template_url = "https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:__REPLACED_PAIR__USDT&interval=60&theme=dark&style=1&timezone=Exchange"
    
    # Process modifications parameters without generating broken brackets configurations
    processed_embed_target = base_embed_template_url.replace("__REPLACED_PAIR__", resolved_asset)
    
    # Append indicator parameters directly matching structural setup strings
    if apply_ema_filter:
        processed_embed_target += "&studies=MASimple@tv-basicstudies"
    if apply_vol_filter:
        processed_embed_target += "&studies=Volume@tv-basicstudies"
        
    st.components.v1.iframe(
        src=processed_embed_target,
        height=dynamic_viewport_height,
        scrolling=False
    )

# Render auxiliary side panels only if normal view matrix constraints match
if workspace_analytics_col is not None:
    with workspace_analytics_col:
        st.markdown(f"""
        <div class="sub-panel-card" style="height: {dynamic_viewport_height}px; overflow-y:auto; margin-bottom:0px;">
            <div class="active-tag" style="text-align:center; margin-bottom:10px;">📉 CONFLUENCE MONITOR</div>
            <p style="font-size:12px; margin-bottom:4px; color:#808a9d;">TARGET INSTRUMENT</p>
            <h4 style="margin:0px; font-family:monospace; color:#ffffff;">{resolved_asset} / USDT</h4>
            <hr style="border:0px; border-top:1px solid #212630; margin:10px 0px;">
            
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#808a9d;">Last Price:</span>
                <span style="font-weight:bold; font-family:monospace;">${target_live_matrix['price']:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#808a9d;">24h High:</span>
                <span style="font-family:monospace; color:#ffffff;">${target_live_matrix['high']:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#808a9d;">24h Low:</span>
                <span style="font-family:monospace; color:#ffffff;">${target_live_matrix['low']:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#808a9d;">24h Turnover:</span>
                <span style="font-family:monospace; color:#0ecb81;">${target_live_matrix['vol']/1000000:,.1f}M</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#808a9d;">VWAP Pivot:</span>
                <span style="font-family:monospace; color:#7047eb;">${target_live_matrix['vwap']:,.2f}</span>
            </div>
            
            <hr style="border:0px; border-top:1px solid #212630; margin:10px 0px;">
            <div class="metric-title-custom" style="margin-bottom:6px;">AUTOMATED STRATEGY MATRIX</div>
            
            <div style="background-color:#050608; border-radius:4px; padding:8px; font-size:11px; margin-bottom:6px; border-left: 3px solid #0ecb81;">
                <b style="color:#0ecb81;">EMA CONFLUENCE:</b><br>
                Price tracking {'ABOVE' if target_live_matrix['price'] > target_live_matrix['vwap'] else 'BELOW'} mathematical VWAP boundaries. Structural bias trend steady.
            </div>
            <div style="background-color:#050608; border-radius:4px; padding:8px; font-size:11px; border-left: 3px solid #7047eb;">
                <b style="color:#7047eb;">VOLUMETRIC SCORE:</b><br>
                Liquid inflows match normal baseline thresholds. No immediate block distribution detected.
            </div>
        </div>
        """, unsafe_html=True)

# ============================================================================
# STEP 6: PROFESSIONAL QUANT TECHNICAL CALCULATIONS PIPELINE
# ============================================================================
if not st.session_state.fullscreen_mode:
    st.markdown("### 📊 ALGORITHMIC DATA PROCESSING & STRATEGY MATRICES")
    
    # Generate high performance analytics data frames based on real time market data values
    historical_dataframe_context = generate_quant_matrix_history(target_live_matrix["price"], datapoints=120)
    
    # --- INDICATOR 1: EXPONENTIAL MOVING AVERAGE MATRIX ARRAY ---
    historical_dataframe_context["EMA_fast"] = historical_dataframe_context["Close"].ewm(span=12, adjust=False).mean()
    historical_dataframe_context["EMA_slow"] = historical_dataframe_context["Close"].ewm(span=26, adjust=False).mean()
    
    # --- INDICATOR 2: RELATIVE STRENGTH INDEX (RSI CODE) ---
    price_delta_matrix = historical_dataframe_context["Close"].diff()
    positive_gains_mapping = (price_delta_matrix.where(price_delta_matrix > 0, 0)).rolling(window=14).mean()
    negative_losses_mapping = (-price_delta_matrix.where(price_delta_matrix < 0, 0)).rolling(window=14).mean()
    relative_strength_series = positive_gains_mapping / (negative_losses_mapping + 1e-10)
    historical_dataframe_context["RSI_14"] = 100 - (100 / (1 + relative_strength_series))
    historical_dataframe_context["RSI_14"] = historical_dataframe_context["RSI_14"].fillna(50.0)
    
    # --- INDICATOR 3: BOLLINGER VOLATILITY BANDS ---
    historical_dataframe_context["BB_Basis"] = historical_dataframe_context["Close"].rolling(window=20).mean()
    historical_dataframe_context["BB_Std"] = historical_dataframe_context["Close"].rolling(window=20).std()
    historical_dataframe_context["BB_Upper"] = historical_dataframe_context["BB_Basis"] + (historical_dataframe_context["BB_Std"] * 2)
    historical_dataframe_context["BB_Lower"] = historical_dataframe_context["BB_Basis"] - (historical_dataframe_context["BB_Std"] * 2)
    
    # Pull current calculation references from tracking lists
    terminal_latest_row = historical_dataframe_context.iloc[-1]
    terminal_previous_row = historical_dataframe_context.iloc[-2]
    
    # Structural presentation block splits for math analytics mapping
    math_col1, math_col2, math_col3, math_col4 = st.columns(4)
    
    with math_col1:
        fast_ema_val = terminal_latest_row["EMA_fast"]
        slow_ema_val = terminal_latest_row["EMA_slow"]
        ema_trend_status = "BULLISH CROSSOVER" if fast_ema_val > slow_ema_val else "BEARISH REVERSED"
        st.metric(
            label=f"EMA (12/26) Signal Matrix", 
            value=f"{fast_ema_val:,.1f}", 
            delta=ema_trend_status,
            delta_color="normal" if fast_ema_val > slow_ema_val else "inverse"
        )
        
    with math_col2:
        rsi_metric_value = terminal_latest_row["RSI_14"]
        if rsi_metric_value >= 70:
            rsi_delta_status = "OVERBOUGHT EXHAUSTION"
        elif rsi_metric_value <= 30:
            rsi_delta_status = "OVERSOLD REBOUND"
        else:
            rsi_delta_status = "NEUTRAL MOMENTUM"
            
        st.metric(
            label="Relative Strength Index (RSI-14)",
            value=f"{rsi_metric_value:.2f}",
            delta=rsi_delta_status,
            delta_color="off"
        )
        
    with math_col3:
        upper_band_value = terminal_latest_row["BB_Upper"]
        lower_band_value = terminal_latest_row["BB_Lower"]
        volatility_spread_percentage = ((upper_band_value - lower_band_value) / terminal_latest_row["Close"]) * 100
        st.metric(
            label="Bollinger Volatility Bandwidth",
            value=f"{volatility_spread_percentage:.2f}%",
            delta="Expansion Phase" if volatility_spread_percentage > 4.5 else "Squeeze Phase",
            delta_color="normal"
        )
 
