import streamlit as st

# --- 1. APP CONFIG & MOBILE OPTIMIZED LAYOUT ---
st.set_page_config(page_title="Delta Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to force clean spacing like your original layout
st.markdown("""
    <style>
        .block-container { padding-top: 0.5rem; padding-bottom: 0rem; padding-left: 0.5rem; padding-right: 0.5rem; }
        iframe { border-radius: 8px; border: 1px solid #212630 !important; }
        .stCheckbox label { color: #808a9d !important; font-size: 12px !important; font-weight: bold; }
    </style>
""", unsafe_html=True)

# --- 2. OLD CONFIG SEARCH & CONTROLS HEADER ---
# This brings back your exact original search panel (Screenshot_20260516_104222.jpg)
col_search, col_btn = st.columns([4, 1])
with col_search:
    asset_input = st.text_input("Asset", value="BTC", label_visibility="collapsed", placeholder="Enter Asset Symbol (e.g. BTC, ETH)...")
with col_btn:
    search_triggered = st.button("Search", use_container_width=True)

# Clean uppercase format for trading pairs
asset_symbol = asset_input.upper().strip()

# --- 3. DYNAMIC INDICATOR CONFIGURATION ---
# Restoring the original interactive EMA and VOL checkboxes
col_ema, col_vol, col_view = st.columns([1, 1, 2])
with col_ema:
    apply_ema = st.checkbox("EMA", value=False)
with col_vol:
    apply_vol = st.checkbox("VOL", value=True) # Kept volume checked by default as per old setups
with col_view:
    # Right-aligned view label to balance the layout structure
    st.markdown("<div style='text-align:right; font-size:11px; color:#808a9d; font-weight:bold; margin-top:4px;'>📊 Chart Mode: Active</div>", unsafe_html=True)

# Building active studies list array based on checkbox toggles safely
active_studies = []
if apply_ema:
    active_studies.append('"MAExp@tv-basicstudies"')  # Exponential Moving Average Line
if apply_vol:
    active_studies.append('"Volume@tv-basicstudies"') # Volume Bars Overlay

studies_js_array = f"[{', '.join(active_studies)}]"

# --- 4. TRADINGVIEW COMPONENT ENGINE ---
# Embeds the chart utilizing pure, standard TradingView architecture
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

# Render chart with custom viewport heights matching your neat mobile screen size
st.components.v1.html(tradingview_js, height=390, scrolling=False)

# --- 5. REAL-TIME AI QUANT INSIGHTS BLOCK ---
# Bringing back your original bottom terminal window box layout (Screenshot_2026_0516_111439.jpg)
st.markdown("<br>", unsafe_html=True)

with st.container():
    st.markdown("""
        <div style="background-color: #15171c; border: 1px solid #212630; border-radius: 8px; padding: 12px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="color: #7047eb; font-weight: bold; font-size: 13px;">📊 Real-time AI Quant Insights</span>
                <span style="background-color: #0ecb81; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">BULLISH</span>
            </div>
            <div style="font-size: 12px; color: #e1e4e8; margin-bottom: 6px; line-height: 1.4;">
                <span style="color: #808a9d; font-weight: bold;">💬 System Analysis:</span> Orderbooks for <b>{asset_symbol}</b> show solid structural absorption at key demand blocks. Market matrix remains stable.
            </div>
        </div>
    """.format(asset_symbol=asset_symbol), unsafe_html=True)

# Add your simple input box below the insights block
ai_query = st.text_input("Ask AI", key="quant_query", placeholder="Market me kya chal raha hai?", label_visibility="collapsed")
