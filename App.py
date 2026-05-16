import streamlit as st
import json

# --- 1. REALISTIC MARKET DATA (As per your Screenshot) ---
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

# --- 2. HTML/CSS/JS INTERFACE ---
dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delta Style AI Trading Platform</title>
    <style>
        :root {{
            --bg-dark: #0b0c10;
            --panel-bg: #15171c;
            --border-color: #212630;
            --text-main: #ffffff;
            --text-muted: #808a9d;
            --accent-color: #7047eb;
            --green: #0ecb81;
            --red: #f6465d;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0; padding: 0;
            user-select: none;
            overflow-x: hidden;
        }}

        /* --- TOP APPNAR NAVBAR --- */
        .top-navbar {{
            position: sticky; top: 0; background-color: var(--panel-bg);
            border-bottom: 1px solid var(--border-color); display: flex;
            justify-content: space-around; padding: 12px 0; z-index: 999;
        }}
        .nav-link {{
            text-align: center; font-size: 12px; color: var(--text-muted);
            cursor: pointer; flex: 1; font-weight: 500;
        }}
        .nav-link.active {{
            color: var(--accent-color); font-weight: bold;
        }}
        .nav-icon {{ font-size: 16px; margin-bottom: 2px; }}

        .container {{ padding: 10px; max-width: 100%; margin: 0 auto; }}
        .tab-panel {{ display: none; }}
        .tab-panel.active {{ display: block; }}

        /* --- HOME SCREEN INTERFACE (Delta Exchange Clone) --- */
        .ticker-row {{ display: flex; gap: 8px; margin-bottom: 12px; }}
        .ticker-card {{
            background: var(--panel-bg); border: 1px solid var(--border-color);
            border-radius: 6px; padding: 10px; flex: 1;
        }}
        .ticker-title {{ font-size: 11px; color: var(--text-muted); display: flex; justify-content: space-between; }}
        .ticker-price {{ font-size: 16px; font-weight: bold; margin-top: 4px; }}
        .list-caption {{ display: flex; justify-content: space-between; color: var(--text-muted); font-size: 11px; padding: 6px 4px; }}
        .coin-item {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 4px; border-bottom: 1px solid var(--border-color);
        }}
        .coin-name {{ font-weight: bold; font-size: 14px; }}
        .coin-sub {{ color: var(--text-muted); font-size: 11px; }}
        .coin-badge {{
            padding: 6px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;
            color: #fff; min-width: 65px; text-align: center;
        }}
        .up-bg {{ background-color: var(--green); }}
        .down-bg {{ background-color: var(--red); }}
        .up-txt {{ color: var(--green); }}
        .down-txt {{ color: var(--red); }}

        /* --- MULTI LANGUAGE 3-DOT BAR --- */
        .news-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .dots-menu {{ position: relative; cursor: pointer; font-size: 20px; padding: 0 8px; }}
        .lang-dropdown {{
            display: none; position: absolute; right: 0; top: 25px;
            background: var(--panel-bg); border: 1px solid var(--border-color);
            border-radius: 6px; z-index: 1000; min-width: 110px;
        }}
        .lang-dropdown div {{ padding: 8px 12px; font-size: 12px; color: var(--text-main); }}
        .lang-dropdown div:hover {{ background: rgba(255,255,255,0.05); color: var(--accent-color); }}
        .lang-dropdown div.selected {{ color: var(--accent-color); font-weight: bold; }}
        .lang-dropdown.show {{ display: block; }}
        .news-item {{ background: var(--panel-bg); border: 1px solid var(--border-color); padding: 12px; border-radius: 8px; margin-bottom: 10px; }}

        /* --- SEARCH WRAPPER --- */
        .search-container {{ display: flex; gap: 6px; margin-bottom: 10px; }}
        .search-bar {{
            flex-grow: 1; padding: 10px; background: var(--panel-bg);
            border: 1px solid var(--border-color); border-radius: 6px; color: #fff; font-weight: bold;
        }}
        .search-trigger {{ background: var(--accent-color); border: none; color: white; padding: 0 14px; border-radius: 6px; font-weight: bold; }}

        /* ================= EXPERT FLEX SYSTEM (HALF/FULL CONTROL) ================= */
        .screen-layout {{
            display: flex; flex-direction: column; gap: 8px; transition: all 0.2s ease;
        }}
        
        .chart-box {{
            flex: 1; background: var(--panel-bg); border: 1px solid var(--border-color);
            border-radius: 8px; overflow: hidden; height: 320px; position: relative;
        }}
        
        /* Replace Buy/Sell Area with Sleek AI Space */
        .ai-exchange-box {{
            flex: 1; background: var(--panel-bg); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 12px; display: flex; flex-direction: column;
            justify-content: space-between; height: 210px;
        }}

        .panel-top-bar {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 6px; background: rgba(255,255,255,0.02); padding: 6px; border-radius: 4px;
        }}
        .indicator-labels {{ display: flex; gap: 10px; font-size: 11px; }}
        .indicator-labels label {{ display: flex; align-items: center; gap: 3px; cursor: pointer; }}
        
        .fs-action {{
            background: #212630; border: none; color: #fff; font-size: 11px;
            padding: 4px 8px; border-radius: 4px; cursor: pointer; font-weight: bold;
        }}

        .ai-header-panel {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; margin-bottom: 6px; }}
        .ai-badge {{ padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #fff; }}
        .ai-output-logs {{ font-size: 12px; color: var(--text-main); line-height: 1.4; overflow-y: auto; flex-grow: 1; margin-bottom: 8px; }}

        /* Chat System */
        .chat-input-bar {{ display: flex; gap: 6px; border-top: 1px solid var(--border-color); padding-top: 8px; }}
        .chat-field {{
            flex-grow: 1; padding: 8px; background: var(--bg-dark);
            border: 1px solid var(--border-color); border-radius: 4px; color: #fff; font-size: 12px;
        }}
        .chat-btn {{ background: var(--accent-color); border: none; color: #fff; padding: 0 12px; border-radius: 4px; font-size: 11px; font-weight: bold; }}

        /* ================= FULL SCREEN MODE (2ND SCREENSHOT CONFIG) ================= */
        body.fullscreen-active .ai-exchange-box {{
            position: fixed; right: 0; bottom: 0; top: 108px; width: 140px;
            height: calc(100vh - 120px); border-left: 1px solid var(--border-color);
            z-index: 500; border-radius: 0; box-shadow: -4px 0 10px rgba(0,0,0,0.5);
        }}
        body.fullscreen-active .chart-box {{
            height: calc(100vh - 140px) !important;
            margin-right: 145px;
        }}
        body.fullscreen-active .screen-layout {{
            flex-direction: row !important;
        }}
        body.fullscreen-active .chat-input-bar {{ display: none !important; }}
    </style>
</head>
<body>

    <div class="top-navbar">
        <div class="nav-link active" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">
            <div class="nav-icon">🏠</div><div>Home</div>
        </div>
        <div class="nav-link" id="btn-news" onclick="tabEngine('news-ui', 'btn-news')">
            <div class="nav-icon">📰</div><div>News</div>
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

        <div id="news-ui" class="tab-panel">
            <div class="news-header">
                <h3 style="margin:0; font-size:16px;">AI Stream News</h3>
                <div class="dots-menu" onclick="toggleLanguage(event)">⋮
                    <div id="lang-box" class="lang-dropdown">
                        <div id="lang-opt-en" class="selected" onclick="setLanguage('en')">English</div>
                        <div id="lang-opt-hi" onclick="setLanguage('hi')">Hindi</div>
                        <div id="lang-opt-pa" onclick="setLanguage('pa')">Punjabi</div>
                    </div>
                </div>
            </div>
            <div id="news-feed-target"></div>
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
                <button class="fs-action" onclick="switchViewMode()">🔍 Full Screen</button>
            </div>

            <div class="screen-layout" id="layout-box">
                <div class="chart-box" id="tv-widget-frame"></div>

                <div class="ai-exchange-box" id="ai-interact-card">
                    <div>
                        <div class="ai-header-panel">
                            <span style="color:var(--accent-color);">✨ AI Intelligence</span>
                            <span id="ai-status-tag" class="ai-badge up-bg">BULLISH</span>
                        </div>
                        <div id="ai-logs-frame" class="ai-output-logs">Analysing market indices...</div>
                    </div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Ask AI: Market me kya chal raha hai?">
                        <button class="chat-btn" onclick="fireQuery()">Ask</button>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <script>
        const rawTickers = {top_cards_json};
        const rawCoins = {coins_list_json};

        const aiBabelEngine = {{
            "en": {{
                "BULLISH": "Market structure looks clean. Bullish crossover spotted on hourly candle frames.",
                "BEARISH": "Liquidation risk high. Price facing distribution patterns at upper resistance bounds.",
                "ask_reply": "System Status: Whales are filling long orders at lower support bands. Trend remains steady."
            }},
            "hi": {{
                "BULLISH": "मार्केट का स्ट्रक्चर मजबूत है। 1-घंटे के चार्ट पर तेजी (Bullish Crossover) देखने को मिल रही है।",
                "BEARISH": "गिरावट का खतरा है। ऊपर के रेजिस्टेंस लेवल पर लगातार सेलिंग प्रेशर बन रहा है।",
                "ask_reply": "मार्केट अपडेट: बड़े ट्रेडर्स और व्हेल्स इस समय नीचे के रेट पर खरीदारी कर रहे हैं, ट्रेंड स्थिर है।"
            }},
            "pa": {{
                "BULLISH": "ਮਾਰਕੀਟ ਵਿੱਚ ਤੇਜ਼ੀ ਦੇ ਸੰਕੇਤ ਹਨ। 1-ਘੰਟੇ ਦੇ ਚਾਰਟ 'ਤੇ ਖਰੀਦਦਾਰੀ ਵਧ ਰਹੀ ਹੈ।",
                "BEARISH": "ਮਾਰਕੀਟ ਵਿੱਚ ਮੰਦੀ ਆ ਸਕਦੀ ਹੈ। ਉੱਪਰਲੇ ਪੱਧਰ 'ਤੇ ਲਗਾਤਾਰ ਵੇਚਣ ਦਾ ਦਬਾਅ ਬਣਿਆ ਹੋਇਆ ਹੈ।",
                "ask_reply": "ਮਾਰਕੀਟ ਸਥਿਤੀ: ਵੱਡੇ ਨਿਵੇਸ਼ਕ ਹੇਠਲੇ ਪੱਧਰ 'ਤੇ ਖਰੀਦਦਾਰੀ ਕਰ ਰਹੇ ਹਨ, ਰੁਝਾਨ ਸਥਿਰ ਹੈ।"
            }}
        }};

        let activeLang = 'en';

        function toggleLanguage(e) {{ e.stopPropagation(); document.getElementById('lang-box').classList.toggle('show'); }}
        window.addEventListener('click', function() {{ document.getElementById('lang-box').classList.remove('show'); }});

        function setLanguage(lang) {{
            activeLang = lang;
            document.querySelectorAll('.lang-dropdown div').forEach(d => d.classList.remove('selected'));
            document.getElementById(`lang-opt-${{lang}}`).classList.add('selected');
            renderTradingCore();
        }}

        // TRADINGVIEW ENGINE CONNECT
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

        // VIEW PORT MODIFIER TOGGLE (HALF vs FULL SPLIT)
        function switchViewMode() {{
            document.body.classList.toggle('fullscreen-active');
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);
        }}

        function renderTradingCore() {{
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);

            const bias = (coin.charCodeAt(0) % 2 === 0) ? "BULLISH" : "BEARISH";
            const badge = document.getElementById('ai-status-tag');
            
            if(bias === "BULLISH") {{
                badge.className = "ai-badge up-bg";
                badge.innerText = activeLang === 'hi' ? 'तेजी' : (activeLang === 'pa' ? 'ਤੇਜ਼ੀ' : 'BULLISH');
            }} else {{
                badge.className = "ai-badge down-bg";
                badge.innerText = activeLang === 'hi' ? 'मंदी' : (activeLang === 'pa' ? 'ਮੰਦੀ' : 'BEARISH');
            }}
            document.getElementById('ai-logs-frame').innerText = `[${{coin}}USDT] - ` + aiBabelEngine[activeLang][bias];
        }}

        function fireQuery() {{
            const val = document.getElementById('user-prompt').value.trim();
            if(!val) return;
            const logBox = document.getElementById('ai-logs-frame');
            logBox.innerHTML = "<i>AI System analyzing data arrays...</i>";
            setTimeout(() => {{
                logBox.innerText = "🤖 " + aiBabelEngine[activeLang]["ask_reply"];
                document.getElementById('user-prompt').value = "";
            }}, 500);
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
            document.getElementById('coin-list-target').innerHTML = rawCoins.map(c => `<div class="coin-item"><div><span class="coin-name">${{c.symbol}}</span><br><span class="coin-sub">${{c.desc}}</span></div><div style="font-weight:bold;">${{c.price}}</div><div class="coin-badge up-bg">${{c.change}}</div></div>`).join('');
            renderTradingCore();
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(dashboard_html, height=720, scrolling=True)
