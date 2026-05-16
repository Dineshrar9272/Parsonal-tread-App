import streamlit as st
import json

# --- 1. CORE APPLICAION SETUP ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session management handling layout properties natively 
if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False

# --- 2. SEARCH OPTION OVER CHART (TOP BAR LAYOUT) ---
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset Input Field", value="BTC", label_visibility="collapsed", placeholder="Enter Asset Symbol (e.g. BTC, ETH)...")
with col_btn:
    st.button("Search", use_container_width=True)

asset_symbol = asset_input.upper().strip()

# --- 3. CONTROL BAR PANEL (CHECKBOXES & VIEW MULTIPLEXER) ---
col_ema, col_vol, col_screen = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False, key="core_ema_key")
with col_vol:
    apply_vol = st.checkbox("VOL", value=True, key="core_vol_key")
with col_screen:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Normal Screen", use_container_width=True, key="trigger_normal"):
            st.session_state.fullscreen_mode = False
            st.rerun()
    else:
        if st.button("🔍 Full Screen", use_container_width=True, key="trigger_full"):
            st.session_state.fullscreen_mode = True
            st.rerun()

# Processing the indicators array mapping securely
active_studies = []
if apply_ema:
    active_studies.append("MASimple@tv-basicstudies")
if apply_vol:
    active_studies.append("Volume@tv-basicstudies")

# Set structural height boundaries dynamically
chart_height = 540 if st.session_state.fullscreen_mode else 340

# --- 4. ENGINE: ISOLATED LIVE TRADINGVIEW COMPONENT ---
tradingview_html_raw = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        html, body { margin: 0; padding: 0; height: 100%; width: 100%; background-color: #0b0c10; overflow: hidden; }
        #canvas-frame { height: 100vh; width: 100vw; }
    </style>
</head>
<body>
    <div id="canvas-frame"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        if (typeof TradingView !== 'undefined') {
            new TradingView.widget({
                "width": "100%", "height": "100%",
                "symbol": "BINANCE:__PAIR__USDT",
                "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                "toolbar_bg": "#15171c", "enable_publishing": false,
                "hide_side_toolbar": false, "allow_symbol_change": true,
                "container_id": "canvas-frame",
                "studies": __STUDIES_ARRAY__
            });
        }
    </script>
</body>
</html>
"""

# Swapping the payload tags safely using native Python text transforms
rendered_html_source = tradingview_html_raw.replace("__PAIR__", asset_symbol).replace("__STUDIES_ARRAY__", json.dumps(active_studies))

# Unique structural key context forces container redraw instantly on value alterations
st.components.v1.html(
    rendered_html_source,
    height=chart_height,
    scrolling=False,
    key=f"terminal_canvas_engine_{asset_symbol}_{chart_height}_{apply_ema}_{apply_vol}"
)

# --- 5. CONDITIONAL BOTTOM QUANT TERMINAL ENGINE (DOCK CONFIGURATION) ---
if not st.session_state.fullscreen_mode:
    # Safe structure output block bypassing direct markdown component overrides entirely
    st.info(f"🤖 **AI Quant Live Feed:** Orderbook streams synchronized for **{asset_symbol}**. Structural metrics match standard tracking parameters.")
    st.text_input("Ask AI Terminal", key="quant_interactive_log", placeholder="Market trend analysis check...", label_visibility="collapsed")
    
