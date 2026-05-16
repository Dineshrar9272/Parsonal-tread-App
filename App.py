import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

# --- 2. SCREEN VIEW MODE STATE (FOR FULL SCREEN / NORMAL SCREEN) ---
if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False

# --- 3. SEARCH OPTION OVER CHART (TOP BAR) ---
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset", value="BTC", label_visibility="collapsed", placeholder="Symbol (e.g. BTC, ETH)...")
with col_btn:
    st.button("Search", use_container_width=True)

asset_symbol = asset_input.upper().strip()

# --- 4. CONTROL INTERFACE (INDICATORS & SCREEN VIEWS) ---
col_ema, col_vol, col_screen = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False)
with col_vol:
    apply_vol = st.checkbox("VOL", value=True)
with col_screen:
    # Full Screen / Normal Screen Toggle Button
    if st.session_state.fullscreen_mode:
        if st.button("📺 Normal Screen", use_container_width=True):
            st.session_state.fullscreen_mode = False
            st.rerun()
    else:
        if st.button("🔍 Full Screen", use_container_width=True):
            st.session_state.fullscreen_mode = True
            st.rerun()

# Dynamic indicator logic allocation
active_studies = []
if apply_ema:
    active_studies.append('"MAExp@tv-basicstudies"')
if apply_vol:
    active_studies.append('"Volume@tv-basicstudies"')

studies_js_array = f"[{', '.join(active_studies)}]"

# Adjust chart heights based on screen selection mode
chart_height = 550 if st.session_state.fullscreen_mode else 350

# --- 5. TRADINGVIEW ENGINE ENGINE ---
tradingview_js = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        html, body {{ margin: 0; padding: 0; height: 100%; width: 100%; background-color: #0b0c10; overflow: hidden; }}
        #tv-chart {{ height: 100vh; width: 100vw; }}
    </style>
</head>
<body>
    <div id="tv-chart"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
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
            "container_id": "tv-chart",
            "studies": {studies_js_array}
        }});
    </script>
</body>
</html>
"""

st.components.v1.html(tradingview_js, height=chart_height, scrolling=False)

# --- 6. CONDITIONAL BOTTOM INSIGHTS WINDOW (HIDES ON FULLSCREEN MODE) ---
if not st.session_state.fullscreen_mode:
    st.markdown("<br>", unsafe_html=True)
    with st.container():
        st.markdown("""
            <div style="background-color: #15171c; border: 1px solid #212630; border-radius: 8px; padding: 12px; font-family: sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="color: #7047eb; font-weight: bold; font-size: 13px;">实时 AI Quant Insights</span>
                    <span style="background-color: #0ecb81; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">BULLISH</span>
                </div>
                <div style="font-size: 12px; color: #e1e4e8; line-height: 1.4;">
                    <span style="color: #808a9d; font-weight: bold;">💬 System Analysis:</span> Orderbooks for <b>{asset}</b> show strong support structure.
                </div>
            </div>
        """.format(asset=asset_symbol), unsafe_html=True)
        
    st.text_input("Ask AI", key="quant_query_old", placeholder="Market me kya chal raha hai?", label_visibility="collapsed")
    
