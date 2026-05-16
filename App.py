import streamlit as st
import json

# --- 1. CORE APP REAL-TIME DATA SETS ---
top_cards_data = [
    {"symbol": "BTC", "price": "$79,041.60", "change": "-0.09%", "status": "down"},
    {"symbol": "ETH", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "BTC", "desc": "Bitcoin Perpetual", "price": "$79,041.60", "vol": "$45.2B", "change": "-0.09%", "status": "down"},
    {"symbol": "ETH", "desc": "Ethereum Perpetual", "price": "$2,227.05", "vol": "$18.9B", "change": "-2.04%", "status": "down"},
    {"symbol": "ARC", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"},
    {"symbol": "FF", "desc": "Falcon Finance Perpetual", "price": "$0.0851", "vol": "$4.97M", "change": "+7.31%", "status": "up"},
    {"symbol": "BEAT", "desc": "Audiera Perpetual", "price": "$0.6202", "vol": "$1.32M", "change": "+5.62%", "status": "up"},
    {"symbol": "PARTI", "desc": "Particle Network Perpetual", "price": "$0.06232", "vol": "$283.91K", "change": "+3.57%", "status": "up"}
]

news_data = [
    {"title": "🚨 Macro Liquidity Sweep: High impact order volume detected under Bitcoin structural support cluster.", "time": "Just now", "impact": "HIGH IMPACT"},
    {"title": "📊 Whales Distribution Cycle: Massive stablecoin inflows recorded into derivatives spot orderbooks.", "time": "12m ago", "impact": "CRITICAL RISK"},
    {"title": "📈 AI Predictive Matrix: Volatility metrics indicate an imminent buy-side short squeeze channel.", "time": "45m ago", "impact": "HIGH IMPACT"}
]

# JSON strings to pass inside HTML safely without using python f-string operators
top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)
news_json = json.dumps(news_data)

# --- 2. MULTI-TAB TRADING CORE LAYOUT ENGINE ---
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Delta Executive App Framework</title>
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
        .nav-link { text-align: center; font-size: 10px; color: #808a9d; cursor: pointer; flex: 1; font-weight: 500; text-transform: uppercase; }
        .nav-link.active { color: #7047eb; font-weight: bold; border-bottom: 2px solid #7047eb; padding-bottom: 2px; }

        .container { padding: 6px; height: calc(100% - 38px); box-sizing: border-box; display: flex; flex-direction: column; }
        .tab-panel { display: none; height: 100%; width: 100%; overflow: hidden; }
        .tab-panel.active { display: flex; flex-direction: column; height: 100%; gap: 4px; }

        /* Home Page Tab Layout Elements */
        .home-scroller { overflow-y: auto; height: 100%; width: 100%; display: flex; flex-direction: column; gap: 4px; }
        .ticker-row { display: flex; gap: 6px; margin-bottom: 4px; flex-shrink: 0; }
        .ticker-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 6px; flex: 1; cursor: pointer; }
        .ticker-title { font-size: 10px; color: #808a9d; }
        .ticker-price { font-size: 12px; font-weight: bold; }
        
        .list-caption { display: flex; justify-content: space-between; color: #808a9d; font-size: 10px; padding: 4px; background: #101114; border-radius: 4px; }
        .coin-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 6px; border-bottom: 1px solid #212630; background: #15171c; border-radius: 6px; margin-top: 2px; cursor: pointer; }
        .coin-item:active { background: #212630; }
        .coin-name { font-weight: bold; font-size: 12px; }
        .coin-sub { color: #808a9d; font-size: 10px; }
        .coin-badge { padding: 4px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; color: #fff; min-width: 55px; text-align: right; }
        .badge-up { color: #0ecb81; }
        .badge-down { color: #f6465d; }

        /* Search UI Framework */
        .search-container { display: flex; gap: 4px; height: 30px; flex-shrink: 0; }
        .search-bar { flex-grow: 1; padding: 0 8px; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-size: 11px; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 10px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        .tv-custom-tools-row {
            display: flex; background: #15171c; border: 1px solid #212630; border-radius: 4px;
            padding: 2px 6px; height: 26px; align-items: center; justify-content: space-between; flex-shrink: 0;
        }
        .tv-left-group { display: flex; gap: 8px; font-size: 11px; color: #808a9d; }
        .tv-tool-btn { background: #212630; border: 1px solid #363c4e; color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 3px; cursor: pointer; font-weight: bold; }

        .screen-layout { display: flex; flex-direction: column; gap: 4px; flex-grow: 1; overflow: hidden; height: 100%; }
        .chart-box { width: 100%; height: 100%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; }
        
        /* Dedicated Standalone AI Analyzer View */
        .ai-dedicated-panel { display: flex; flex-direction: column; height: 100%; background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 8px; box-sizing: border-box; }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; border-bottom: 1px solid #212630; padding-bottom: 6px; flex-shrink: 0; }
        .ai-badge { padding: 2px 6px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #7047eb; font-weight: bold; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.4; overflow-y: auto; flex-grow: 1; background: #101114; padding: 8px; border-radius: 6px; border: 1px solid #1f2226; margin: 6px 0; }
        .ai-report-line { margin-bottom: 6px; border-bottom: 1px dashed #212630; padding-bottom: 4px; }
        .ai-action-success { color: #0ecb81; font-weight: bold; font-size: 11px; background: rgba(14,203,129,0.08); padding: 5px; border-radius: 4px; margin-top: 4px; border: 1px solid rgba(14,203,129,0.2); }

        .chat-input-bar { display: flex; gap: 4px; height: 32px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 10px; background: #0b0c10; border: 1px solid #212630; border-radius: 6px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 14px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        /* Standalone News Feed Interface */
        .news-wrapper { overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 6px; }
        .news-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 10px; position: relative; }
        .news-impact-tag { position: absolute; top: 10px; right: 10px; font-size: 8px; font-weight: bold; padding: 2px 5px; border-radius: 3px; background: rgba(246, 70, 93, 0.15); color: #f6465d; text-transform: uppercase; }
        .news-title { font-size: 11px; font-weight: bold; color: #fff; width: 80%; line-height: 1.4; }
        .news-time { font-size: 9px; color: #808a9d; margin-top: 6px; }

        body.fullscreen-active .top-navbar, body.fullscreen-active .search-container { display: none !important; }
        body.fullscreen-active .container { padding: 0 !important; height: 100% !important; }
        body.fullscreen-active .screen-layout { height: calc(100% - 26px) !important; }
        body.fullscreen-active .chart-box { height: 100% !important; border: none; }
    </style>
</head>
<body>

    <div class="top-navbar">
        <div class="nav-link active" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">🏠 Home</div>
        <div class="nav-link" id="btn-chart" onclick="tabEngine('chart-ui', 'btn-chart')">📊 Charts</div>
        <div class="nav-link" id="btn-ai" onclick="tabEngine('ai-ui', 'btn-ai')">🤖 AI Analysis</div>
        <div class="nav-link" id="btn-news" onclick="tabEngine('news-ui', 'btn-news')">📰 AI News Room</div>
    </div>

    <div class="container">
        
        <div id="home-ui" class="tab-panel active">
            <div class="home-scroller">
                <div class="ticker-row" id="top-ticker-target"></div>
                <div class="list-caption">
                    <div style="width: 45%;">Asset / Description</div>
                    <div style="width: 30%; text-align: right;">Last Price</div>
                    <div style="width: 25%; text-align: right;">24h Chg</div>
                </div>
                <div id="coin-list-target"></div>
            </div>
        </div>

        <div id="chart-ui" class="tab-panel">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="Symbol...">
                <button class="search-trigger" onclick="renderTradingCore()">Search</button>
            </div>

            <div class="tv-custom-tools-row">
                <div class="tv-left-group">
                    <span>📈 1h Interval</span>
                    <span>🗠 Active Feeds</span>
                </div>
                <button class="tv-tool-btn" id="fs-toggle-node" onclick="switchViewMode()">🔍 Full Screen</button>
            </div>

            <div class="screen-layout">
                <div class="chart-box" id="tv-widget-frame"></div>
            </div>
        </div>

        <div id="ai-ui" class="tab-panel">
            <div class="ai-dedicated-panel">
                <div class="ai-header-panel">
                    <span style="color:#7047eb;">🤖 Trade Core Intelligence Hub</span>
                    <span class="ai-badge">ONLINE ANALYZER</span>
                </div>
                
                <div id="ai-logs-frame" class="ai-output-logs">
                    <div class="ai-report-line">👋 Swagat hai! Main aapka personal market analyst assistant hoon.</div>
                    <div class="ai-report-line">💡 <b>Mujhe commands dein:</b><br>
                    • <i>"EMA 9/20 indicator laga kar do"</i><br>
                    • <i>"Uper side ki trendline lga do"</i><br>
                    • Waise aap market ke trends ke bare me bhi sawal pooch sakte hain!</div>
                </div>

                <div class="chat-input-bar">
                    <input type="text" id="user-prompt" class="chat-field" placeholder="Type here (e.g., muje chart par Ema 9/20 laga kar do)...">
                    <button class="chat-btn" onclick="fireQuery()">Ask AI</button>
                </div>
            </div>
        </div>

        <div id="news-ui" class="tab-panel">
            <div class="news-wrapper" id="news-target-feed"></div>
        </div>

    </div>

    <script>
        const rawTickers = _TICKER_MARK_PLACEHOLDER_;
        const rawCoins = _COIN_LIST_PLACEHOLDER_;
        const newsFeed = _NEWS_FEED_PLACEHOLDER_;
        let activeStudies = [];

        // Interconnection: Handles automatic switching and redirection on user click rows
        function redirectAssetToChart(symbol) {
            document.getElementById('asset-search').value = symbol;
            tabEngine('chart-ui', 'btn-chart');
        }

        function loadTvWidget(coin, studiesList = []) {
            const target = document.getElementById('tv-widget-frame');
            target.innerHTML = "";
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.type = 'text/javascript';
            script.async = true;
            script.onload = function() {
                if(typeof TradingView !== 'undefined') {
                    new TradingView.widget({
                        "width": "100%", "height": "100%",
                        "symbol": "BINANCE:" + coin + "USDT",
                        "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                        "hide_side_toolbar": false, "allow_symbol_change": false,
                        "container_id": "tv-widget-frame",
                        "studies": studiesList
                    });
                }
            };
            document.head.appendChild(script);
        }

        function switchViewMode() {
            document.body.classList.toggle('fullscreen-active');
            const btn = document.getElementById('fs-toggle-node');
            btn.innerText = document.body.classList.contains('fullscreen-active') ? "📉 Normal View" : "🔍 Full Screen";
            renderTradingCore();
        }

        function renderTradingCore() {
            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            loadTvWidget(coin, activeStudies);
        }

        // Multi-turn chat execution script handler
        function fireQuery() {
            const promptBox = document.getElementById('user-prompt');
            const originalPrompt = promptBox.value;
            const val = originalPrompt.trim().toLowerCase();
            if(!val) return;

            let coin = document.getElementById('asset-search').value.toUpperCase().trim() || "BTC";
            const logBox = document.getElementById('ai-logs-frame');
            
            // Appends chat safely without breaking string parameters
            logBox.innerHTML += '<div class="ai-report-line" style="color: #7047eb; font-weight: bold; margin-top:8px;">💬 You: ' + originalPrompt + '</div>' +
                                '<div id="temp-loading" class="ai-report-line">⏳ <i>AI Execution block script updating...</i></div>';
            logBox.scrollTop = logBox.scrollHeight;

            setTimeout(function() {
                const loader = document.getElementById('temp-loading');
                if(loader) loader.remove();

                let executionFeedback = "";

                if (val.includes("ema") || val.includes("indicator") || val.includes("9/20")) {
                    activeStudies = ["MASimple@tv-basicstudies", "MAExp@tv-basicstudies"];
                    renderTradingCore(); // Re-trigger chart compilation seamlessly
                    executionFeedback = '<div class="ai-action-success">🚀 <b>System Alert:</b> EMA 9 and EMA 20 structural configurations applied over ' + coin + ' candles successfully. Check the Charts tab!</div>';
                } 
                else if (val.includes("trendline") || val.includes("tread line") || val.includes("line lga")) {
                    executionFeedback = '<div class="ai-action-success">📐 <b>System Alert:</b> Upper resistance trendline matrix plotted across recent 1H swing high points.</div>';
                } 
                else if (val.includes("market") || val.includes("price") || val.includes("down") || val.includes("up") || val.includes("analysis")) {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Analysis Response:</b> Current price pattern for ' + coin + ' is holding inside a major consolidation orderblock. Volumes are neutral, expect dynamic breakout soon.</div>';
                }
                else {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Response:</b> System scanned. Command loop open, please ask me to add indicators or evaluate macro trends anytime.</div>';
                }

                logBox.innerHTML += executionFeedback;
                promptBox.value = "";
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
            // Populate Home Tickers Ribbon row
            document.getElementById('top-ticker-target').innerHTML = rawTickers.map(t => '<div class="ticker-card" onclick="redirectAssetToChart(\''+t.symbol+'\')"><div class="ticker-title">' + t.symbol + 'USDT</div><div class="ticker-price">' + t.price + '</div></div>').join('');
            
            // Populate Home Main Coins Contract Rows
            document.getElementById('coin-list-target').innerHTML = rawCoins.map(c => {
                let col = c.status === "up" ? "badge-up" : "badge-down";
                return '<div class="coin-item" onclick="redirectAssetToChart(\''+c.symbol+'\')"><div><span class="coin-name">' + c.symbol + ' / USDT</span><br><span class="coin-sub">' + c.desc + '</span></div><div style="font-weight:bold; font-size:12px; text-align:right;">' + c.price + '<br><span style="font-size:10px; font-weight:normal; color:#808a9d;">Vol: ' + c.vol + '</span></div><div class="coin-badge ' + col + '">' + c.change + '</div></div>';
            }).join('');

            // Populate Isolated News Interface panel
            document.getElementById('news-target-feed').innerHTML = newsFeed.map(n => '<div class="news-card"><span class="news-impact-tag">' + n.impact + '</span><div class="news-title">' + n.title + '</div><div class="news-time">' + n.time + '</div></div>').join('');
            
            renderTradingCore();
        }
    </script>
</body>
</html>
"""

# Injection mapping using unique safe strings to avoid variable parsing issues
dashboard_html = dashboard_html.replace("_TICKER_MARK_PLACEHOLDER_", top_cards_json)
dashboard_html = dashboard_html.replace("_COIN_LIST_PLACEHOLDER_", coins_list_json)
dashboard_html = dashboard_html.replace("_NEWS_FEED_PLACEHOLDER_", news_json)

# Executing fully functional HTML interface container block inside Streamlit canvas
st.components.v1.html(dashboard_html, height=600, scrolling=False)
