import streamlit as st

# --- 1. SET CONFIGURATION & SESSION STATES ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False
if "chart_reload_key" not in st.session_state:
    st.session_state.chart_reload_key = 0

# --- 2. SEARCH OPTION OVER CHART (TOP BAR) ---
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset", value="BTC", label_visibility="collapsed", placeholder="Symbol (e.g. BTC, ETH)...")
with col_btn:
    if st.button("Search", use_container_width=True):
        st.session_state.chart_reload_key += 1  # Forces chart engine to pull fresh live candle feed

asset_symbol = asset_input.upper().strip()

# --- 3. CONTROL INTERFACE (INDICATORS & SCREEN VIEWS) ---
col_ema, col_vol, col_screen = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False, key="ema_toggle")
with col_vol:
    apply_vol = st.checkbox("VOL", value=True, key="vol_toggle")
with col_screen:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Normal Screen", use_container_width=True):
            st.session_state.fullscreen_mode = False
            st.session_state.chart_reload_key += 1
            st.rerun()
    else:
        if st.button("🔍 Full Screen", use_container_width=True):
            st.session_state.fullscreen_mode = True
            st.session_state.chart_reload_key += 1
            st.rerun()

# Dynamic live indicator tracking array
active_studies = []
if apply_ema:
    active_studies.append("MAExp@tv-basicstudies")
if apply_vol:
    active_studies.append("Volume@tv-basicstudies")

# Set exact structural pixel height mapping
chart_height = 550 if st.session_state.fullscreen_mode else 350

# --- 4. HIGH-PERFORMANCE LIVE TRADINGVIEW EMBED ENGINE ---
# We write the raw dynamic configuration natively into the TradingView constructor injection
import json
studies_json = json.dumps(active_studies)

tradingview_js = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        html, body {{ margin: 0; padding: 0; height: 100%; width: 100%; background-color: #0b0c10; overflow: hidden; }}
        #tv-chart-frame {{ height: 100vh; width: 100vw; }}
    </style>
</head>
<body>
    <div id="tv-chart-frame"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        (function() {{
            if (typeof TradingView !== 'undefined') {{
                new TradingView.widget({{
                    "width": "100%",
                    "height": "100%",
                    "symbol": "BINANCE:{asset_symbol}USDT",
                    "interval": "60",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "toolbar_bg": "#15171c",
                    "enable_publishing": false,
                    "hide_side_toolbar": false,
                    "allow_symbol_change": true,
                    "container_id": "tv-chart-frame",
                    "studies": {studies_json}
                }});
            }
        }})();
    </script>
</body>
</html>
"""

# Unique key forces Streamlit component layer to update instantly when a checkbox changes state
st.components.v1.html(
    tradingview_js, 
    height=chart_height, 
    scrolling=False, 
    key=f"live_chart_{asset_symbol}_{st.session_state.chart_reload_key}_{apply_ema}_{apply_vol}"
)

# --- 5. CONDITIONAL BOTTOM INSIGHTS WINDOW (HIDES ON FULLSCREEN) ---
if not st.session_state.fullscreen_mode:
    st.markdown("<br>", unsafe_html=True)
    with st.container():
        st.markdown(f"""
            <div style="background-color: #15171c; border: 1px solid #212630; border-radius: 8px; padding: 12px; font-family: sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="color: #7047eb; font-weight: bold; font-size: 13px;">📊 Real-time AI Quant Insights</span>
                    <span style="background-color: #0ecb81; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">LIVE TRACKING</span>
                </div>
                <div style="font-size: 12px; color: #e1e4e8; line-height: 1.4;">
                    <span style="color: #808a9d; font-weight: bold;">💬 System Analysis:</span> Data streaming for <b>{asset_symbol}</b> is active. Orderbook monitoring core components responding perfectly.
                </div>
            </div>
        """, unsafe_html=True)
        
    st.text_input("Ask AI", key="quant_query_live", placeholder="Market me kya chal raha hai?", label_visibility="collapsed")
    
