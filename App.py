import streamlit as st

# --- 1. SET CONFIGURATION & SESSION STATES ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False

# --- 2. SEARCH OPTION OVER CHART (TOP BAR) ---
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset", value="BTC", label_visibility="collapsed", placeholder="Symbol (e.g. BTC, ETH)...")
with col_btn:
    st.button("Search", use_container_width=True)

asset_symbol = asset_input.upper().strip()

# --- 3. CONTROL INTERFACE (INDICATORS & SCREEN VIEWS) ---
col_ema, col_vol, col_screen = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False, key="ema_toggle_fixed")
with col_vol:
    apply_vol = st.checkbox("VOL", value=True, key="vol_toggle_fixed")
with col_screen:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Normal Screen", use_container_width=True):
            st.session_state.fullscreen_mode = False
            st.st.rerun()
    else:
        if st.button("🔍 Full Screen", use_container_width=True):
            st.session_state.fullscreen_mode = True
            st.st.rerun()

# Build active studies list safely without string formatting breaking python
active_studies = []
if apply_ema:
    active_studies.append("MASimple@tv-basicstudies")
if apply_vol:
    active_studies.append("Volume@tv-basicstudies")

chart_height = 560 if st.session_state.fullscreen_mode else 360

# --- 4. SAFE TRADINGVIEW EMBED ENGINE (NO CONFUSED F-STRINGS) ---
# Separating the dynamic injections cleanly to avoid braces conflict completely
tradingview_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        html, body { margin: 0; padding: 0; height: 100%; width: 100%; background-color: #0b0c10; overflow: hidden; }
        #tv-chart-container { height: 100vh; width: 100vw; }
    </style>
</head>
<body>
    <div id="tv-chart-container"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        if (typeof TradingView !== 'undefined') {
            new TradingView.widget({
                "width": "100%",
                "height": "100%",
                "symbol": "BINANCE:__ASSET__USDT",
                "interval": "60",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#15171c",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "container_id": "tv-chart-container",
                "studies": __STUDIES__
            });
        }
    </script>
</body>
</html>
"""

# Replace placeholders safely using standard string replace instead of f-string
import json
ready_html = tradingview_html.replace("__ASSET__", asset_symbol).replace("__STUDIES__", json.dumps(active_studies))

st.components.v1.html(
    ready_html, 
    height=chart_height, 
    scrolling=False, 
    key=f"tv_fixed_{asset_symbol}_{chart_height}_{apply_ema}_{apply_vol}"
)

# --- 5. CONDITIONAL BOTTOM INSIGHTS WINDOW ---
if not st.session_state.fullscreen_mode:
    st.markdown("<br>", unsafe_html=True)
    with st.container():
        st.markdown(f"""
            <div style="background-color: #15171c; border: 1px solid #212630; border-radius: 8px; padding: 12px; font-family: sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="color: #7047eb; font-weight: bold; font-size: 13px;">📊 Real-time AI Quant Insights</span>
                    <span style="background-color: #0ecb81; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">LIVE ACTIVE</span>
                </div>
                <div style="font-size: 12px; color: #e1e4e8; line-height: 1.4;">
                    <span style="color: #808a9d; font-weight: bold;">💬 System Analysis:</span> Orderbook feed synchronized for <b>{asset_symbol}</b>. Indicators tracking accurately.
                </div>
            </div>
        """, unsafe_html=True)
        
    st.text_input("Ask AI", key="quant_query_v2", placeholder="Market me kya chal raha hai?", label_visibility="collapsed")
    
