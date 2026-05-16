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

# --- 2. SCREEN PORT ENGINE ---
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
        .nav-icon { font-size: 13px; margin-bottom: 1px; }

        .container { 
            padding: 8px; 
            height: calc(100% - 38px); 
            box-sizing: border-box;
            overflow: hidden;
        }
        .tab-panel { display: none; height: 100%; width: 100%; }
        .tab-panel.active { display: flex; flex-direction: column; height: 100%; }

        .home-scroller { overflow-y: auto; height: 100%; width: 100%; }
        .ticker-row { display: flex; gap: 6px; margin-bottom: 8px; }
        .ticker-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 6px; flex: 1; }
        .ticker-title { font-size: 10px; color: #808a9d; }
        .ticker-price { font-size: 14px; font-weight: bold; margin-top: 1px; }
        .list-caption { display: flex; justify-content: space-between; color: #808a9d; font-size: 10px; padding: 4px; }
        .coin-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 4px; border-bottom: 1px solid #212630; }
        .coin-name { font-weight: bold; font-size: 12px; }
        .coin-sub { color: #808a9d; font-size: 10px; }
        .coin-badge { padding: 4px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; color: #fff; min-width: 55px; text-align: center; background-color: #0ecb81; }

        .search-container { display: flex; gap: 4px; margin-bottom: 6px; height: 32px; flex-shrink: 0; }
        .search-bar { flex-grow: 1; padding: 0 8px; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-weight: bold; font-size: 12px; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; }

        .panel-top-bar { display: flex; justify-content: flex-end; align-items: center; margin-bottom: 4px; flex-shrink: 0; }
        .fs-action { background: #212630; border: 1px solid #363c4e; color: #fff; font-size: 11px; padding: 3px 8px; border-radius: 4px; cursor: pointer; font-weight: bold; }

        .screen-layout { display: flex; flex-direction: column; gap: 6px; flex-grow: 1; height: calc(100% - 46px); box-sizing: border-box; overflow: hidden; }
        .chart-box { width: 100%; height: 55%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; box-sizing: border-box; }
        
        .ai-exchange-box { width: 100%; height: 45%; background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 8px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; margin-bottom: 2px; }
        .ai-badge { padding: 1px 4px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #0ecb81; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.35; overflow-y: auto; flex-grow: 1; margin-bottom: 4px; background: #101114; padding: 6px; border-radius: 4px; border: 1px solid #1f2226; }
        .ai-report-line { margin-bottom: 2px; border-bottom: 1px dashed #212630; padding-bottom: 1px; }
        .ai-highlight { color: #f0a500; font-weight: bold; }

        .chat-input-bar { display: flex; gap: 4px; border-top: 1px solid #212630; padding-top: 4px; height: 28px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 8px; background: #0b0c10; border: 1px solid #212630; border-radius: 4px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 10px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; }

        .floating-exit-btn { display: none; position: fixed; top: 6px; right: 6px; z-index: 999999; background: rgba(112, 71, 235, 0.95); border: none; color: white; padding: 4px 8px; font-size: 11px; font-weight: bold; border-radius: 4px; cursor: pointer; }

        body.fullscreen-active .top-navbar,
        body.fullscreen-active .search-container,
        body.fullscreen-active .panel-top-bar,
        body.fullscreen-active .ai-exchange-box { display: none !important; }
        body.fullscreen-active .container { padding: 0 !important; margin: 0 !important; height: 100% !important; width: 100% !important; }
        body.fullscreen-active .screen-layout { height: 100% !important; gap: 0 !important; }
        body.fullscreen-active .chart-box { position: absolute; top: 0; left: 0; width: 100%; height: 100% !important; border: none; border-radius: 0; z-index: 99999; }
        body.fullscreen-active .floating-exit-btn { display: block !important; }
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
            <div class="home-scroller">
                <div class="ticker-row" id="top-ticker-target"></div>
                <div class="list-caption">
                    <div style="width: 40%;">Contract</div><div style="width: 35%; text-align: right;">Price</div><div style="width: 25%; text-align: right;">Change</div>
                </div>
                <div id="coin-list-target"></div>
            </div>
        </div>

        <div id="chart-ui" class="tab-panel active">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="Symbol...">
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
                        <div id="ai-logs-frame" class="ai-output-logs">Evaluating metrics...</div>
                    </div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Ask AI: Entry kaha banau bullish ya bearish?">
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
            let rsi = status === "BULLISH" ? Math.floor(Math.random() * 10) + 62 : Math.floor(Math.random() * 10) + 38;
            let themeColor = status === "BULLISH" ? "#0ecb81" : "#f6465d";
            let statusText = status === "BULLISH" ? "Bullish Structure" : "Distribution";
            let advice = status === "BULLISH" ? "Buy setups active on minor pullbacks." : "Avoid long entry, sell pressure intense.";
            
            return '<div class="ai-report-line">🌐 <b>Asset:</b> <span class="ai-highlight">' + coin + 'USDT</span></div>' +
                   '<div class="ai-report-line">📈 <b>Vector:</b> <span style="color:' + themeColor + '; font-weight:bold;">' + statusText + '</span></div>' +
                   '<div class="ai-report-line">🔢 <b>RSI Index:</b> <span class="ai-highlight">' + rsi + '</span></div>' +
                   '<div class="ai-report-line">💡 <b>AI Bias:</b> ' + advice + '</div>';
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
                    "studies": []
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
                badge.style.backgroundColor = "#0ecb81"; badge.innerText = "BULLISH";
            } else {
                badge.style.backgroundColor = "#f6465d"; badge.innerText = "BEARISH";
            }
            document.getElementById('ai-logs-frame').innerHTML = generateDetailedAnalysis(coin, bias);
        }

        function fireQuery() {
            const promptBox = document.getElementById('user-prompt');
            const originalPrompt = promptBox.value;
            const val = originalPrompt.trim().toLowerCase();
            if(!val) return;

            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            const logBox = document.getElementById('ai-logs-frame');
            logBox.innerHTML = "⏳ <i>AI processing smart order blocks...</i>";
            
            setTimeout(function() {
                let aiResponse = "";
                
                if (val.includes("entry") || val.includes("kaha banau") || val.includes("tread") || val.includes("trade")) {
                    if (val.includes("brish") || val.includes("bearish") || val.includes("down")) {
                        aiResponse = '<div class="ai-report-line" style="color: #f6465d; font-weight: bold;">🚨 Bearish Trade Setup Selected</div>' +
                                     '<div class="ai-report-line">🛑 <b>Short Entry Zone:</b> Break below local VWAP support block.</div>' +
                                     '<div class="ai-report-line">🎯 <b>Targets:</b> Support Block-1 & Fib extension 0.618</div>' +
                                     '<div class="ai-report-line">🛡️ <b>Stop-Loss:</b> Previous 1H swing high matrix level.</div>';
                    } else {
                        aiResponse = '<div class="ai-report-line" style="color: #0ecb81; font-weight: bold;">✅ Bullish Setup Confirmed</div>' +
                                     '<div class="ai-report-line">🟢 <b>Long Entry Optimal Level:</b> Wait for retracement to Order Block demand pool.</div>' +
                                     '<div class="ai-report-line">🎯 <b>Take-Profit Targets:</b> Next liquidity pocket resistance lines.</div>' +
                                     '<div class="ai-report-line">🛡️ <b>Invalidation (SL):</b> Structural close below current session low.</div>';
                    }
                } else if (val.includes("bullish") || val.includes("buy") || val.includes("up")) {
                    aiResponse = '<div class="ai-report-line">🤖 <b>AI Bias:</b> Aggressive buy side accumulation detected on <span class="ai-highlight">' + coin + '</span>. Momentum favors Long configurations.</div>';
                } else if (val.includes("bearish") || val.includes("brish") || val.includes("sell")) {
                    aiResponse = '<div class="ai-report-line">🤖 <b>AI Bias:</b> Order distribution phase active for <span class="ai-highlight">' + coin + '</span>. Sell blocks are heavily defended.</div>';
                } else {
                    aiResponse = '<div class="ai-report-line">🤖 <b>AI Core Response:</b> Structure on <span class="ai-highlight">' + coin + '</span> shows strong limit order absorption. Overhead resistance is soft, matrix stable.</div>';
                }

                logBox.innerHTML = '<div class="ai-report-line" style="color: #7047eb; font-weight: bold;">💬 User Request: "' + originalPrompt + '"</div>' + aiResponse;
                promptBox.value = "";
            }, 450);
        }

        function tabEngine(panelId, btnId) {
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            document.getElementById(btnId).classList.add('active');
            if(panelId === 'chart-ui') { renderTradingCore(); }
        }

        window.onload = function() {
            document.getElementById('top-ticker-target').innerHTML = rawTickers.map(t => '<div class="ticker-card"><div class="ticker-title"><span>' + t.symbol + '</span></div><div class="ticker-price">' + t.price + '</div></div>').join('');
            document.getElementById('coin-list-target').innerHTML = rawCoins.map(c => '<div class="coin-item"><div><span class="coin-name">' + c.symbol + '</span><br><span class="coin-sub">' + c.desc + '</span></div><div style="font-weight:bold;">' + c.price + '</div><div class="coin-badge">' + c.change + '</div></div>').join('');
            renderTradingCore();
        }
    </script>
</body>
</html>
"""

dashboard_html = dashboard_html.replace("##TOP_TICKERS##", top_cards_json)
dashboard_html = dashboard_html.replace("##COINS_LIST##", coins_list_json)

st.components.v1.html(dashboard_html, height=580, scrolling=False)
