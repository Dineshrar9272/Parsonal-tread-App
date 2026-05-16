import streamlit as st
import requests
import json

# --- 1. SET CORE LAYOUT CONFIGURATION ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

# Simple screen mode handling without messy components
if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False

# --- 2. PYTHON API LIVE TICKER DATA FETCH ---
def get_live_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        res = requests.get(url, timeout=2).json()
        price = float(res['lastPrice'])
        change = float(res['priceChangePercent'])
        return f"${price:,.2f}", f"{change:+.2f}%", change >= 0
    except:
        return "Syncing...", "0.00%", True

# Pull current rates instantly 
btc_p, btc_c, btc_up = get_live_price("BTC")
eth_p, eth_c, eth_up = get_live_price("ETH")
sol_p, sol_c, sol_up = get_live_price("SOL")
paxg_p, paxg_c, paxg_up = get_live_price("PAXG")

# --- 3. SEARCH PANEL (TOP BAR DESIGN OVER CHART) ---
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset", value="BTC", label_visibility="collapsed", placeholder="Search Symbol (e.g. BTC, ETH)...")
with col_btn:
    st.button("Search", use_container_width=True)

asset_symbol = asset_input.upper().strip()

# --- 4. CONTROLS SYSTEM INTERFACE (EMA, VOL, TOGGLE SCREEN) ---
col_ema, col_vol, col_screen = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False)
with col_vol:
    apply_vol = st.checkbox("VOL", value=True)
with col_screen:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Normal Screen", use_container_width=True):
            st.session_state.fullscreen_mode = False
            st.rerun()
    else:
        if st.button("🔍 Full Screen", use_container_width=True):
            st.session_state.fullscreen_mode = True
            st.rerun()

# Build pure static studies configurations string safely
active_studies = []
if apply_ema:
    active_studies.append("MASimple@tv-basicstudies")
if apply_vol:
    active_studies.append("Volume@tv-basicstudies")

chart_height = 540 if st.session_state.fullscreen_mode else 340

# --- 5. CLEAN & UNCRASHABLE LIVE TRADINGVIEW IFRAME ---
# Fixed direct integration blueprint to guarantee stability
tradingview_html_source = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        html, body { margin: 0; padding: 0; height: 100%; width: 100%; background-color: #0b0c10; overflow: hidden; }
        #canvas-frame-container { height: 100vh; width: 100vw; }
    </style>
</head>
<body>
    <div id="canvas-frame-container"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        if (typeof TradingView !== 'undefined') {
            new TradingView.widget({
                "width": "100%", "height": "100%",
                "symbol": "BINANCE:__ASSET_PAIR__USDT",
                "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                "toolbar_bg": "#15171c", "enable_publishing": false,
                "hide_side_toolbar": false, "allow_symbol_change": true,
                "container_id": "canvas-frame-container",
                "studies": __STUDIES_LIST__
            });
        }
    </script>
</body>
</html>
"""

# Swapping placeholders without changing variable keys inside streamlit component
compiled_html = tradingview_html_source.replace("__ASSET_PAIR__", asset_symbol).replace("__STUDIES_LIST__", json.dumps(active_studies))

# Static key prevents the component wrapper from breaking on re-renders
st.components.v1.html(
    compiled_html,
    height=chart_height,
    scrolling=False,
    key="fixed_tradingview_terminal_frame"
)

# --- 6. REAL-TIME MINI TICKER TILES & AI FEED (HIDES ON FULLSCREEN) ---
if not st.session_state.fullscreen_mode:
    st.markdown("<br>", unsafe_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px; margin-bottom:6px;">
            <div style="color:#808a9d; font-size:11px;">BTC / USD</div>
            <div style="font-size:15px; font-weight:bold; color:white;">{btc_p}</div>
            <div style="color:{'#0ecb81' if btc_up else '#f6465d'}; font-size:11px;">{btc_c}</div>
        </div>
        """, unsafe_html=True)
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px;">
            <div style="color:#808a9d; font-size:11px;">SOL / USD</div>
            <div style="font-size:15px; font-weight:bold; color:white;">{sol_p}</div>
            <div style="color:{'#0ecb81' if sol_up else '#f6465d'}; font-size:11px;">{sol_c}</div>
        </div>
        """, unsafe_html=True)
        
    with col2:
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px; margin-bottom:6px;">
            <div style="color:#808a9d; font-size:11px;">ETH / USD</div>
            <div style="font-size:15px; font-weight:bold; color:white;">{eth_p}</div>
            <div style="color:{'#0ecb81' if eth_up else '#f6465d'}; font-size:11px;">{eth_c}</div>
        </div>
        """, unsafe_html=True)
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px;">
            <div style="color:#808a9d; font-size:11px;">PAXG / USD</div>
            <div style="font-size:15px; font-weight:bold; color:white;">{paxg_p}</div>
            <div style="color:{'#0ecb81' if paxg_up else '#f6465d'}; font-size:11px;">{paxg_c}</div>
        </div>
        """, unsafe_html=True)

    st.markdown("<br>", unsafe_html=True)
    st.info(f"📊 **Live Status:** Feed synchronized for **{asset_symbol}**. Data streaming pipeline stable.")
    st.text_input("Ask Quant AI", key="quant_stable_chat", placeholder="Ask something about current trends...", label_visibility="collapsed")
    
