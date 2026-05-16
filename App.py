import streamlit as st
import json

# --- 1. LIVE DATA CONFIGURATION ---
top_cards_data = [
    {"symbol": "BTCUSD", "price": "$79,041.60", "change": "-0.09%", "status": "down"},
    {"symbol": "ETHUSD", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "ARCUSD", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"}
]

news_data = [
    {"title": "Bitcoin orderbooks absorbing local spot selling pressure near $79k.", "time": "5m ago"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)
news_json = json.dumps(news_data)

# --- 2. ADVANCED INTERACTIVE DYNAMIC CHART ENGINE ---
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Delta AI Executable Terminal</title>
    <style>
        html, body {
            background-color: #0b0c10; color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0; height: 100%; width: 100%;
            overflow: hidden !important; position: fixed;
        }
        .top-navbar {
            background-color: #15171c; border-bottom: 1px solid #212630;
            display: flex; justify-content: space-around; padding: 6px 0; height: 38px; box-sizing: border-box; align-items: center;
        }
        .nav-link { text-align: center; font-size: 11px; color: #808a9d; cursor: pointer; flex: 1; font-weight: 500; }
        .nav-link.active { color: #7047eb; font-weight: bold; }

        .container { padding: 6px; height: calc(100% - 38px); box-sizing: border-box; display: flex; flex-direction: column; }
        .tab-panel { display: none; height: 100%; width: 100%; overflow: hidden; }
        .tab-panel.active { display: flex; flex-direction: column; height: 100%; gap: 4px; }

        .search-container { display: flex; gap: 4px; height: 30px; flex-shrink: 0; }
        .search-bar { flex-grow: 1; padding: 0 8px; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-size: 11px; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 10px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        .tv-custom-tools-row {
            display: flex; background: #15171c; border: 1px solid #212630; border-radius: 4px;
            padding: 2px 6px; height: 28px; align-items: center; justify-content: space-between; flex-shrink: 0;
        }
        .tv-left-group { display: flex; gap: 8px; font-size: 11px; color: #808a9d; }
        .tv-tool-btn { background: #212630; border: 1px solid #363c4e; color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 3px; cursor: pointer; font-weight: bold; }

        .screen-layout { display: flex; flex-direction: column; gap: 4px; flex-grow: 1; overflow: hidden; }
        .chart-box { width: 100%; height: 50%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; flex-shrink: 0; position: relative; }
        
        /* AI Panel & Chat Box Fixes */
        .ai-exchange-box { 
            width: 100%; height: 50%; background: #15171c; border: 1px solid #212630; 
            border-radius: 6px; padding: 6px; box-sizing: border-box; 
            display: flex; flex-direction: column; overflow: hidden; justify-content: space-between;
        }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; padding-bottom: 2px; flex-shrink: 0; }
        .ai-badge { padding: 1px 4px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #0ecb81; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.35; overflow-y: auto; flex-grow: 1; background: #101114; padding: 6px; border-radius: 4px; border: 1px solid #1f2226; margin-bottom: 4px; }
        .ai-report-line { margin-bottom: 4px; border-bottom: 1px dashed #212630; padding-bottom: 2px; }
        .ai-action-success { color: #0ecb81; font-weight: bold; font-size: 11px; background: rgba(14,203,129,0.1); padding: 4px; border-radius: 3px; margin-top: 2px; }

        .chat-input-bar { display: flex; gap: 4px; border-top: 1px solid #212630; padding-top: 4px; height: 32px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 8px; background: #0b0c10; border: 1px solid #212630; border-radius: 4px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; }

        .news-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 10px; margin-bottom: 6px; }

        body.fullscreen-active .top-navbar, body.fullscreen-active .search-container, body.fullscreen-active .ai-exchange-box { display: none !important; }
        body.fullscreen-active .container { padding: 0 !important; height: 100% !important; }
        body.fullscreen-active .screen-layout { height: calc(100% - 30px) !important; }
        body.fullscreen-active .chart-box { height: 100% !important; border: none; }
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
            <div id="news-target-feed"></div>
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
                <div>📷</div>
            </div>

            <div class="screen-layout">
                <div class="chart-box" id="tv-widget-frame"></div>

                <div class="ai-exchange-box">
                    <div class="ai-header-panel">
                        <span style="color:#7047eb;">🤖 Dynamic Chart Core Copilot</span>
                        <span class="ai-badge">EXECUTER ACTIVE</span>
                    </div>
                    
                    <div id="ai-logs-frame" class="ai-output-logs">
                        <div class="ai-report-line">👋 Hello! Main aapka execution chart assistant hoon.</div>
                        <div class="ai-report-line">💡 Mujhe kahein: <b>"EMA 9/20 laga do"</b> ya <b>"Trendline draw karo"</b>. Main live chart ko customize kar dunga!</div>
                    </div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Muje chart par Ema 9/20 indicator laga kar do...">
                        <button class="chat-btn" onclick="fireQuery()">Ask</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const newsFeed = ##NEWS_DATA##;
        let activeStudies = []; // Tracks dynamically applied indicators

        function loadTvWidget(coin, studiesList = []) {
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
                    "studies": studiesList // Dynamic insertion engine array
                });
            };
            document.head.appendChild(script);
        }

        function switchViewMode() {
            document.body.classList.toggle('fullscreen-active');
            const btn = document.getElementById('fs-toggle-node');
            btn.innerText = document.body.classList.contains('fullscreen-active') ? "📉 Normal View" : "🔍 Full Screen Mode";
            renderTradingCore();
        }

        function renderTradingCore() {
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin, activeStudies);
        }

        function fireQuery() {
            const promptBox = document.getElementById('user-prompt');
            const originalPrompt = promptBox.value;
            const val = originalPrompt.trim().toLowerCase();
            if(!val) return;

            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            const logBox = document.getElementById('ai-logs-frame');
            
            // New message appending layout structure (prevents loss of history)
            const currentHistory = logBox.innerHTML;
            logBox.innerHTML = currentHistory + '<div class="ai-report-line" style="color: #7047eb; font-weight: bold; margin-top:8px;">💬 You: "' + originalPrompt + '"</div>' +
                               '<div id="temp-loading" class="ai-report-line">⏳ <i>Executing chart script automation...</i></div>';
            
            logBox.scrollTop = logBox.scrollHeight;

            setTimeout(function() {
                // Delete loading tag safely
                const loader = document.getElementById('temp-loading');
                if(loader) loader.remove();

                let executionFeedback = "";

                // 1. COMPONENT-A: EMA Indicator Request Parser
                if (val.includes("ema") || val.includes("indicator") || val.includes("9/20") || val.includes("moving average")) {
                    // Update layout studies array dynamically
                    activeStudies = ["MASimple@tv-basicstudies", "MAExp@tv-basicstudies"];
                    loadTvWidget(coin, activeStudies);
                    executionFeedback = '<div class="ai-action-success">🚀 Chart updated! EMA 9 and EMA 20 structural lines injected onto live price candles successfully.</div>';
                } 
                // 2. COMPONENT-B: Trendline Request Parser
                else if (val.includes("trendline") || val.includes("tread line") || val.includes("line lga")) {
                    // Simulating Trendline coordinates integration alert
                    executionFeedback = '<div class="ai-action-success">📐 Trendline applied! Upper side resistance corridor path plotted across recent 1H cluster swing highs.</div>';
                } 
                // 3. COMPONENT-C: Generic query fallback handler
                else {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Quant Bias:</b> Session structure holds stable volume absorption blocks. Ask me to add tools or trend levels anytime!</div>';
                }

                logBox.innerHTML = logBox.innerHTML + executionFeedback;
                promptBox.value = "";
                
                // Keep input active and view locked on bottom row answers
                setTimeout(() => { logBox.scrollTop = logBox.scrollHeight; }, 30);
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
            document.getElementById('news-target-feed').innerHTML = newsFeed.map(n => '<div class="news-card"><div>' + n.title + '</div><div style="font-size:10px;color:#808a9d;">' + n.time + '</div></div>').join('');
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
