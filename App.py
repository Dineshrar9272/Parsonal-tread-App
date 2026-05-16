import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import json

# --- 1. SET LAYOUT & AUTO REFRESH INTERVAL ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

# Har 10 second me background metrics data auto-update hoga (Bina page browser reset kiye)
st_autorefresh(interval=10000, limit=1000, key="live_data_counter")

if "fullscreen_mode" not in st.session_state:
    st.session_state.fullscreen_mode = False

# --- 2. FETCH REAL-TIME BINANCE LIVE TICKER RATES ---
def get_live_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        res = requests.get(url, timeout=2).json()
        price = float(res['lastPrice'])
        change = float(res['priceChangePercent'])
        return f"${price:,.2f}", f"{change:+.2f}%", change >= 0
    except:
        return "Loading...", "0.00%", True

btc_p, btc_c, btc_up = get_live_price("BTC")
eth_p, eth_c, eth_up = get_live_price("ETH")
sol_p, sol_c, sol_up = get_live_price("SOL")
paxg_p, paxg_c, paxg_up = get_live_price("PAXG")

# --- 3. SEARCH OPTION OVER CHART (TOP BAR) ---
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset Input Box", value="BTC", label_visibility="collapsed", placeholder="Enter Asset Symbol (e.g. BTC, ETH)...")
with col_btn:
    st.button("Search", use_container_width=True)

asset_symbol = asset_input.upper().strip()

# --- 4. CONTROL PANEL INTERFACE (INDICATORS & SCREEN VIEWS) ---
col_ema, col_vol, col_screen = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False, key="terminal_ema")
with col_vol:
    apply_vol = st.checkbox("VOL", value=True, key="terminal_vol")
with col_screen:
    if st.session_state.fullscreen_mode:
        if st.button("📺 Normal Screen", use_container_width=True, key="switch_normal"):
            st.session_state.fullscreen_mode = False
            st.rerun()
    else:
        if st.button("🔍 Full Screen", use_container_width=True, key="switch_full"):
            st.session_state.fullscreen_mode = True
            st.rerun()

# Build active indicators configurations natively
active_studies = []
if apply_ema:
    active_studies.append("MASimple@tv-basicstudies")
if apply_vol:
    active_studies.append("Volume@tv-basicstudies")

chart_height = 540 if st.session_state.fullscreen_mode else 340

# --- 5. 100% NON-FREEZING LIVE TRADINGVIEW EMBED ENGINE ---
tradingview_html_skeleton = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        html, body { margin: 0; padding: 0; height: 100%; width: 100%; background-color: #0b0c10; overflow: hidden; }
        #live-canvas { height: 100vh; width: 100vw; }
    </style>
</head>
<body>
    <div id="live-canvas"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        if (typeof TradingView !== 'undefined') {
            new TradingView.widget({
                "width": "100%", "height": "100%",
                "symbol": "BINANCE:__TICKER__USDT",
                "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                "toolbar_bg": "#15171c", "enable_publishing": false,
                "hide_side_toolbar": false, "allow_symbol_change": true,
                "container_id": "live-canvas",
                "studies": __STUDIES__
            });
        }
    </script>
</body>
</html>
"""

# Dynamic string swaps bypass f-string system errors completely
compiled_chart = tradingview_html_skeleton.replace("__TICKER__", asset_symbol).replace("__STUDIES__", json.dumps(active_studies))

st.components.v1.html(
    compiled_chart,
    height=chart_height,
    scrolling=False,
    key=f"live_view_engine_{asset_symbol}_{chart_height}_{apply_ema}_{apply_vol}"
)

# --- 6. LIVE METRICS MONITORING PANELS (HIDES ON FULLSCREEN) ---
if not st.session_state.fullscreen_mode:
    st.markdown("<br>", unsafe_html=True)
    
    # Live mini layout block matching dashboard cards (Screenshot_20260516_134254.jpg)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px; margin-bottom:5px;">
            <div style="color:#808a9d; font-size:11px;">BTC / USD</div>
            <div style="font-size:16px; font-weight:bold; color:white;">{btc_p}</div>
            <div style="color:{'#0ecb81' if btc_up else '#f6465d'}; font-size:11px;">{btc_c}</div>
        </div>
        """, unsafe_html=True)
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px;">
            <div style="color:#808a9d; font-size:11px;">SOL / USD</div>
            <div style="font-size:16px; font-weight:bold; color:white;">{sol_p}</div>
            <div style="color:{'#0ecb81' if sol_up else '#f6465d'}; font-size:11px;">{sol_c}</div>
        </div>
        """, unsafe_html=True)
        
    with c2:
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px; margin-bottom:5px;">
            <div style="color:#808a9d; font-size:11px;">ETH / USD</div>
            <div style="font-size:16px; font-weight:bold; color:white;">{eth_p}</div>
            <div style="color:{'#0ecb81' if eth_up else '#f6465d'}; font-size:11px;">{eth_c}</div>
        </div>
        """, unsafe_html=True)
        st.markdown(f"""
        <div style="background-color:#15171c; border:1px solid #212630; padding:10px; border-radius:6px;">
            <div style="color:#808a9d; font-size:11px;">PAXG / USD</div>
            <div style="font-size:16px; font-weight:bold; color:white;">{paxg_p}</div>
            <div style="color:{'#0ecb81' if paxg_up else '#f6465d'}; font-size:11px;">{paxg_c}</div>
        </div>
        """, unsafe_html=True)

    # Bot terminal window
    st.info(f"📊 **Live Feed Status:** Terminal synchronized. Orderbooks tracking data engine active for **{asset_symbol}**.")
    st.text_input("Ask Quant AI", key="quant_terminal_input", placeholder="Ask anything about current market metrics...", label_visibility="collapsed")
    
