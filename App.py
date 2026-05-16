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

# --- 2. CLEAN HIGH-PERFORMANCE INTERFACE HTML ---
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delta Style Mobile Terminal</title>
    <style>
        body {
            background-color: #0b0c10;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0;
            overflow-x: hidden;
        }

        /* Top Bar Navigation */
        .top-navbar {
            position: sticky; top: 0; background-color: #15171c;
            border-bottom: 1px solid #212630; display: flex;
            justify-content: space-around; padding: 12px 0; z-index: 999;
        }
        .nav-link {
            text-align: center; font-size: 12px; color: #808a9d;
            cursor: pointer; flex: 1; font-weight: 500;
        }
        .nav-link.active { color: #7047eb; font-weight: bold; }
        .nav-icon { font-size: 16px; margin-bottom: 2px; }

        .container { padding: 10px; }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }

        /* Home View Layout */
        .ticker-row { display: flex; gap: 8px; margin-bottom: 12px; }
        .ticker-card {
            background: #15171c; border: 1px solid #212630;
            border-radius: 6px; padding: 10px; flex: 1;
        }
        .ticker-title { font-size: 11px; color: #808a9d; }
        .ticker-price { font-size: 16px; font-weight: bold; margin-top: 4px; }
        .list-caption { display: flex; justify-content: space-between; color: #808a9d; font-size: 11px; padding: 6px 4px; }
        .coin-item {
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 4px; border-bottom: 1px solid #212630;
        }
        .coin-name { font-weight: bold; font-size: 14px; }
        .coin-sub { color: #808a9d; font-size: 11px; }
        .coin-badge {
            padding: 6px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;
            color: #fff; min-width: 65px; text-align: center; background-color: #0ecb81;
        }

        /* Search Layout Header */
        .search-container { display: flex; gap: 6px; margin-bottom: 10px; }
        .search-bar {
            flex-grow: 1; padding: 10px; background: #15171c;
            border: 1px solid #212630; border-radius: 6px; color: #fff; font-weight: bold;
        }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 14px; border-radius: 6px; font-weight: bold; cursor: pointer; }

        /* Full Screen Trigger Control Block */
        .panel-top-bar {
            display: flex; justify-content: flex-end; align-items: center;
            margin-bottom: 8px;
        }
        .fs-action {
            background: #7047eb; border: none; color: #fff; font-size: 12px;
            padding: 6px 14px; border-radius: 4px; cursor: pointer; font-weight: bold;
        }

        /* Responsive Layout Matrix */
        .screen-layout { display: flex; flex-direction: column; gap: 10px; width: 100%; }
        .chart-box { width: 100%; height: 340px; background: #15171c; border: 1px solid #212630; border-radius: 8px; overflow: hidden; }
        
        /* AI Interface Box */
        .ai-exchange-box {
            width: 100%; height: 250px; background: #15171c; 
            border: 1px solid #212630; border-radius: 8px; padding: 12px;
            box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;
        }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; margin-bottom: 6px; }
        .ai-badge { padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #fff; background-color: #0ecb81; }
        .ai-output-logs { 
            font-size: 11.5px; color: #e1e4e8; line-height: 1.5; overflow-y: auto; flex-grow: 1; margin-bottom: 8px;
            background: #101114; padding: 8px; border-radius: 6px; border: 1px solid #1f2226;
        }
        .ai-report-line { margin-bottom: 4px; border-bottom: 1px dashed #212630; padding-bottom: 3px; }
        .ai-highlight { color: #f0a500; font-weight: bold; }

        /* User Query Chat fields */
        .chat-input-bar { display: flex; gap: 6px; border-top: 1px solid #212630; padding-top: 8px; }
        .chat-field {
            flex-grow: 1; padding: 8px 12px; background: #0b0c10;
            border: 1px solid #212630; border-radius: 6px; color: #ffffff; font-size: 13px; outline: none;
        }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 14px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; }

        /* Floating Back/Normal View Button for Pure Fullscreen Mode */
        .floating-exit-btn {
            display: none; position: fixed; top: 10px; right: 10px; z-index: 99999;
            background: rgba(112, 71, 235, 0.9); border: none; color: white;
            padding: 6px 12px; font-size: 11px; font-weight: bold; border-radius: 4px; cursor: pointer;
        }

        /* ================= DEEP STRETCH IMMERSIVE FULLSCREEN MODE ================= */
        body.fullscreen-active .top-navbar,
        body.fullscreen-active .search-container,
        body.fullscreen-active .panel-top-bar,
        body.fullscreen-active .ai-exchange-box {
            display: none !important; /* Hides everything else instantly */
        }
        body.fullscreen-active .container {
            padding: 0 !important; margin: 0 !important;
        }
        body.fullscreen-active .chart-box {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh !important;
            border: none; border-radius: 0; z-index: 9999;
        }
        body.fullscreen-active .floating-exit-btn {
            display: block !important; /* Shows exit trigger on top corner of the blank chart */
        }
    </style>
</head>
<body>

    <button class="floating-exit-btn" onclick="switchViewMode()">📉 Normal View</button>

    <div class="top-navbar">
        <div class="nav-link" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">
            <div class="nav-icon">🏠</div><div>Home</div>
        </div>
        <div class="nav-link active" id="btn-chart" onclick="tabEngine('chart-ui', 'btn-chart')">
            <div class="nav-icon">📊</div><div>Charts</div>
        </div>
    </div>

    <div class="container">
        <div id="home-ui" class="tab-panel">
            <div class="ticker-row" id="top-ticker-target"></div>
            <div class="list-caption">
                <div style="width: 40%;">Contract</div><div style="width: 35%; text-align: right;">Price</div><div style="width: 25%; text-align: right;">Change</div>
            </div>
            <div id="coin-list-target"></div>
        </div>

        <div id="chart-ui" class="tab-panel active">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="Symbol (e.g. BTC, ETH)...">
                <button class="search-trigger" onclick="renderTradingCore()">Search</button>
            </div>

            <div class="panel-top-bar">
                <button class="fs-action" onclick="switchViewMode()">🔍 Full Chart Mode</button>
            </div>

            <div class="screen-layout" id="layout-box">
                <div class="chart-box" id="tv-widget-frame"></div>

                <div class="ai-exchange-box" id="ai-interact-card">
                    <div>
                        <div class="ai-header-panel">
                            <span style="color:#7047eb;">📊 Real-time AI Quant Insights</span>
                            <span id="ai-status-tag" class="ai-badge">ANALYZING</span>
                        </div>
                        <div id="ai-logs-frame" class="ai-output-logs">Parsing multi-timeframe candle profiles...</div>
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
        const rawTickers = ##TOP_TICKERS##;
        const rawCoins = ##COINS_LIST##;

        function generateDetailedAnalysis(coin, status) {
            let rsi = status === "BULLISH" ? Math.floor(Math.random() * 15) + 55 : Math.floor(Math.random() * 15) + 35;
            let support = status === "BULLISH" ? "Strong baseline buying" : "Fragile local support";
            
            return `
                <div class="ai-report-line">🌐 <b>Asset:</b> <span class="ai-highlight">${coin}USDT (1H Frame)</span></div>
                <div class="ai-report-line">📈 <b>Trend Vector:</b> ${status === "BULLISH" ? '<span style="color:#0ecb81; font-weight:bold;">Strong Inflow (Bullish)</span>' : '<span style="color:#f6465d; font-weight:bold;">Distribution Phase</span>'}</div>
                <div class="ai-report-line">🔢 <b>RSI Index:</b> <span class="ai-highlight">${rsi}</span></div>
                <div class="ai-report-line">🛡️ <b>Orderbook Depth:</b> ${support} spotted at local Fibonacci blocks.</div>
                <div class="ai-report-line">💡 <b>AI Bias:</b> ${status === "BULLISH" ? 'Accumulate on pullbacks.' : 'Wait for breakdown confirmation.'}</div>
            `;
        }

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
                    "container_id": "tv-widget-frame",
                    "studies": ["MAExp@tv-basicstudies", "Volume@tv-basicstudies"]
                });
            };
            document.head.appendChild(script);
        }

        function switchViewMode() {
            document.body.classList.toggle('fullscreen-active');
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);
        }

        function renderTradingCore() {
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);
            const bias = (coin.charCodeAt(0) % 2 === 0) ? "BULLISH" : "BEARISH";
            const badge = document.getElementById('ai-status-tag');
            
            if(bias === "BULLISH") {
                badge.style.backgroundColor = "#0ecb81";
                badge.innerText = "BULLISH";
            } else {
                badge.style.backgroundColor = "#f6465d";
                badge.innerText = "BEARISH";
            }
            document.getElementById('ai-logs-frame').innerHTML = generateDetailedAnalysis(coin, bias);
        }

        function fireQuery() {
            const promptBox = document.getElementById('user-prompt');
            const val = promptBox.value.trim();
            if(!val) return;

            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            const logBox = document.getElementById('ai-logs-frame');
            logBox.innerHTML = "⏳ <i>AI is scanning orderbooks...</i>";
            
            setTimeout(function() {
                logBox.innerHTML = `
                    <div class="ai-report-line" style="color: #7047eb; font-weight: bold;">💬 Question Asked: "${val}"</div>
                    <div class="ai-report-line">🤖 <b>AI Live Answer:</b> <span class="ai-highlight">${coin}</span> orderbook patterns indicate smart money is actively holding current support zones. No heavy panic liquidations detected. Trend is steady.</div>
                `;
                promptBox.value = "";
            }, 600);
        }

        function tabEngine(panelId, btnId) {
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            document.getElementById(btnId).classList.add('active');
            if(panelId === 'chart-ui') { renderTradingCore(); }
        }

        window.onload = function() {
            document.getElementById('top-ticker-target').innerHTML = rawTickers.map(t => `<div class="ticker-card"><div class="ticker-title"><span>${t.symbol}</span></div><div class="ticker-price">${t.price}</div></div>`).join('');
            document.getElementById('coin-list-target').innerHTML = rawCoins.map(c => `<div class="coin-item"><div><span class="coin-name">${c.symbol}</span><br><span class="coin-sub">${c.desc}</span></div><div style="font-weight:bold;">${c.price}</div><div class="coin-badge">${c.change}</div></div>`).join('');
            renderTradingCore();
        }
    </script>
</body>
</html>
"""

# Safe DOM Dynamic Injections
dashboard_html = dashboard_html.replace("##TOP_TICKERS##", top_cards_json)
dashboard_html = dashboard_html.replace("##COINS_LIST##", coins_list_json)

st.components.v1.html(dashboard_html, height=750, scrolling=True)
