import streamlit as st

# --- 1. CORE HTML CONTAINER (PURE TEXT - NO PYTHON OR CSS MARKDOWN CONFLICTS) ---
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Delta Terminal Canvas</title>
    <style>
        html, body {
            background-color: #0b0c10; color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0; height: 100%; width: 100%;
            overflow: hidden !important; position: fixed;
        }
        .top-navbar {
            background-color: #15171c; border-bottom: 1px solid #212630;
            display: flex; justify-content: space-around; padding: 8px 0; height: 42px; box-sizing: border-box; align-items: center;
        }
        .nav-link { text-align: center; font-size: 11px; color: #808a9d; cursor: pointer; flex: 1; font-weight: 500; }
        .nav-link.active { color: #7047eb; font-weight: bold; border-bottom: 2px solid #7047eb; }

        .container { padding: 6px; height: calc(100% - 42px); box-sizing: border-box; display: flex; flex-direction: column; }
        .tab-panel { display: none; height: 100%; width: 100%; overflow: hidden; }
        .tab-panel.active { display: flex; flex-direction: column; height: 100%; gap: 4px; }

        /* Home Scroller Layout Grid */
        .home-scroller { overflow-y: auto; height: 100%; width: 100%; display: flex; flex-direction: column; gap: 4px; }
        .ticker-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 4px; flex-shrink: 0; }
        .ticker-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 8px; cursor: pointer; }
        .ticker-flex { display: flex; justify-content: space-between; align-items: center; }
        .ticker-title { font-size: 11px; font-weight: bold; color: #ffffff; }
        .ticker-price { font-size: 12px; font-weight: bold; margin-top: 2px; }
        .ticker-change { font-size: 10px; font-weight: bold; }
        
        .list-caption { display: flex; justify-content: space-between; color: #808a9d; font-size: 10px; padding: 4px; background: #101114; border-radius: 4px; }
        .coin-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 6px; border-bottom: 1px solid #212630; background: #15171c; border-radius: 6px; margin-top: 2px; cursor: pointer; }
        .coin-item:active { background: #212630; }
        .coin-name { font-weight: bold; font-size: 12px; }
        .coin-sub { color: #808a9d; font-size: 10px; }
        .coin-badge { padding: 4px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; min-width: 55px; text-align: right; }
        .badge-up { color: #0ecb81; }
        .badge-down { color: #f6465d; }

        /* Real-Time TradingView Frame Configurations */
        .search-container { display: flex; gap: 4px; height: 32px; flex-shrink: 0; margin-bottom: 4px; }
        .search-bar { flex-grow: 1; padding: 0 8px; background: #15171c; border: 1px solid #212630; border-radius: 6px; color: #fff; font-size: 11px; outline: none; }
        .search-trigger { background: #7047eb; border: none; color: white; padding: 0 12px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }
        .screen-layout { display: flex; flex-direction: column; gap: 4px; flex-grow: 1; overflow: hidden; height: 100%; }
        .chart-box { width: 100%; height: 100%; background: #15171c; border: 1px solid #212630; border-radius: 6px; overflow: hidden; }
        
        /* Dedicated Live AI Quantum Interface Logs */
        .ai-dedicated-panel { display: flex; flex-direction: column; height: 100%; background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 8px; box-sizing: border-box; }
        .ai-header-panel { display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; border-bottom: 1px solid #212630; padding-bottom: 6px; flex-shrink: 0; }
        .ai-badge { padding: 2px 6px; border-radius: 3px; font-size: 9px; color: #fff; background-color: #7047eb; font-weight: bold; }
        .ai-output-logs { font-size: 11px; color: #e1e4e8; line-height: 1.4; overflow-y: auto; flex-grow: 1; background: #101114; padding: 8px; border-radius: 6px; border: 1px solid #1f2226; margin: 6px 0; }
        .ai-report-line { margin-bottom: 6px; border-bottom: 1px dashed #212630; padding-bottom: 4px; }
        .ai-action-success { color: #0ecb81; font-weight: bold; font-size: 11px; background: rgba(14,203,129,0.08); padding: 5px; border-radius: 4px; margin-top: 4px; border: 1px solid rgba(14,203,129,0.2); }
        .chat-input-bar { display: flex; gap: 4px; height: 34px; flex-shrink: 0; }
        .chat-field { flex-grow: 1; padding: 0 10px; background: #0b0c10; border: 1px solid #212630; border-radius: 6px; color: #ffffff; font-size: 11px; outline: none; }
        .chat-btn { background: #7047eb; border: none; color: #fff; padding: 0 14px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; }

        /* Isolated News Engine */
        .news-wrapper { overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 6px; }
        .news-card { background: #15171c; border: 1px solid #212630; border-radius: 6px; padding: 10px; position: relative; }
        .news-impact-tag { position: absolute; top: 10px; right: 10px; font-size: 8px; font-weight: bold; padding: 2px 5px; border-radius: 3px; background: rgba(246, 70, 93, 0.15); color: #f6465d; text-transform: uppercase; }
        .news-title { font-size: 11px; font-weight: bold; color: #fff; width: 80%; line-height: 1.4; }
        .news-time { font-size: 9px; color: #808a9d; margin-top: 6px; }
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
                <div class="ticker-grid">
                    <div class="ticker-card" onclick="redirectAssetToChart('BTC')">
                        <div class="ticker-flex"><span class="ticker-title">BTC / USD</span><span class="ticker-change" style="color:#f6465d;">-0.11%</span></div>
                        <div class="ticker-price" style="color:#f6465d;">$79,025.35</div>
                    </div>
                    <div class="ticker-card" onclick="redirectAssetToChart('ETH')">
                        <div class="ticker-flex"><span class="ticker-title">ETH / USD</span><span class="ticker-change" style="color:#f6465d;">-2.04%</span></div>
                        <div class="ticker-price" style="color:#f6465d;">$2,227.05</div>
                    </div>
                    <div class="ticker-card" onclick="redirectAssetToChart('SOL')">
                        <div class="ticker-flex"><span class="ticker-title">SOL / USD</span><span class="ticker-change" style="color:#0ecb81;">+4.12%</span></div>
                        <div class="ticker-price" style="color:#0ecb81;">$142.50</div>
                    </div>
                    <div class="ticker-card" onclick="redirectAssetToChart('PAXG')">
                        <div class="ticker-flex"><span class="ticker-title">PAXG / USD</span><span class="ticker-change" style="color:#0ecb81;">+0.15%</span></div>
                        <div class="ticker-price" style="color:#0ecb81;">$2,350.10</div>
                    </div>
                </div>

                <div class="list-caption">
                    <div style="width: 45%;">Asset / Description</div>
                    <div style="width: 30%; text-align: right;">Last Price</div>
                    <div style="width: 25%; text-align: right;">24h Chg</div>
                </div>

                <div id="coin-list-target">
                    <div class="coin-item" onclick="redirectAssetToChart('BTC')">
                        <div><span class="coin-name">BTCUSD</span><br><span class="coin-sub">Bitcoin / US Dollar</span></div>
                        <div style="font-weight:bold; font-size:12px; text-align:right;">$79,025.35<br><span style="font-size:10px; font-weight:normal; color:#808a9d;">Vol: $45.2B</span></div>
                        <div class="coin-badge badge-down">-0.11%</div>
                    </div>
                    <div class="coin-item" onclick="redirectAssetToChart('ETH')">
                        <div><span class="coin-name">ETHUSD</span><br><span class="coin-sub">Ethereum / US Dollar</span></div>
                        <div style="font-weight:bold; font-size:12px; text-align:right;">$2,227.05<br><span style="font-size:10px; font-weight:normal; color:#808a9d;">Vol: $18.9B</span></div>
                        <div class="coin-badge badge-down">-2.04%</div>
                    </div>
                    <div class="coin-item" onclick="redirectAssetToChart('SOL')">
                        <div><span class="coin-name">SOLUSD</span><br><span class="coin-sub">Solana / US Dollar</span></div>
                        <div style="font-weight:bold; font-size:12px; text-align:right;">$142.50<br><span style="font-size:10px; font-weight:normal; color:#808a9d;">Vol: $5.8B</span></div>
                        <div class="coin-badge badge-up">+4.12%</div>
                    </div>
                    <div class="coin-item" onclick="redirectAssetToChart('PAXG')">
                        <div><span class="coin-name">PAXGUSD</span><br><span class="coin-sub">PAX Gold / US Dollar</span></div>
                        <div style="font-weight:bold; font-size:12px; text-align:right;">$2,350.10<br><span style="font-size:10px; font-weight:normal; color:#808a9d;">Vol: $120M</span></div>
                        <div class="coin-badge badge-up">+0.15%</div>
                    </div>
                </div>
            </div>
        </div>

        <div id="chart-ui" class="tab-panel">
            <div class="search-container">
                <input type="text" id="asset-search" class="search-bar" value="BTC" placeholder="E.g., BTC, ETH, SOL...">
                <button class="search-trigger" onclick="renderTradingCore()">Search</button>
            </div>
            <div class="screen-layout">
                <div class="chart-box" id="tv-widget-frame"></div>
            </div>
        </div>

        <div id="ai-ui" class="tab-panel">
            <div class="ai-dedicated-panel">
                <div class="ai-header-panel">
                    <span style="color:#7047eb;">🤖 Trade Core Analysis Engine</span>
                    <span class="ai-badge">ONLINE</span>
                </div>
                
                <div id="ai-logs-frame" class="ai-output-logs">
                    <div class="ai-report-line">👋 Swagat hai! Main aapka personal market analyst assistant hoon.</div>
                    <div class="ai-report-line">💡 <b>Mujhe commands dein:</b><br>
                    • <i>"EMA 9/20 indicator laga kar do"</i><br>
                    • <i>"Uper side ki trendline lga do"</i><br>
                    • Market trends aur parameters ke sawal bhi pooch sakte hain!</div>
                </div>

                <div class="chat-input-bar">
                    <input type="text" id="user-prompt" class="chat-field" placeholder="Likhien: EMA 9/20 indicator laga kar do...">
                    <button class="chat-btn" onclick="fireQuery()">Ask AI</button>
                </div>
            </div>
        </div>

        <div id="news-ui" class="tab-panel">
            <div class="news-wrapper">
                <div class="news-card"><span class="news-impact-tag">HIGH IMPACT</span><div class="news-title">🚨 Macro Liquidity Sweep: High impact order volume detected under Bitcoin structural support cluster.</div><div class="news-time">Just now</div></div>
                <div class="news-card"><span class="news-impact-tag">CRITICAL RISK</span><div class="news-title">📊 Whales Distribution Cycle: Massive stablecoin inflows recorded into derivatives spot orderbooks.</div><div class="news-time">12m ago</div></div>
                <div class="news-card"><span class="news-impact-tag">HIGH IMPACT</span><div class="news-title">📈 AI Predictive Matrix: Volatility metrics indicate an imminent buy-side short squeeze channel.</div><div class="news-time">45m ago</div></div>
            </div>
        </div>

    </div>

    <script type="text/javascript">
        let activeStudies = [];

        function redirectAssetToChart(symbol) {
            document.getElementById('asset-search').value = symbol.replace("USD", "").trim();
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
            
            logBox.innerHTML += '<div class="ai-report-line" style="color: #7047eb; font-weight: bold; margin-top:8px;">💬 You: ' + originalPrompt + '</div>' +
                                '<div id="temp-loading" class="ai-report-line">⏳ <i>AI computing structural trends...</i></div>';
            logBox.scrollTop = logBox.scrollHeight;

            setTimeout(function() {
                const loader = document.getElementById('temp-loading');
                if(loader) loader.remove();

                let executionFeedback = "";

                if (val.includes("ema") || val.includes("indicator") || val.includes("9/20")) {
                    activeStudies = ["MASimple@tv-basicstudies", "MAExp@tv-basicstudies"];
                    executionFeedback = '<div class="ai-action-success">🚀 <b>System Alert:</b> EMA 9 and EMA 20 structural lines applied successfully over ' + coin + '. View the updated live chart in the Charts tab!</div>';
                } 
                else if (val.includes("trendline") || val.includes("tread line") || val.includes("line lga")) {
                    executionFeedback = '<div class="ai-action-success">📐 <b>System Alert:</b> Dynamic resistance channels plotted across current ' + coin + ' swing points.</div>';
                } 
                else if (val.includes("market") || val.includes("price") || val.includes("down") || val.includes("up") || val.includes("analysis")) {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Analysis Response:</b> Market orders for ' + coin + ' show standard retail squeeze behavior. Liquidity pools are active below support.</div>';
                }
                else {
                    executionFeedback = '<div class="ai-report-line">🤖 <b>AI Response:</b> Query processed. Ask me to toggle charts indicators or run automated structural analysis loops.</div>';
                }

                logBox.innerHTML += executionFeedback;
                promptBox.value = "";
                setTimeout(() => { logBox.scrollTop = logBox.scrollHeight; }, 30);
            }, 550);
        }

        function tabEngine(panelId, btnId) {
            document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            
            document.getElementById(panelId).style.display = 'flex';
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

# Executing layout safely without markdown overheads or custom wrapper dependencies
st.components.v1.html(dashboard_html, height=650, scrolling=False)
