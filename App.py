import streamlit as st
import json

# --- 1. COINS DATA (Aap isme apna real data/API replace kar sakte hain) ---
top_cards_data = [
    {"symbol": "BTCUSD", "price": "$79,080.5", "change": "-2.45%", "status": "down"},
    {"symbol": "ETHUSD", "price": "$2,227.05", "change": "-2.04%", "status": "down"}
]

coins_list_data = [
    {"symbol": "ARCUSD", "desc": "AI Rig Complex Perpetual", "price": "$0.07554", "vol": "$2.49M", "change": "+34.03%", "status": "up"},
    {"symbol": "FFUSD", "desc": "Falcon Finance Perpetual", "price": "$0.0851", "vol": "$4.97M", "change": "+7.31%", "status": "up"},
    {"symbol": "BEATUSD", "desc": "Audiera Perpetual", "price": "$0.6202", "vol": "$1.32M", "change": "+5.62%", "status": "up"},
    {"symbol": "PARTIUSD", "desc": "Particle Network Perpetual", "price": "$0.06232", "vol": "$283.91K", "change": "+3.57%", "status": "up"},
    {"symbol": "HANAUSD", "desc": "HANA Network Perpetual", "price": "$0.0368", "vol": "$73.39K", "change": "+1.35%", "status": "up"},
    {"symbol": "PIEVERSEUSD", "desc": "Pieverse Perpetual", "price": "$0.9623", "vol": "$569.48K", "change": "+1.15%", "status": "up"}
]

# JSON strings banayein taaki JavaScript ise padh sake
top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)


# --- 2. COMPLETE DASHBOARD HTML, CSS & JS ---
dashboard_html = f"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Dashboard</title>
    <style>
        /* Modern UI Styling & Variables */
        :root[data-theme="dark"] {{
            --bg-color: #121318;
            --text-color: #ffffff;
            --text-secondary: #848e9c;
            --card-bg: #1e2026;
            --nav-bg: #16181d;
            --nav-active: #f0a500;
            --green: #0ecb81;
            --red: #f6465d;
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
            --border-color: #e6e8ea;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0; padding: 0;
            transition: all 0.3s ease;
        }}

        /* Navbar Bottom Styles (App like experience) */
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

        /* Main Content Container */
        .container {{
            padding: 16px;
            padding-bottom: 80px; /* space for bottom navbar */
            max-width: 500px;
            margin: 0 auto;
        }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* Top Cards Layout */
        .top-cards-grid {{
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }}
        .crypto-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            flex: 1;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: bold;
        }}
        .card-price {{
            font-size: 18px;
            font-weight: bold;
            margin-top: 6px;
        }}

        /* List Headers */
        .list-header {{
            display: flex;
            justify-content: space-between;
            color: var(--text-secondary);
            font-size: 11px;
            padding: 8px 4px;
            border-bottom: 1px solid var(--border-color);
            margin-top: 10px;
        }}

        /* Coins List Rows */
        .coin-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 4px;
            border-bottom: 1px solid var(--border-color);
        }}
        .coin-info {{ display: flex; flex-direction: column; }}
        .coin-symbol {{ font-weight: bold; font-size: 15px; }}
        .coin-desc {{ color: var(--text-secondary); font-size: 11px; margin-top: 2px; }}
        
        .coin-price-block {{ text-align: right; flex-grow: 1; margin-right: 15px; }}
        .coin-price {{ font-weight: bold; font-size: 14px; }}
        .coin-vol {{ color: var(--text-secondary); font-size: 11px; margin-top: 2px; }}

        /* Percentage Badge */
        .badge {{
            padding: 6px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 13px;
            min-width: 65px;
            text-align: center;
            color: white;
        }}
        .bg-up {{ background-color: var(--green); }}
        .bg-down {{ background-color: var(--red); }}
        .text-up {{ color: var(--green); }}
        .text-down {{ color: var(--red); }}

        /* Settings CSS */
        .setting-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .btn {{
            background-color: var(--nav-active);
            color: black; font-weight: bold; border: none;
            padding: 10px 16px; border-radius: 4px; cursor: pointer; margin-right: 8px;
        }}
        .btn-reboot {{ background-color: var(--red); color: white; }}
        select {{
            width: 100%; padding: 10px; background: var(--bg-color); 
            color: var(--text-color); border: 1px solid var(--border-color); border-radius: 4px;
        }}
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

        <div id="settings-tab" class="tab-content">
            <h2 style="margin-top:0;">Settings</h2>
            
            <div class="setting-card">
                <h3>System Controls</h3>
                <p style="color: var(--text-secondary); font-size:13px;">Manage script execution status</p>
                <button class="btn" onclick="rerunApp()">🔄 Rerun</button>
                <button class="btn btn-reboot" onclick="rebootApp()">⚠️ Reboot</button>
            </div>

            <div class="setting-card">
                <h3>Theme Customization</h3>
                <p style="color: var(--text-secondary); font-size:13px;">Select your preferred workspace visual mode</p>
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
        <div class="nav-item" id="nav-settings" onclick="switchTab('settings-tab', 'nav-settings')">
            <div class="nav-icon">⚙️</div>
            <div>Settings</div>
        </div>
    </div>

    <script>
        // Data fetch from Python
        const topCardsData = {top_cards_json};
        const coinsListData = {coins_list_json};

        // 1. Render Top Mini Cards (BTC/ETH)
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

        // 2. Render Main Coins List
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

        // Tab Switcher
        function switchTab(tabId, navId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            document.getElementById(navId).classList.add('active');
        }}

        // Settings Actions
        function rerunApp() {{
            alert("Process Re-running...");
            window.location.reload();
        }}

        function rebootApp() {{
            if(confirm("Do you really want to reboot the connection?")) {{
                alert("System Rebooting...");
                window.location.reload();
            }}
        }}

        function changeTheme(val) {{
            document.documentElement.setAttribute('data-theme', val);
            localStorage.setItem('app-theme', val);
        }}

        // Initialize App
        window.onload = function() {{
            renderTopCards();
            renderCoinsList();
            
            // Theme persistence
            const savedTheme = localStorage.getItem('app-theme') || 'dark';
            document.getElementById('theme-select').value = savedTheme;
            changeTheme(savedTheme);
        }}
    </script>
</body>
</html>
"""

# Streamlit Output Component
st.components.v1.html(dashboard_html, height=750, scrolling=True)
