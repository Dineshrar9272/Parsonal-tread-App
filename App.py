import streamlit as st
import json

# --- 1. COINS & TICKER DATA ---
top_cards_data = [
    {"symbol": "BTCUSD", "price": "$79,080.5", "change": "-2.45%", "status": "down"},
    {"symbol": "ETHUSD", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "ARCUSD", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"},
    {"symbol": "FFUSD", "desc": "Falcon Finance Perpetual", "price": "$0.0851", "vol": "$4.97M", "change": "+7.31%", "status": "up"},
    {"symbol": "BEATUSD", "desc": "Audiera Perpetual", "price": "$0.6202", "vol": "$1.32M", "change": "+5.62%", "status": "up"},
    {"symbol": "PARTIUSD", "desc": "Particle Network Perpetual", "price": "$0.06232", "vol": "$283.91K", "change": "+3.57%", "status": "up"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)

# --- 2. ADVANCED INTERFACE WITHOUT PYTHON BLOCKING BUGS ---
dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delta Style Mobile Terminal</title>
    <style>
        body {{
            background-color: #0b0c10;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0;
            overflow-x: hidden;
        }}

        /* Navbar Layout */
        .top-navbar {{
            position: sticky; top: 0; background-color: #15171c;
            border-bottom: 1px solid #212630; display: flex;
            justify-content: space-around; padding: 12px 0; z-index: 999;
        }}
        .nav-link {{
            text-align: center; font-size: 12px; color: #808a9d;
            cursor: pointer; flex: 1; font-weight: 500;
        }}
        .nav-link.active {{ color: #7047eb; font-weight: bold; }}
        .nav-icon {{ font-size: 16px; margin-bottom: 2px; }}

        .container {{ padding: 10px; }}
        .tab-panel {{ display: none; }}
        .tab-panel.active {{ display: block; }}

        /* Home View Styles */
        .ticker-row {{ display: flex; gap: 8px; margin-bottom: 12px; }}
        .ticker-card {{
            background: #15171c; border: 1px solid #212630;
            border-radius: 6px; padding: 10px; flex: 1;
        }}
        .ticker-title {{ font-size: 11px; color: #808a9d; }}
        .ticker-price {{ font-size: 16px; font-weight: bold; margin-top: 4px; }}
        .list-caption {{ display: flex; justify-content: space-between; color: #808a9d; font-size: 11px; padding: 6px 4px; }}
        .coin-item {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 4px; border-bottom: 1px solid #212630;
        }}
        .coin-name {{ font-weight: bold; font-size: 14px; }}
        .coin-sub {{ color: #808a9d; font-size: 11px; }}
        .coin-badge {{
            padding: 6px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;
            color: #fff; min-width: 65px; text-align: center; background-color: #0ecb81;
        }}

        /* News Language Layout */
        .news-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .dots-menu {{ position: relative; cursor: pointer; font-size: 20px; padding: 0 8px; }}
        .lang-dropdown {{
            display: none; position: absolute; right: 0; top: 25px;
            background: #15171c; border: 1px solid #212630;
            border-radius: 6px; z-index: 1000; min-width: 110px;
        }}
        .lang-dropdown div {{ padding: 8px 12px; font-size: 12px; color: #ffffff; }}
        .lang-dropdown div.selected {{ color: #7047eb; font-weight: bold; }}
        .lang-dropdown.show {{ display: block; }}

        /* Dynamic Search Tools */
        .search-container {{ display: flex; gap: 6px; margin-bottom: 10px; }}
        .search-bar {{
            flex-grow: 1; padding: 10px; background: #15171c;
            border: 1px solid #212630; border-radius: 6px; color: #fff; font-weight: bold;
        }}
        .search-trigger {{ background: #7047eb; border: none; color: white; padding: 0 14px; border-radius: 6px; font-weight: bold; cursor: pointer; }}

        /* Control Toggles Bar */
        .panel-top-bar {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 8px; background: rgba(255,255,255,0.02); padding: 8px; border-radius: 6px;
        }}
        .indicator-labels {{ display: flex; gap: 12px; font-size: 12px; font-weight: 500; }}
        .indicator-labels label {{ display: flex; align-items: center; gap: 4px; cursor: pointer; }}
        .fs-action {{
            background: #212630; border: 1px solid #808a9d; color: #fff; font-size: 11px;
            padding: 5px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; transition: 0.2s;
        }}
        .fs-action:hover {{ background: #7047eb; border-color: #7047eb; }}

        /* ================= RESPONSIVE SMART LAYOUT GRID ================= */
        .screen-layout {{
            display: flex; flex-direction: column; gap: 10px; width: 100%;
        }}
        
        /* Normal Mode Height Layout (As per your Screenshot 1) */
        .chart-box {{
            width: 100%; height: 340px; background: #15171c; 
            border: 1px solid #212630; border-radius: 8px; overflow: hidden;
        }}
        
        /* AI Panel Layout (Placed where your old buy/sell used to be) */
        .ai-exchange-box {{
            width: 100%; height: 210px; background: #15171c; 
            border: 1px solid #212630; border-radius: 8px; padding: 12px;
            box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;
        }}

        .ai-header-panel {{ display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; margin-bottom: 6px; }}
        .ai-badge {{ padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #fff; background-color: #0ecb81; }}
        .ai-output-logs {{ font-size: 12px; color: #ffffff; line-height: 1.4; overflow-y: auto; flex-grow: 1; margin-bottom: 8px; }}

        /* Interactive Text Input Box (Fixed Typing Freezes) */
        .chat-input-bar {{ display: flex; gap: 6px; border-top: 1px solid #212630; padding-top: 8px; }}
        .chat-field {{
            flex-grow: 1; padding: 8px 12px; background: #0b0c10;
            border: 1px solid #212630; border-radius: 6px; color: #ffffff; font-size: 13px;
            outline: none;
        }}
        .chat-field:focus {{ border-color: #7047eb; }}
        .chat-btn {{ background: #7047eb; border: none; color: #fff; padding: 0 14px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; }}

        /* ================= EXTRA ACTION: STRETCH FULLSCREEN CONFIG ================= */
        body.fullscreen-active .ai-exchange-box {{
            display: none !important; /* Fully hidden when chart is expanded */
        }}
        body.fullscreen-active .chart-box {{
            height: 560px !important; /* Chart occupies whole block space smoothly */
        }}
    </style>
</head>
<body>

    <div class="top-navbar">
        <div class="nav-link active" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">
            <div class="nav-icon">🏠</div><div>Home</div>
        </div>
        <div class="nav-link" id="btn-chart" onclick="tabEngine('chart-ui', 'btn-chart')">
            <div class="nav-icon">📊</div><div>Charts</div>
        </div>
    </div>

    <div class="container">
        
        <div id="home-ui" class="tab-panel active">
            <div class="ticker-row" id="top-ticker-target"></div>
            <div class="list-caption">
                <div style="width: 40%;">Contract</div><div style="width: 35%; text-align: right;">Price</div><div style="width: 25%; text-align: right;">Change</div>
            </div>
            <div id="coin-list-target"></div>
        </div>

        <div id="chart-ui" class="tab-panel">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="Symbol (e.g. BTC, ETH)...">
                <button class="search-trigger" onclick="renderTradingCore()">Search</button>
            </div>

            <div class="panel-top-bar">
                <div class="indicator-labels">
                    <label><input type="checkbox" id="ind-ema" onchange="renderTradingCore()"> EMA</label>
                    <label><input type="checkbox" id="ind-vol" checked onchange="renderTradingCore()"> VOL</label>
                </div>
                <button id="fs-toggle-btn" class="fs-action" onclick="switchViewMode()">🔍 Full Screen Mode</button>
            </div>

            <div class="screen-layout" id="layout-box">
                <div class="chart-box" id="tv-widget-frame"></div>

                <div class="ai-exchange-box" id="ai-interact-card">
                    <div>
                        <div class="ai-header-panel">
                            <span style="color:#7047eb;">✨ AI Analytics Engine</span>
                            <span id="ai-status-tag" class="ai-badge">BULLISH</span>
                        </div>
                        <div id="ai-logs-frame" class="ai-output-logs">Parsing real-time volume structures...</div>
                    </div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Ask AI (e.g., Market me kya chal raha hai?)" value="">
                        <button class="chat-btn" onclick="fireQuery()">Ask</button>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <script>
        const rawTickers = {top_cards_json};
        const rawCoins = {coins_list_json};

        // Static Multi-lingual Database Maps
        const aiBabelEngine = {{
            "BULLISH": "Market framework is holding the support block securely. Volume delta shows buying accumulation on 1-hour candle sets.",
            "BEARISH": "Slight distribution noticed at higher range boundaries. Short term traders should manage target risks tightly.",
            "ask_reply": "AI Market Scan: Whales are currently protecting key demand blocks. No immediate aggressive breakdown trends are visible right now."
        }};

        // TRADINGVIEW LOADER LAYER 
        function loadTvWidget(coin) {{
            const target = document.getElementById('tv-widget-frame');
            target.innerHTML = "";

            const emaActive = document.getElementById('ind-ema').checked;
            const volActive = document.getElementById('ind-vol').checked;
            const studies = [];
            if(emaActive) studies.push("MAExp@tv-basicstudies");
            if(volActive) studies.push("Volume@tv-basicstudies");

            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.type = 'text/javascript';
            script.async = true;
            script.onload = function() {{
                new TradingView.widget({{
                    "width": "100%", "height": "100%",
                    "symbol": "BINANCE:" + coin + "USDT",
                    "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                    "hide_side_toolbar": false, "allow_symbol_change": false,
                    "container_id": "tv-widget-frame",
                    "studies": studies
                }});
            }};
            document.head.appendChild(script);
        }}

        // MASTER TOGGLE RULE: HIDE AI WHEN FULLSCREEN, SHOW AI WHEN NORMAL MODE
        function switchViewMode() {{
            const body = document.body;
            const btn = document.getElementById('fs-toggle-btn');
            
            body.classList.toggle('fullscreen-active');
            
            if(body.classList.contains('fullscreen-active')) {{
                btn.innerText = "📉 Normal View";
            }} else {{
                btn.innerText = "🔍 Full Screen Mode";
            }}

            // Refresh layout mapping 
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);
        }}

        function renderTradingCore() {{
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);

            const bias = (coin.charCodeAt(0) % 2 === 0) ? "BULLISH" : "BEARISH";
            const badge = document.getElementById('ai-status-tag');
            
            if(bias === "BULLISH") {{
                badge.style.backgroundColor = "#0ecb81";
                badge.innerText = "BULLISH";
            }} else {{
                badge.style.backgroundColor = "#f6465d";
                badge.innerText = "BEARISH";
            }}
            document.getElementById('ai-logs-frame').innerText = "[" + coin + "USDT] - " + aiBabelEngine[bias];
        }}

        // Dynamic AI Answering Processing
        function fireQuery() {{
            const promptBox = document.getElementById('user-prompt');
            const val = promptBox.value.trim();
            if(!val) return;

            const logBox = document.getElementById('ai-logs-frame');
            logBox.innerHTML = "⏳ <i>AI is scanning orderbooks for: \\"" + val + "\\"...</i>";
            
            setTimeout(() => {{
                logBox.innerHTML = "🤖 <b>AI Prediction:</b> " + aiBabelEngine["ask_reply"];
                promptBox.value = ""; // Empty string safely resets field without interface lockups
            }}, 600);
        }}

        function tabEngine(panelId, btnId) {{
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            document.getElementById(btnId).classList.add('active');
            if(panelId === 'chart-ui') {{ renderTradingCore(); }}
        }}

        window.onload = function() {{
            document.getElementById('top-ticker-target').innerHTML = rawTickers.map(t => `<div class="ticker-card"><div class="ticker-title"><span>${{t.symbol}}</span></div><div class="ticker-price">${{t.price}}</div></div>`).join('');
            document.getElementById('coin-list-target').innerHTML = rawCoins.map(c => `<div class="coin-item"><div><span class="coin-name">${{c.symbol}}</span><br><span class="coin-sub">${{c.desc}}</span></div><div style="font-weight:bold;">${{c.price}}</div><div class="coin-badge">${{c.change}}</div></div>`).join('');
            renderTradingCore();
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(dashboard_html, height=750, scrolling=True)
