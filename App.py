import streamlit as st
import json

# --- 1. COINS DATA ---
top_cards_data = [
    {"symbol": "BTCUSD", "price": "$79,080.5", "change": "-2.45%", "status": "down"},
    {"symbol": "ETHUSD", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "ARCUSD", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"},
    {"symbol": "FFUSD", "desc": "Falcon Finance Perpetual", "price": "$0.0851", "vol": "$4.97M", "change": "+7.31%", "status": "up"},
    {"symbol": "BEATUSD", "desc": "Audiera Perpetual", "price": "$0.6202", "vol": "$1.32M", "change": "+5.62%", "status": "up"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)

# --- 2. MAIN DASHBOARD HTML, CSS & JS ---
# Handled safely without f-string decimal conflict bugs
dashboard_html = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Advanced Analytics Panel</title>
    <style>
        :root[data-theme="dark"] {
            --bg-color: #121318; --text-color: #ffffff; --text-secondary: #848e9c;
            --card-bg: #1e2026; --nav-bg: #16181d; --nav-active: #f0a500;
            --green: #0ecb81; --red: #f6465d; --orange: #ff9800; --border-color: #2b2f36;
        }
        :root[data-theme="light"] {
            --bg-color: #f8f9fa; --text-color: #000000; --text-secondary: #5e6673;
            --card-bg: #ffffff; --nav-bg: #ffffff; --nav-active: #007bff;
            --green: #03a66d; --red: #cf304a; --orange: #e65100; --border-color: #e6e8ea;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color); color: var(--text-color); margin: 0; padding: 0;
            transition: all 0.3s ease; overflow-x: hidden;
        }

        /* Top Navigation Menu Bar */
        .navbar {
            position: sticky; top: 0; left: 0; right: 0; background-color: var(--nav-bg);
            border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }
        .nav-item { text-align: center; font-size: 11px; color: var(--text-secondary); cursor: pointer; flex: 1; }
        .nav-item.active { color: var(--nav-active); font-weight: bold; border-bottom: 2px solid var(--nav-active); }
        .nav-icon { font-size: 16px; }

        .container { padding: 12px; max-width: 1200px; margin: 0 auto; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* Home lists config */
        .top-cards-grid { display: flex; gap: 12px; margin-bottom: 15px; }
        .crypto-card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; flex: 1; }
        .card-header { display: flex; justify-content: space-between; font-size: 12px; }
        .card-price { font-size: 18px; font-weight: bold; margin-top: 4px; }
        .list-header { display: flex; justify-content: space-between; color: var(--text-secondary); font-size: 11px; padding: 8px 4px; border-bottom: 1px solid var(--border-color); }
        .coin-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 4px; border-bottom: 1px solid var(--border-color); }
        .coin-symbol { font-weight: bold; }
        .badge { padding: 6px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; color: white; min-width: 60px; text-align: center; }
        .bg-up { background-color: var(--green); } .bg-down { background-color: var(--red); }

        /* 3-Dot Languages Context Rules */
        .news-heading-box { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .menu-container { position: relative; }
        .three-dot-btn { font-size: 22px; cursor: pointer; padding: 0 10px; }
        .dropdown-menu { display: none; position: absolute; right: 0; top: 25px; background-color: var(--card-bg); min-width: 120px; border: 1px solid var(--border-color); border-radius: 8px; z-index: 200; }
        .dropdown-menu div { color: var(--text-color); padding: 8px 12px; font-size: 13px; cursor: pointer; }
        .dropdown-menu div:hover { background: rgba(255,255,255,0.08); color: var(--nav-active); }
        .dropdown-menu div.selected { color: var(--nav-active); font-weight: bold; }
        .dropdown-menu.show { display: block; }
        .news-card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px; margin-bottom: 12px; cursor: pointer; }

        /* ================= EXPERT SPLIT CONTAINER CONFIG ================= */
        .search-box-container { display: flex; gap: 8px; margin-bottom: 12px; }
        .search-input { flex-grow: 1; padding: 10px; border-radius: 6px; background-color: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-color); font-weight: bold; }
        .search-btn { background-color: var(--nav-active); color: black; border: none; padding: 0 14px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        
        /* 50:50 Screen structure adjustments */
        .split-grid { display: flex; gap: 14px; align-items: stretch; transition: all 0.3s ease; }
        .left-panel { flex: 1.3; min-width: 0; transition: all 0.3s ease; } /* Chart takes priority balance */
        .right-panel { flex: 0.7; min-width: 0; display: flex; flex-direction: column; gap: 12px; transition: all 0.3s ease; } /* AI panel is kept narrower/smaller */

        .chart-header-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .indicator-group { display: flex; gap: 12px; font-size: 12px; font-weight: bold; }
        .indicator-group label { display: flex; align-items: center; gap: 4px; cursor: pointer; }
        .btn-fullscreen { background: var(--nav-active); color: black; border: none; padding: 5px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: bold; }

        .chart-wrapper { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; height: 460px; overflow: hidden; position: relative; }
        
        /* AI Box Architecture */
        .ai-analysis-card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px; height: calc(460px - 30px); display: flex; flex-direction: column; justify-content: space-between; }
        .ai-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; color: var(--nav-active); margin-bottom: 8px; }
        .ai-direction-badge { padding: 2px 8px; border-radius: 4px; font-size: 11px; color: white; }
        .ai-text-box { font-size: 13px; line-height: 1.5; color: var(--text-color); margin-bottom: 10px; overflow-y: auto; flex-grow: 1; }
        
        /* Chat elements configuration */
        .ai-chat-container { border-top: 1px solid var(--border-color); padding-top: 10px; display: flex; gap: 6px; }
        .chat-input { flex-grow: 1; padding: 8px; border-radius: 6px; background-color: var(--bg-color); border: 1px solid var(--border-color); color: var(--text-color); font-size: 12px; }
        .chat-send-btn { background: var(--nav-active); border: none; color: black; font-weight: bold; border-radius: 6px; padding: 0 12px; cursor: pointer; font-size: 12px; }

        /* ================= FULLSCREEN RECONFIG (2ND SCREENSHOT LOOK) ================= */
        body.fs-mode .right-panel { display: none !important; }
        body.fs-mode .left-panel { flex: 1 1 100% !important; width: 100% !important; }
        body.fs-mode .chart-wrapper { height: 600px; } /* Maximum full viewport display stretch */
    </style>
</head>
<body>

    <div class="navbar">
        <div class="nav-item active" id="nav-home" onclick="switchTab('home-tab', 'nav-home')">
            <div class="nav-icon">🏠</div><div>Home</div>
        </div>
        <div class="nav-item" id="nav-news" onclick="switchTab('news-tab', 'nav-news')">
            <div class="nav-icon">📰</div><div>News</div>
        </div>
        <div class="nav-item" id="nav-chart" onclick="switchTab('chart-tab', 'nav-chart')">
            <div class="nav-icon">📊</div><div>Chart</div>
        </div>
    </div>

    <div class="container">
        
        <div id="home-tab" class="tab-content active">
            <div class="top-cards-grid" id="top-cards-container"></div>
            <div class="list-header">
                <div style="width: 40%;">Contract</div><div style="width: 35%; text-align: right;">Price / Vol</div><div style="width: 25%; text-align: right;">24h Chg.</div>
            </div>
            <div id="coins-list-container"></div>
        </div>

        <div id="news-tab" class="tab-content">
            <div class="news-heading-box">
                <h2 style="margin: 0;">Market News</h2>
                <div class="menu-container">
                    <span class="three-dot-btn" onclick="toggleLangMenu(event)">⋮</span>
                    <div id="lang-dropdown" class="dropdown-menu">
                        <div id="lang-en" class="selected" onclick="changeLanguage('en')">🇺🇸 English</div>
                        <div id="lang-hi" onclick="changeLanguage('hi')">🇮🇳 Hindi</div>
                        <div id="lang-pa" onclick="changeLanguage('pa')">🇮🇳 Punjabi</div>
                    </div>
                </div>
            </div>
            <div id="ai-news-container"></div>
        </div>

        <div id="chart-tab" class="tab-content">
            <div class="search-box-container">
                <input type="text" id="chart-search-input" class="search-input" value="BTC" placeholder="Search Asset Symbol (e.g. BTC, ETH)...">
                <button class="search-btn" onclick="updateChartAndAI()">Search</button>
            </div>

            <div class="split-grid" id="split-grid-box">
                
                <div class="left-panel">
                    <div class="chart-header-actions">
                        <div class="indicator-group">
                            <label><input type="checkbox" id="check-ema" onchange="updateChartAndAI()"> EMA</label>
                            <label><input type="checkbox" id="check-vol" checked onchange="updateChartAndAI()"> Volume</label>
                        </div>
                        <button class="btn-fullscreen" onclick="toggleFullScreen()">🔍 Full Screen Mode</button>
                    </div>
                    <div class="chart-wrapper" id="tv-chart-container"></div>
                </div>

                <div class="right-panel" id="ai-right-panel">
                    <div class="ai-analysis-card">
                        <div>
                            <div class="ai-header">
                                <span>✨ AI Market Analysis</span>
                                <span id="ai-badge" class="ai-direction-badge bg-up">BULLISH</span>
                            </div>
                            <div id="ai-analysis-text" class="ai-text-box">Engine loading...</div>
                        </div>

                        <div class="ai-chat-container">
                            <input type="text" id="user-chat-input" class="chat-input" placeholder="Ask AI (e.g. Market me kya chal raha hai?)">
                            <button class="chat-send-btn" onclick="askAIEngine()">Ask</button>
                        </div>
                    </div>
                </div>

            </div>
        </div>

    </div>

    <script>
        // Multi-Language Structural Engine
        const aiAnalysisDatabase = {
            "en": {
                "BULLISH": "Technical indicators suggest a strong uptrend. EMA lines show an upward golden crossover. Volume patterns show accumulating buy orders.",
                "BEARISH": "RSI values entering overbought zone with high overhead resistance. Short-term downside corrections are highly probable.",
                "market_status": "The general market sentiment is consolidating. Institutional volumes are steadily shifting support bases upward."
            },
            "hi": {
                "BULLISH": "तकनीकी संकेतक मजबूत तेजी का संकेत दे रहे हैं। EMA लाइनें ऊपर की ओर गोल्डन क्रॉसओवर दिखा रही हैं और वॉल्यूम बढ़ रहा है।",
                "BEARISH": "RSI वैल्यू ओवरबॉट जोन में जा रही है, ऊपर की तरफ मजबूत रेजिस्टेंस है। कुछ समय के लिए कीमतों में गिरावट आ सकती है।",
                "market_status": "मार्केट में इस समय बड़ी स्थिरता देखी जा रही है। बड़े व्हेल्स और ट्रेडर्स नीचे के स्तरों पर अपनी पोजीशन बढ़ा रहे हैं।"
            },
            "pa": {
                "BULLISH": "ਤਕਨੀਕੀ ਸੰਕੇਤਕ ਮਜ਼ਬੂਤ ਤੇਜ਼ੀ ਦਾ ਇਸ਼ਾਰਾ ਕਰ ਰਹੇ ਹਨ। EMA ਲਾਈਨਾਂ ਉੱਪਰ ਵੱਲ ਗੋਲਡਨ ਕ੍ਰਾਸਓਵਰ ਦਿਖਾ ਰਹੀਆਂ ਹਨ।",
                "BEARISH": "RSI ਓਵਰਬੌਟ ਜ਼ੋਨ ਵਿੱਚ ਜਾ ਰਿਹਾ ਹੈ, ਉੱਪਰ ਵੱਲ ਰੁਕਾਵਟ ਬਣੀ ਹੋਈ ਹੈ। ਕੁਝ ਸਮੇਂ ਲਈ ਮਾਰਕੀਟ ਹੇਠਾਂ ਆ ਸਕਦੀ ਹੈ।",
                "market_status": "ਮਾਰਕੀਟ ਵਿੱਚ ਇਸ ਸਮੇਂ ਸਥਿਰਤਾ ਹੈ। ਵੱਡੇ ਨਿਵੇਸ਼ਕ ਹੇਠਲੇ ਪੱਧਰ 'ਤੇ ਹੌਲੀ-ਹੌਲੀ ਹੋਰ ਖਰੀਦਦਾਰੀ ਵਧਾ ਰਹੇ ਹਨ।"
            }
        };

        let currentLang = 'en';

        function toggleLangMenu(e) { e.stopPropagation(); document.getElementById('lang-dropdown').classList.toggle('show'); }
        window.addEventListener('click', function() { document.getElementById('lang-dropdown').classList.remove('show'); });

        function changeLanguage(lang) {
            currentLang = lang;
            document.querySelectorAll('.dropdown-menu div').forEach(div => div.classList.remove('selected'));
            document.getElementById(`lang-${lang}`).classList.add('selected');
            updateChartAndAI();
        }

        // TradingView Initialization Layer
        function loadTradingViewChart(symbol) {
            const container = document.getElementById('tv-chart-container');
            container.innerHTML = "";
            
            const showEMA = document.getElementById('check-ema').checked;
            const showVol = document.getElementById('check-vol').checked;
            
            const studiesArray = [];
            if(showEMA) studiesArray.push("MAExp@tv-basicstudies");
            if(showVol) studiesArray.push("Volume@tv-basicstudies");

            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.type = 'text/javascript';
            script.async = true;
            script.onload = function() {
                new TradingView.widget({
                    "width": "100%", "height": "100%",
                    "symbol": "BINANCE:" + symbol + "USDT",
                    "interval": "60", "theme": "dark", "style": "1", "locale": "en",
                    "hide_side_toolbar": false, "allow_symbol_change": false,
                    "container_id": "tv-chart-container",
                    "studies": studiesArray
                });
            };
            document.head.appendChild(script);
        }

        // Action Trigger for Full Screen Toggling
        function toggleFullScreen() {
            document.body.classList.toggle('fs-mode');
            let coinSymbol = document.getElementById('chart-search-input').value.toUpperCase().trim() || "BTC";
            loadTradingViewChart(coinSymbol);
        }

        function updateChartAndAI() {
            let coinSymbol = document.getElementById('chart-search-input').value.toUpperCase().trim() || "BTC";
            loadTradingViewChart(coinSymbol);

            const signal = (coinSymbol.charCodeAt(0) % 2 === 0) ? "BULLISH" : "BEARISH";
            const badge = document.getElementById('ai-badge');
            
            if(signal === "BULLISH") {
                badge.innerText = currentLang === 'hi' ? 'तेजी (BULLISH)' : (currentLang === 'pa' ? 'ਤੇਜ਼ੀ' : 'BULLISH');
                badge.className = "ai-direction-badge bg-up";
            } else {
                badge.innerText = currentLang === 'hi' ? 'मंदी (BEARISH)' : (currentLang === 'pa' ? 'ਮੰਦੀ' : 'BEARISH');
                badge.className = "ai-direction-badge bg-down";
            }
            document.getElementById('ai-analysis-text').innerText = `[${coinSymbol}USDT] - ` + aiAnalysisDatabase[currentLang][signal];
        }

        function askAIEngine() {
            const query = document.getElementById('user-chat-input').value.trim();
            if(!query) return;

            const targetBox = document.getElementById('ai-analysis-text');
            targetBox.innerHTML = "⏳ <i>AI Processing query analytics...</i>";
            
            setTimeout(() => {
                targetBox.innerText = aiAnalysisDatabase[currentLang]["market_status"];
                document.getElementById('user-chat-input').value = "";
            }, 600);
        }

        function switchTab(tabId, navId) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            document.getElementById(navId).classList.add('active');
            if(tabId === 'chart-tab') { updateChartAndAI(); }
        }

        window.onload = function() {
            updateChartAndAI();
        }
    </script>
</body>
</html>
"""

st.components.v1.html(dashboard_html, height=720, scrolling=True)
