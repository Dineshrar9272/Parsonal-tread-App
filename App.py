import streamlit as st
import json

# --- 1. COINS, TICKER & DUMMY NEWS DATA ---
top_cards_data = [
    {"symbol": "BTCUSD", "price": "$79,041.60", "change": "-0.09%", "status": "down"},
    {"symbol": "ETHUSD", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "ARCUSD", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"},
    {"symbol": "FFUSD", "desc": "Falcon Finance Perpetual", "price": "$0.0851", "vol": "$4.97M", "change": "+7.31%", "status": "up"}
]

news_data = [
    {"title": "Bitcoin consolidates around $79K as orderbooks absorb localized spot selling pressure.", "time": "10m ago"},
    {"title": "Macro analysis suggests heavy liquidity building up near structural weekend session lows.", "time": "45m ago"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)
news_json = json.dumps(news_data)

# --- 2. STREAMLINED RE-STRUCTURED MOBILE ENGINE ---
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

        /* Top Bar Configuration with News Incorporated */
        .top-navbar {
            background-color: #15171c;
            border-bottom: 1px solid #212630; display: flex;
            justify-content: space-around; padding: 6px 0; height: 38px; box-sizing: border-box;
            align-items: center;
        }
        .nav-link {
            text-align: center; font-size: 11px; color: #808a9d;
            cursor: pointer; flex: 1; font-weight: 500; display: flex; justify-content: center; align-items: center; gap: 4px;
        }
        .nav-link.active { color: #7047eb; font-weight: bold; }

        .container { 
            padding: 6px; 
            height: calc(100% - 38px); 
            box-sizing: border-box;
            display: flex; flex-direction: column;
        }
        .tab-panel { display: none; height: 100%; width: 100%; overflow: hidden; }
        .tab-panel.active { display: flex; flex-direction: column; height: 100%; gap: 4px; }

        .search-container { display: flex; gap: 4px; height: 30px; flex-shrink: 0; align-items: center; }
        .search-bar { flex-grow: 1; padding: 0 8px; height: 100%; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-size: 11px; box-sizing: border-box; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 10px; height: 100%; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        /* Integrated Chart Header Row matching TradingView layout */
        .tv-custom-tools-row {
            display: flex; background: #15171c; border: 1px solid #212630; border-radius: 4px;
            padding: 2px 6px; height: 28px; align-items: center; justify-content: space-between; flex-shrink: 0; margin-bottom: 2px;
        }
        .tv-left-group { display: flex; gap: 8px; font-size: 11px; color: #808a9d; align-items: center; }
        .tv-tool-btn { background: #212630; border: 1px solid #363c4e; color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 3px; cursor: pointer; font-weight: bold; }
        .tv-right-camera { font-size: 12px; opacity: 0.8; }

        .screen-layout { display: flex; flex-direction: column; gap: 4px; flex-grow: 1; overflow: hidden; }
        .chart-box { width: 100%; height: 52%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; flex-shrink: 0; }
        
        /* AI Layout Section */
        .ai-exchange-box { 
            width: 100%; height: 48%; background: #15171c; 
            border: 1px solid #212630; border-radius: 6px; padding: 6px; 
            box-sizing: border-box; display: flex; flex-direction: column; 
            overflow: hidden; justify-content: space-between;
        }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; padding-bottom: 2px; flex-shrink: 0; }
        .ai-badge { padding: 1px 4px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #0ecb81; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.35; overflow-y: auto; flex-grow: 1; background: #101114; padding: 6px; border-radius: 4px; border: 1px solid #1f2226; margin-bottom: 4px; }
        .ai-report-line { margin-bottom: 2px; border-bottom: 1px dashed #212630; padding-bottom: 1px; }
        .ai-highlight { color: #f0a500; font-weight: bold; }

        .chat-input-bar { display: flex; gap: 4px; border-top: 1px solid #212630; padding-top: 4px; height: 30px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 8px; background: #0b0c10; border: 1px solid #212630; border-radius: 4px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; }

        /* News Cards Styles */
        .news-wrapper { overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 6px; }
        .news-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 10px; }
        .news-title { font-size: 12px; font-weight: 500; line-height: 1.4; color: #fff; }
        .news-time { font-size: 10px; color: #808a9d; margin-top: 4px; }

        /* Dynamic Full Screen Setup rules */
        body.fullscreen-active .top-navbar,
        body.fullscreen-active .search-container,
        body.fullscreen-active .ai-exchange-box { display: none !important; }
        body.fullscreen-active .container { padding: 0 !important; margin: 0 !important; height: 100% !important; width: 100% !important; }
        body.fullscreen-active .screen-layout { height: calc(100% - 30px) !important; }
        body.fullscreen-active .chart-box { height: 100% !important; border: none; border-radius: 0; }
    </style>
</head>
<body>

    <div class="top-navbar">
        <div class="nav-link" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">🏠 Home</div>
        <div class="nav-link" id="btn-news" onclick="tabEngine('news-ui', 'btn-news')">📰 News</div>
        <div class="nav-link active" id="btn-chart" onclick="tabEngine('chart-ui', 'btn-chart')">📊 Charts & AI</div>
    </div>

    <div class="container">
        <div id="home-ui" class="tab-panel">
            <div style="padding: 10px; color: #808a9d; font-size: 11px;">Select Charts & AI tab to configure positions.</div>
        </div>

        <div id="news-ui" class="tab-panel">
            <div class="news-wrapper" id="news-target-feed"></div>
        </div>

        <div id="chart-ui" class="tab-panel active">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="Symbol...">
                <button class="search-trigger" onclick="renderTradingCore()">Search</button>
            </div>

            <div class="tv-custom-tools-row">
                <div class="tv-left-group">
                    <span>📈 1h</span>
                    <span>🗠 Indicators</span>
                </div>
                <button class="tv-tool-btn" id="fs-toggle-node" onclick="switchViewMode()">🔍 Full Screen Mode</button>
                <div class="tv-right-camera">📷</div>
            </div>

            <div class="screen-layout">
                <div class="chart-box" id="tv-widget-frame"></div>

                <div class="ai-exchange-box" id="ai-interact-card">
                    <div class="ai-header-panel">
                        <span style="color:#7047eb;">📊 Real-time AI Quant Insights</span>
                        <span id="ai-status-tag" class="ai-badge">BULLISH</span>
                    </div>
                    
                    <div id="ai-logs-frame" class="ai-output-logs">AI Engine initialized and active. Ask questions below...</div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Ask AI: Entry kaha par lein?">
                        <button class="chat-btn" onclick="fireQuery()">Ask</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const newsFeed = ##NEWS_DATA##;

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

        function switchViewMode() {
            const bodyNode = document.body;
            bodyNode.classList.toggle('fullscreen-active');
            const btn = document.getElementById('fs-toggle-node');
            
            if (bodyNode.classList.contains('fullscreen-active')) {
                btn.innerText = "📉 Normal View";
            } else {
                btn.innerText = "🔍 Full Screen Mode";
            }
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin);
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
            logBox.innerHTML = "⏳ <i>AI processing requested matrix configurations...</i>";
            
            setTimeout(function() {
                let aiResponse = "";
                if (val.includes("entry") || val.includes("kaha par") || val.includes("trade") || val.includes("kaha banau")) {
                    aiResponse = '<div class="ai-report-line" style="color: #0ecb81; font-weight: bold;">✅ Bullish Setup Tracked</div>' +
                                 '<div class="ai-report-line">🟢 <b>Optimal Entry Zone:</b> Consolidation pullback at immediate block support levels.</div>' +
                                 '<div class="ai-report-line">🎯 <b>Targets:</b> Overhead resistance liquidity pockets.</div>' +
                                 '<div class="ai-report-line">🛡️ <b>Invalidation (SL):</b> Structural invalidation below immediate hourly swing low.</div>';
                } else {
                    aiResponse = '<div class="ai-report-line">🤖 <b>AI Bias:</b> Asset distribution profile suggests strong local defensive blocks. Volume profiling remains steady.</div>';
                }

                logBox.innerHTML = '<div class="ai-report-line" style="color: #7047eb; font-weight: bold;">💬 Ask: "' + originalPrompt + '"</div>' + aiResponse;
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
            document.getElementById('news-target-feed').innerHTML = newsFeed.map(n => '<div class="news-card"><div class="news-title">' + n.title + '</div><div class="news-time">' + n.time + '</div></div>').join('');
            renderTradingCore();
        }
    </script>
</body>
</html>
"""

dashboard_html = dashboard_html.replace("##TOP_TICKERS##", top_cards_json)
dashboard_html = dashboard_html.replace("##COINS_LIST##", coins_list_json)
dashboard_html = dashboard_html.replace("##NEWS_DATA##", news_json)

st.components.v1.html(dashboard_html, height=580, scrolling=False)
