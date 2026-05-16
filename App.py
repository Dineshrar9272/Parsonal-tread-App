import streamlit as st
import json

# --- 1. AAPKA COINS DATA ---
# (Yahan maine dummy data diya hai, aap apna API fetch karne wala data is 'coins_list' me daal dena)
coins_list = [
    {"name": "Bitcoin", "symbol": "BTC", "price": "$64,500"},
    {"name": "Ethereum", "symbol": "ETH", "price": "$3,450"},
    {"name": "Solana", "symbol": "SOL", "price": "$145"},
    {"name": "Cardano", "symbol": "ADA", "price": "$0.45"},
    {"name": "Ripple", "symbol": "XRP", "price": "$0.52"}
]

# Python list ko JavaScript ke samajhne layak JSON string me convert karein
coins_json = json.dumps(coins_list)


# --- 2. MULTI-TAB DASHBOARD HTML & JS ---
dashboard_html = f"""
<!DOCTYPE html>
<html lang="en" data-theme="system">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Dashboard</title>
    <style>
        /* CSS Themes */
        :root[data-theme="light"] {{
            --bg-color: #f4f6f9;
            --text-color: #333333;
            --card-bg: #ffffff;
            --nav-bg: #007bff;
            --nav-text: #ffffff;
            --border-color: #cccccc;
        }}
        :root[data-theme="dark"] {{
            --bg-color: #121212;
            --text-color: #ffffff;
            --card-bg: #1e1e1e;
            --nav-bg: #1f1f1f;
            --nav-text: #bb86fc;
            --border-color: #333333;
        }}
        @media (prefers-color-scheme: dark) {{
            :root[data-theme="system"] {{
                --bg-color: #121212; --text-color: #ffffff; --card-bg: #1e1e1e; --nav-bg: #1f1f1f; --nav-text: #bb86fc; --border-color: #333333;
            }}
        }}
        @media (prefers-color-scheme: light) {{
            :root[data-theme="system"] {{
                --bg-color: #f4f6f9; --text-color: #333333; --card-bg: #ffffff; --nav-bg: #007bff; --nav-text: #ffffff; --border-color: #cccccc;
            }}
        }}

        body {{
            font-family: Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0; padding: 0;
            transition: background 0.3s, color 0.3s;
        }}

        /* Navbar */
        .navbar {{
            background-color: var(--nav-bg);
            color: var(--nav-text);
            display: flex;
            justify-content: space-around;
            padding: 15px;
            font-weight: bold;
        }}
        .nav-item {{ cursor: pointer; padding: 5px 15px; border-radius: 4px; }}
        .nav-item.active {{ background-color: rgba(255,255,255,0.2); }}

        .container {{ padding: 20px; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* Coin Card Style */
        .coin-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
        }}

        /* Settings Style */
        .setting-section {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .btn {{
            background-color: #007bff; color: white; border: none;
            padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-right: 10px;
        }}
        .btn-reboot {{ background-color: #dc3545; }} /* Red color for reboot */
        select {{
            padding: 6px; background: var(--card-bg); color: var(--text-color); border: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>

    <div class="navbar">
        <div class="nav-item active" onclick="switchTab('home-tab')">🏠 Home</div>
        <div class="nav-item" onclick="switchTab('settings-tab')">⚙️ Settings</div>
    </div>

    <div class="container">
        <div id="home-tab" class="tab-content active">
            <h2>All Coins</h2>
            <div id="coins-container">
                </div>
        </div>

        <div id="settings-tab" class="tab-content">
            <h2>Settings</h2>
            
            <div class="setting-section">
                <h3>System Controls</h3>
                <button class="btn" onclick="rerunApp()">🔄 Rerun Process</button>
                <button class="btn btn-reboot" onclick="rebootApp()">⚠️ Reboot System</button>
            </div>

            <div class="setting-section">
                <h3>Theme Options</h3>
                <select id="theme-select" onchange="changeTheme(this.value)">
                    <option value="system">🖥️ System Default</option>
                    <option value="light">☀️ Light Mode</option>
                    <option value="dark">🌙 Dark Mode</option>
                </select>
            </div>
        </div>
    </div>

    <script>
        // 1. Data Injecting: Python ka saara coin data JS me aa gaya
        const coinsData = {coins_json};

        // Function: Saare coins ko screen par print karne ke liye
        function loadCoins() {{
            const container = document.getElementById('coins-container');
            container.innerHTML = ""; // Pehle clear karein

            coinsData.forEach(coin => {{
                const card = document.createElement('div');
                card.className = 'coin-card';
                card.innerHTML = `
                    <span><strong>${{coin.name}} (${{coin.symbol}})</strong></span>
                    <span>${{coin.price}}</span>
                `;
                container.appendChild(card);
            }});
        }}

        // Tab Switching Logic
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}

        // Rerun & Reboot Controls
        function rerunApp() {{
            alert("Rerunning/Refreshing script data...");
            window.location.reload(); 
        }}

        function rebootApp() {{
            let confirmReboot = confirm("Are you sure you want to REBOOT the entire system?");
            if(confirmReboot) {{
                alert("System Rebooting...");
                // Yahan aap clear cache ya completely app state restart ka code trigger kar sakte hain
                window.location.reload();
            }}
        }}

        // Theme Handling
        function changeTheme(val) {{
            document.documentElement.setAttribute('data-theme', val);
            localStorage.setItem('dashboard-theme', val);
        }}

        // On Load
        window.onload = function() {{
            loadCoins(); // Coins load karein
            
            // Saved Theme load karein
            const savedTheme = localStorage.getItem('dashboard-theme') || 'system';
            document.getElementById('theme-select').value = savedTheme;
            changeTheme(savedTheme);
        }}
    </script>
</body>
</html>
"""

# Streamlit me isse render karein
st.components.v1.html(dashboard_html, height=700, scrolling=True)
