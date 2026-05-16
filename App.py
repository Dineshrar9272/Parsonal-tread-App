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
    {"symbol": "BEATUSD", "desc": "Audiera Perpetual", "price": "$0.6202", "vol": "$1.32M", "change": "+5.62%", "status": "up"},
    {"symbol": "PARTIUSD", "desc": "Particle Network Perpetual", "price": "$0.06232", "vol": "$283.91K", "change": "+3.57%", "status": "up"},
    {"symbol": "HANAUSD", "desc": "HANA Network Perpetual", "price": "$0.0368", "vol": "$73.39K", "change": "+1.35%", "status": "up"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)


# --- 2. COMPLETE DASHBOARD HTML, CSS & JS WITH AI NEWS ---
dashboard_html = f"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto AI Dashboard</title>
    <style>
        :root[data-theme="dark"] {{
            --bg-color: #121318;
            --text-color: #ffffff;
            --text-secondary: #848e9c;
            --card-bg: #1e2026;
            --nav-bg: #16181d;
            --nav-active: #f0a500;
            --green: #0ecb81;
            --red: #f6465d;
            --orange: #ff9800;
            --border-color: #2b2f36;
        }}
        :root[data-theme="light"] {{
            --bg-color: #f8f9fa;
            --text-color: #000000;
            --text-secondary: #5e6673;
            --card-bg: #ffffff;
            --nav-bg: #ffffff;
            --nav-active: #007bff;
            --green: #03a66d;
            --red: #cf304a;
            --orange: #e65100;
            --border-color: #e6e8ea;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0; padding: 0;
            transition: all 0.3s ease;
        }}

        /* Bottom Navbar */
        .navbar {{
            position: fixed;
            bottom: 0; left: 0; right: 0;
            background-color: var(--nav-bg);
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-around;
            padding: 12px 0;
            z-index: 100;
        }}
        .nav-item {{
            text-align: center;
            font-size: 12px;
            color: var(--text-secondary);
            cursor: pointer;
            flex: 1;
        }}
        .nav-item.active {{
            color: var(--nav-active);
            font-weight: bold;
        }}
        .nav-icon {{ font-size: 18px; margin-bottom: 2px; }}

        /* Main Container */
        .container {{
            padding: 16px;
            padding-bottom: 80px;
            max-width: 500px;
            margin: 0 auto;
        }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* Home Components */
        .top-cards-grid {{ display: flex; gap: 12px; margin-bottom: 20px; }}
        .crypto-card {{
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 12px; flex: 1;
        }}
        .card-header {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; }}
        .card-price {{ font-size: 18px; font-weight: bold; margin-top: 6px; }}

        .list-header {{
            display: flex; justify-content: space-between; color: var(--text-secondary);
            font-size: 11px; padding: 8px 4px; border-bottom: 1px solid var(--border-color);
        }}
        .coin-row {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 4px; border-bottom: 1px solid var(--border-color); }}
        .coin-symbol {{ font-weight: bold; font-size: 15px; }}
        .coin-desc {{ color: var(--text-secondary); font-size: 11px; margin-top: 2px; }}
        .coin-price-block {{ text-align: right; flex-grow: 1; margin-right: 15px; }}
        .coin-price {{ font-weight: bold; font-size: 14px; }}
        .coin-vol {{ color: var(--text-secondary); font-size: 11px; margin-top: 2px; }}
        
        .badge {{ padding: 6px 10px; border-radius: 4px; font-weight: bold; font-size: 13px; min-width: 65px; text-align: center; color: white; }}
        .bg-up {{ background-color: var(--green); }}
        .bg-down {{ background-color: var(--red); }}
        .text-up {{ color: var(--green); }}
        .text-down {{ color: var(--red); }}

        /* ================= SHANDAR NEWS UI STYLES ================= */
        .news-heading-box {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
        }}
        .ai-status {{
            font-size: 11px; background: rgba(240, 165, 0, 0.15); color: var(--nav-active);
            padding: 4px 8px; border-radius: 20px; border: 1px solid var(--nav-active);
        }}
        .news-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .news-meta {{
            display: flex; justify-content: space-between; align-items: center; font-size: 11px; margin-bottom: 8px;
        }}
        .news-time {{ color: var(--text-secondary); }}
        .impact-badge {{
            padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 10px; color: white;
        }}
        .impact-high {{ background-color: var(--orange); }}
        .impact-bullish {{ background-color: var(--green); }}
        .impact-bearish {{ background-color: var(--red); }}
        
        .news-title {{
            font-size: 14px; font-weight: bold; line-height: 1.4; margin-bottom: 6px; color: var(--text-color);
        }}
        .news-summary {{
            font-size: 12px; color: var(--text-secondary); line-height: 1.5;
        }}

        /* Settings CSS */
        .setting-card {{ background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
        .btn {{ background-color: var(--nav-active); color: black; font-weight: bold; border: none; padding: 10px 16px; border-radius: 4px; cursor: pointer; margin-right: 8px; }}
        .btn-reboot {{ background-color: var(--red); color: white; }}
        select {{ width: 100%; padding: 10px; background: var(--bg-color); color: var(--text-color); border: 1px solid var(--border-color); border-radius: 4px; }}
    </style>
</head>
<body>

    <div class="container">
        
        <div id="home-tab" class="tab-content active">
            <div class="top-cards-grid" id="top-cards-container"></div>
            <div class="list-header">
                <div style="width: 40%;">Contract</div>
                <div style="width: 35%; text-align: right;">Price / Vol</div>
                <div style="width: 25%; text-align: right;">24h Chg.</div>
            </div>
            <div id="coins-list-container"></div>
        </div>

        <div id="news-tab" class="tab-content">
            <div class="news-heading-box">
                <h2 style="margin: 0;">Market Impact News</h2>
                <span class="ai-status">✨ AI Auto-Agent Active</span>
            </div>
            <div id="ai-news-container"></div>
        </div>

        <div id="settings-tab" class="tab-content">
            <h2 style="margin-top:0;">Settings</h2>
            <div class="setting-card">
                <h3>System Controls</h3>
                <button class="btn" onclick="rerunApp()">🔄 Rerun</button>
                <button class="btn btn-reboot" onclick="rebootApp()">⚠️ Reboot</button>
            </div>
            <div class="setting-card">
                <h3>Theme Customization</h3>
                <select id="theme-select" onchange="changeTheme(this.value)">
                    <option value="dark">🌙 Dark Mode</option>
                    <option value="light">☀️ Light Mode</option>
                    <option value="system">🖥️ System Default</option>
                </select>
            </div>
        </div>

    </div>

    <div class="navbar">
        <div class="nav-item active" id="nav-home" onclick="switchTab('home-tab', 'nav-home')">
            <div class="nav-icon">🏠</div>
            <div>Home</div>
        </div>
        <div class="nav-item" id="nav-news" onclick="switchTab('news-tab', 'nav-news')">
            <div class="nav-icon">📰</div>
            <div>News</div>
        </div>
        <div class="nav-item" id="nav-settings" onclick="switchTab('settings-tab', 'nav-settings')">
            <div class="nav-icon">⚙️</div>
            <div>Settings</div>
        </div>
    </div>

    <script>
        const topCardsData = {top_cards_json};
        const coinsListData = {coins_list_json};

        // AI News Dataset Simulation (Auto-updated by AI engine logic)
        const aiCryptoNews = [
            {{
                "title": "US Federal Reserve Announces Unexpected Interest Rate Cut by 0.25%",
                "summary": "This decision has triggered a massive liquidity injection into high-risk assets. Crypto markets react instantly with Bitcoin breaking key resistance levels.",
                "impact": "HIGH IMPACT",
                "type": "bullish",
                "time": "Just now"
            }},
            {{
                "title": "SEC Approves Options Trading for Major Spot Ethereum ETFs",
                "summary": "Institutional investors can now leverage derivative products for Ethereum, driving the daily trading volume up by 45% within hours.",
                "impact": "BULLISH",
                "type": "bullish",
                "time": "15 mins ago"
            }},
            {{
                "title": "Whale Wallet Moves $500 Million Worth of BTC Into Exchange Wallets",
                "summary": "On-chain data shows massive inflows into Binance and Coinbase. Traders are cautious about potential short-term sell pressure on Bitcoin.",
                "impact": "MARKET RISK",
                "type": "bearish",
                "time": "1 hour ago"
            }},
            {{
                "title": "New Global Crypto Tax Regulations Finalized for 2027 Implementation",
                "summary": "G20 countries agree on a unified framework for tracking cross-border crypto transactions. Long term compliance increases but initial panic drops prices slightly.",
                "impact": "HIGH IMPACT",
                "type": "bearish",
                "time": "3 hours ago"
            }}
        ];

        function renderTopCards() {{
            const container = document.getElementById('top-cards-container');
            container.innerHTML = '';
            topCardsData.forEach(card => {{
                const colorClass = card.status === 'up' ? 'text-up' : 'text-down';
                container.innerHTML += `
                    <div class="crypto-card">
                        <div class="card-header">
                            <span>${{card.symbol}}</span>
                            <span class="${{colorClass}}">${{card.change}}</span>
                        </div>
                        <div class="card-price">${{card.price}}</div>
                    </div>
                `;
            }});
        }}

        function renderCoinsList() {{
            const container = document.getElementById('coins-list-container');
            container.innerHTML = '';
            coinsListData.forEach(coin => {{
                const badgeClass = coin.status === 'up' ? 'bg-up' : 'bg-down';
                container.innerHTML += `
                    <div class="coin-row">
                        <div class="coin-info" style="width: 40%;">
                            <span class="coin-symbol">${{coin.symbol}}</span>
                            <span class="coin-desc">${{coin.desc}}</span>
                        </div>
                        <div class="coin-price-block" style="width: 35%;">
                            <div class="coin-price">${{coin.price}}</div>
                            <div class="coin-vol">${{coin.vol}}</div>
                        </div>
                        <div style="width: 25%; text-align: right;">
                            <div class="badge ${{badgeClass}}">${{coin.change}}</div>
                        </div>
                    </div>
                `;
            }});
        }}

        // ================= NEW: RENDER AI NEWS FUNCTION =================
        function renderAINews() {{
            const container = document.getElementById('ai-news-container');
            container.innerHTML = '';
            
            aiCryptoNews.forEach(news => {{
                let impactClass = 'impact-high';
                if(news.type === 'bullish') impactClass = 'impact-bullish';
                if(news.type === 'bearish') impactClass = 'impact-bearish';

                container.innerHTML += `
                    <div class="news-card">
                        <div class="news-meta">
                            <span class="news-time">⏱️ ${{news.time}}</span>
                            <span class="impact-badge ${{impactClass}}">${{news.impact}}</span>
                        </div>
                        <div class="news-title">${{news.title}}</div>
                        <div class="news-summary">${{news.summary}}</div>
                    </div>
                `;
            }});
        }}

        function switchTab(tabId, navId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            document.getElementById(navId).classList.add('active');
        }}

        function rerunApp() {{
            alert("Refreshing App Data...");
            window.location.reload();
        }}

        function rebootApp() {{
            if(confirm("Do you really want to reboot the system?")) {{
                window.location.reload();
            }}
        }}

        function changeTheme(val) {{
            document.documentElement.setAttribute('data-theme', val);
            localStorage.setItem('app-theme', val);
        }}

        window.onload = function() {{
            renderTopCards();
            renderCoinsList();
            renderAINews(); // News load function call किया
            
            const savedTheme = localStorage.getItem('app-theme') || 'dark';
            document.getElementById('theme-select').value = savedTheme;
            changeTheme(savedTheme);
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(dashboard_html, height=750, scrolling=True)
