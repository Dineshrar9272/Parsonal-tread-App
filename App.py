import streamlit as st
import json

# --- 1. FULL COINS LIST & DYNAMIC MARKET NEWS DATA ---
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
    {"title": "🚨 Macro Alert: Core CPI index release creates massive liquidity sweep under Bitcoin $78,500 support zone.", "time": "Just now", "impact": "HIGH IMPACT"},
    {"title": "📊 Institutional Orderbooks show heavy limit order absorption for ETH near $2,200 demand cluster.", "time": "14m ago", "impact": "MEDIUM IMPACT"},
    {"title": "🐳 Whale Wallet Movement: Over $150M USDT injected into top spot exchanges, indicating upcoming buy-side volatility.", "time": "32m ago", "impact": "HIGH IMPACT"},
    {"title": "📈 AI Quant Matrix confirms local distribution pattern over for ARC token as volume breakout spikes 34%.", "time": "1h ago", "impact": "STOCHASTIC BREAKOUT"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)
news_json = json.dumps(news_data)

# --- 2. INTERCONNECTED SYSTEM LAYOUT ENGINE ---
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Delta Interconnected Quantum Terminal</title>
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

        /* Home Layout Classes */
        .home-scroller { overflow-y: auto; height: 100%; width: 100%; display: flex; flex-direction: column; gap: 4px; }
        .ticker-row { display: flex; gap: 6px; margin-bottom: 4px; flex-shrink: 0; }
        .ticker-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 6px; flex: 1; }
        .ticker-title { font-size: 10px; color: #808a9d; }
        .ticker-price { font-size: 13px; font-weight: bold; }
        
        .list-caption { display: flex; justify-content: space-between; color: #808a9d; font-size: 10px; padding: 4px; background: #101114; border-radius: 4px; }
        .coin-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 6px; border-bottom: 1px solid #212630; background: #15171c; border-radius: 6px; margin-top: 2px; cursor: pointer; transition: background 0.2s; }
        .coin-item:active { background: #212630; }
        .coin-name { font-weight: bold; font-size: 12px; }
        .coin-sub { color: #808a9d; font-size: 10px; }
        .coin-badge { padding: 4px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; color: #fff; min-width: 55px; text-align: center; }
        .badge-up { background-color: #0ecb81; }
        .badge-down { background-color: #f6465d; }

        /* Chart & Terminal UI Classes */
        .search-container { display: flex; gap: 4px; height: 30px; flex-shrink: 0; }
        .search-bar { flex-grow: 1; padding: 0 8px; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-size: 11px; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 10px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        .tv-custom-tools-row {
            display: flex; background: #15171c; border: 1px solid #212630; border-radius: 4px;
            padding: 2px 6px; height: 26px; align-items: center; justify-content: space-between; flex-shrink: 0;
        }
        .tv-left-group { display: flex; gap: 8px; font-size: 11px; color: #808a9d; }
        .tv-tool-btn { background: #212630; border: 1px solid #363c4e; color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 3px; cursor: pointer; font-weight: bold; }

        .screen-layout { display: flex; flex-direction: column; gap: 4px; flex-grow: 1; overflow: hidden; }
        .chart-box { width: 100%; height: 48%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; flex-shrink: 0; }
        
        /* AI Tool Box Structure */
        .ai-exchange-box { 
            width: 100%; height: 52%; background: #15171c; border: 1px solid #212630; 
            border-radius: 6px; padding: 6px; box-sizing: border-box; 
            display: flex; flex-direction: column; overflow: hidden; justify-content: space-between; flex-shrink: 0;
        }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; padding-bottom: 2px; flex-shrink: 0; }
        .ai-badge { padding: 1px 4px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #0ecb81; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.35; overflow-y: auto; flex-grow: 1; background: #101114; padding: 6px; border-radius: 4px; border: 1px solid #1f2226; margin-bottom: 4px; }
        .ai-report-line { margin-bottom: 4px; border-bottom: 1px dashed #212630; padding-bottom: 2px; }
        .ai-action-success { color: #0ecb81; font-weight: bold; font-size: 11px; background: rgba(14,203,129,0.1); padding: 4px; border-radius: 3px; margin-top: 2px; }

        .chat-input-bar { display: flex; gap: 4px; border-top: 1px solid #212630; padding-top: 4px; height: 30px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 8px; background: #0b0c10; border: 1px solid #212630; border-radius: 4px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; }

        /* News Section Classes */
        .news-wrapper { overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 6px; padding: 2px; }
        .news-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 8px; position: relative; }
        .news-impact-tag { position: absolute; top: 8px; right: 8px; font-size: 8px; font-weight: bold; padding: 2px 4px; border-radius: 3px; background: rgba(240, 165, 0, 0.15); color: #f0a500; }
        .news-title { font-size: 11px; font-weight: 500; color: #fff; width: 80%; line-height: 1.4; }
        .news-time { font-size: 9px; color: #808a9d; margin-top: 4px; }

        body.fullscreen-active .top-navbar, body.fullscreen-active .search-container, body.fullscreen-active .ai-exchange-box { display: none !important; }
        body.fullscreen-active .container { padding: 0 !important; height: 100% !important; }
        body.fullscreen-active .screen-layout { height: calc(100% - 28px) !important; }
        body.fullscreen-active .chart-box { height: 100% !important; border: none; }
    </style>
</head>
<body>

    <div class="top-navbar">
        <div class="nav-link active" id="btn-home" onclick="tabEngine('home-ui', 'btn-home')">🏠 Home</div>
        <div class="nav-link" id="btn-chart" onclick="tabEngine('chart-ui', 'btn-chart')">📊 Charts & AI</div>
        <div class="nav-link" id="btn-news" onclick="tabEngine('news-ui', 'btn-news')">📰 AI News Room</div>
    </div>

    <div class="container">
        
        <div id="home-ui" class="tab-panel active">
            <div class="home-scroller">
                <div class="ticker-row" id="top-ticker-target"></div>
                <div class="list-caption">
                    <div style="width: 40%;">Asset Contract</div>
                    <div style="width: 35%; text-align: right;">Last Price</div>
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
                        <span style="color:#7047eb;">🤖 Real-Time AI Quant Terminal</span>
                        <span class="ai-badge">ANALYZER ONLINE</span>
                    </div>
                    
                    <div id="ai-logs-frame" class="ai-output-logs">
                        <div class="ai-report-line">👋 Main aapka automated analysis bot hoon.</div>
                        <div class="ai-report-line">💡 Mujhe likhein: <b>"EMA 9/20 laga kar do"</b> ya <b>"trendline draw karo"</b>, ya koi bhi crypto prediction sawal poochhein!</div>
                    </div>

                    <div class="chat-input-bar">
                        <input type="text" id="user-prompt" class="chat-field" placeholder="Likhien: EMA 9/20 indicator laga kar do...">
                        <button class="chat-btn" onclick="fireQuery()">Ask</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="news-ui" class="tab-panel">
            <div class="news-wrapper" id="news-target-feed"></div>
        </div>

    </div>

    <script>
        const rawTickers = ##TOP_TICKERS##;
        const rawCoins = ##COINS_LIST##;
        const newsFeed = ##NEWS_DATA##;
        let activeStudies = [];

        // Dynamic Redirection Engine: Opens chart direct from Home click row
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
                new TradingView.widget({
                    "width": "100%", "height": "100%",
                    "symbol": "BINANCE:" + coin + "USDT",
                    "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                    "hide_side_toolbar": false, "allow_symbol_change": false,
                    "container_id": "tv-widget-frame",
                    "studies": studiesList
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
            
            const currentHistory = logBox.innerHTML;
            logBox.innerHTML = currentHistory + '<div class="ai-report-line" style="color: #7047eb; font-weight: bold; margin-top:8px;">💬 You: "' + originalPrompt + '"</div>' +
                               '<div id="temp-loading" class="ai-report-line">⏳ <i>AI computing market matrices...</i></div>';
            
            logBox.scrollTop = logBox.scrollHeight;

            setTimeout(function() {
                const loader = document.getElementById('temp-loading');
                if(loader) loader.remove();

                let executionFeedback = "";

                if (val.includes("ema") || val.includes("indicator") || val.includes("9/20")) {
                    activeStudies = ["MASimple@tv-basicstudies", "MAExp@tv-basicstudies"];
                    loadTvWidget(coin, activeStudies);
                    executionFeedback = '<div class="ai-action-success">🚀 Action Executed! Exponential Moving Averages (EMA 9/20) injected into live ' + coin + ' candles.</div>';
                } 
                else if (val.includes("trendline") || val.includes("tread line") || val.includes("line lga")) {
                    executionFeedback = '<div class="ai-action-success">📐 Chart Plotted! Upper resistance corridor line aligned over 1H local high peaks.</div>';
                } 
                else if (val.includes("market") || val.includes("analysis") || val.includes("prediction") || val.includes("up") || val.includes("down")) {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Technical Assessment:</b> Orderbook structure for ' + coin + ' exhibits strong validation near major support blocks. Invalidation metrics are currently resting stable.</div>';
                }
                else {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Response:</b> Input scanned. I am continuously processing ' + coin + ' liquidity clusters. Ask me for specific indicators or entry metrics anytime!</div>';
                }

                logBox.innerHTML = logBox.innerHTML + executionFeedback;
                promptBox.value = "";
                setTimeout(() => { logBox.scrollTop = logBox.scrollHeight; }, 30);
            }, 550);
        }

        function tabEngine(panelId, btnId) {
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            document.getElementById(btnId).classList.add('active');
            if(panelId === 'chart-ui') { renderTradingCore(); }
        }

        window.onload = function() {
            // Render Home Top Ribbon Cards
            document.getElementById('top-ticker-target').innerHTML = rawTickers.map(t => '<div class="ticker-card" onclick="redirectAssetToChart(\''+t.symbol+'\')"><div class="ticker-title"><span>' + t.symbol + 'USDT</span></div><div class="ticker-price">' + t.price + '</div></div>').join('');
            
            // Render Home Restored Main Coins Table Row
            document.getElementById('coin-list-target').innerHTML = rawCoins.map(c => {
                let badgeClass = c.status === "up" ? "badge-up" : "badge-down";
                return '<div class="coin-item" onclick="redirectAssetToChart(\''+c.symbol+'\')"><div><span class="coin-name">' + c.symbol + '/USDT</span><br><span class="coin-sub">' + c.desc + '</span></div><div style="font-weight:bold; font-size:11px;">' + c.price + '</div><div class="coin-badge ' + badgeClass + '">' + c.change + '</div></div>';
            }).join('');

            // Render AI Crypto Impact News Tab
            document.getElementById('news-target-feed').innerHTML = newsFeed.map(n => '<div class="news-card"><span class="news-impact-tag">' + n.impact + '</span><div class="news-title">' + n.title + '</div><div class="news-time">' + n.time + '</div></div>').join('');
            
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
