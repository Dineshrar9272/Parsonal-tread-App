import streamlit as st
import json

# --- 1. COINS & TICKER DATA ---
top_cards_data = [
    {"symbol": "BTCUSD", "price": "$79,000.0", "change": "-0.14%", "status": "down"},
    {"symbol": "ETHUSD", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "ARCUSD", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"},
    {"symbol": "FFUSD", "desc": "Falcon Finance Perpetual", "price": "$0.0851", "vol": "$4.97M", "change": "+7.31%", "status": "up"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)

# --- 2. RESTORED AI LAYOUT ENGINE ---
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Delta Style Mobile Terminal</title>
    <style>
        html, body {
            background-color: #0b0c10;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0;
            height: 100%; width: 100%;
            overflow: hidden !important;
            position: fixed;
        }

        .top-navbar {
            background-color: #15171c;
            border-bottom: 1px solid #212630; display: flex;
            justify-content: space-around; padding: 6px 0; height: 38px; box-sizing: border-box;
        }
        .nav-link {
            text-align: center; font-size: 11px; color: #808a9d;
            cursor: pointer; flex: 1; font-weight: 500;
        }
        .nav-link.active { color: #7047eb; font-weight: bold; }

        .container { 
            padding: 6px; 
            height: calc(100% - 38px); 
            box-sizing: border-box;
            display: flex; flex-direction: column;
        }
        .tab-panel { display: none; height: 100%; width: 100%; }
        .tab-panel.active { display: flex; flex-direction: column; height: 100%; gap: 4px; }

        .search-container { display: flex; gap: 4px; height: 30px; flex-shrink: 0; }
        .search-bar { flex-grow: 1; padding: 0 8px; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-size: 11px; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 10px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        .screen-layout { display: flex; flex-direction: column; gap: 6px; flex-grow: 1; overflow: hidden; height: calc(100% - 34px); }
        .chart-box { width: 100%; height: 50%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; flex-shrink: 0; }
        
        /* Persistent AI Panel Structure */
        .ai-exchange-box { 
            width: 100%; height: 50%; background: #15171c; 
            border: 1px solid #212630; border-radius: 6px; padding: 6px; 
            box-sizing: border-box; display: flex; flex-direction: column; 
            overflow: hidden; justify-content: space-between;
        }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; padding-bottom: 2px; flex-shrink: 0; }
        .ai-badge { padding: 1px 4px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #0ecb81; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.35; overflow-y: auto; flex-grow: 1; background: #101114; padding: 6px; border-radius: 4px; border: 1px solid #1f2226; margin-bottom: 4px; }
        .ai-report-line { margin-bottom: 2px; border-bottom: 1px dashed #212630; padding-bottom: 1px; }
        .ai-highlight { color: #f0a500; font-weight: bold; }

        .chat-input-bar { display: flex; gap: 4px; border-top: 1px solid #212630; padding-top: 4px; height: 32px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 8px; background: #0b0c10; border: 1px solid #212630; border-radius: 4px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div class="top-navbar">
        <div class="nav-link" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">🏠 Home</div>
        <div class="nav-link active" id="btn-chart" onclick="tabEngine('chart-ui', 'btn-chart')">📊 Charts & AI</div>
    </div>

    <div class="container">
        <div id="home-ui" class="tab-panel">
            <div style="padding: 10px; color: #808a9d; font-size: 12px;">Market Assets and Tickers Active.</div>
        </div>

        <div id="chart-ui" class="tab-panel active">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="Symbol...">
                <button class="search-trigger" onclick="renderTradingCore()">Search</button>
            </div>

            <div class="screen-layout">
                <div class="chart-box" id="tv-widget-frame"></div>

                <div class="ai-exchange-box" id="ai-interact-card">
                    <div class="ai-header-panel">
                        <span style="color:#7047eb;">📊 Real-time AI Quant Insights</span>
                        <span id="ai-status-tag" class="ai-badge">BULLISH</span>
                    </div>
                    
                    <div id="ai-logs-frame" class="ai-output-logs">AI Engine initialized. Ask a query below...</div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Ask AI: Entry kaha par lein?">
                        <button class="chat-btn" onclick="fireQuery()">Ask</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function loadTvWidget(coin) {
            const target = document.getElementById('tv-widget-frame');
            target.innerHTML = "";
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.type = 'text/javascript';
            script.async = true;
            script.onload = function() {
                new TradingView.widget({
                    "width": "100%", "height": "100%",
                    "symbol": "BINANCE:" + coin + "USDT",
                    "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                    "hide_side_toolbar": false, "allow_symbol_change": false,
                    "container_id": "tv-widget-frame"
                });
            };
            document.head.appendChild(script);
        }

        function renderTradingCore() {
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);
        }

        function fireQuery() {
            const promptBox = document.getElementById('user-prompt');
            const originalPrompt = promptBox.value;
            const val = originalPrompt.trim().toLowerCase();
            if(!val) return;

            const logBox = document.getElementById('ai-logs-frame');
            logBox.innerHTML = "⏳ <i>AI processing setup configurations...</i>";
            
            setTimeout(function() {
                let aiResponse = "";
                if (val.includes("entry") || val.includes("kaha par") || val.includes("trade")) {
                    aiResponse = '<div class="ai-report-line" style="color: #0ecb81; font-weight: bold;">✅ Bullish Setup Tracked</div>' +
                                 '<div class="ai-report-line">🟢 <b>Long Entry Zone:</b> Retracement to key Order Block/Demand cluster.</div>' +
                                 '<div class="ai-report-line">🎯 <b>Targets:</b> Next liquidity overhead zone.</div>' +
                                 '<div class="ai-report-line">🛡️ <b>Invalidation:</b> Close below structural session low.</div>';
                } else {
                    aiResponse = '<div class="ai-report-line">🤖 <b>AI Bias:</b> Asset order book structure shows strong support absorption. Market matrix holds steady.</div>';
                }

                logBox.innerHTML = '<div class="ai-report-line" style="color: #7047eb; font-weight: bold;">💬 User Request: "' + originalPrompt + '"</div>' + aiResponse;
                promptBox.value = "";
                logBox.scrollTop = 0;
            }, 400);
        }

        function tabEngine(panelId, btnId) {
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            document.getElementById(btnId).classList.add('active');
            if(panelId === 'chart-ui') { renderTradingCore(); }
        }

        window.onload = function() {
            renderTradingCore();
        }
    </script>
</body>
</html>
"""

dashboard_html = dashboard_html.replace("##TOP_TICKERS##", top_cards_json)
dashboard_html = dashboard_html.replace("##COINS_LIST##", coins_list_json)

st.components.v1.html(dashboard_html, height=580, scrolling=False)
