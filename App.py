<!DOCTYPE html>
<html lang="en" data-theme="system">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Dashboard</title>
    <style>
        /* CSS Variables for Themes */
        :root[data-theme="light"] {
            --bg-color: #f4f6f9;
            --text-color: #333333;
            --card-bg: #ffffff;
            --nav-bg: #007bff;
            --nav-text: #ffffff;
            --border-color: #cccccc;
        }
        :root[data-theme="dark"] {
            --bg-color: #121212;
            --text-color: #ffffff;
            --card-bg: #1e1e1e;
            --nav-bg: #1f1f1f;
            --nav-text: #bb86fc;
            --border-color: #333333;
        }
        /* System theme default handling via JS or Media Query */
        @media (prefers-color-scheme: dark) {
            :root[data-theme="system"] {
                --bg-color: #121212;
                --text-color: #ffffff;
                --card-bg: #1e1e1e;
                --nav-bg: #1f1f1f;
                --nav-text: #bb86fc;
                --border-color: #333333;
            }
        }
        @media (prefers-color-scheme: light) {
            :root[data-theme="system"] {
                --bg-color: #f4f6f9;
                --text-color: #333333;
                --card-bg: #ffffff;
                --nav-bg: #007bff;
                --nav-text: #ffffff;
                --border-color: #cccccc;
            }
        }

        body {
            font-family: Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            transition: background 0.3s, color 0.3s;
        }

        /* Navbar Style */
        .navbar {
            background-color: var(--nav-bg);
            color: var(--nav-text);
            display: flex;
            justify-content: space-around;
            padding: 15px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .nav-item {
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 4px;
        }
        .nav-item.active {
            background-color: rgba(255,255,255,0.2);
        }

        /* Content Sections */
        .container {
            padding: 20px;
            max-width: 800px;
            margin: auto;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }

        /* Coins List Style (Home) */
        .coin-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Settings Style */
        .setting-option {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .btn:hover { background-color: #0056b3; }
        select {
            padding: 8px;
            border-radius: 4px;
            background: var(--card-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
        }
    </style>
</head>
<body>

    <!-- Navigation Bar -->
    <div class="navbar">
        <div class="nav-item active" onclick="switchTab('home-tab')">🏠 Home</div>
        <div class="nav-item" onclick="switchTab('settings-tab')">⚙️ Settings</div>
    </div>

    <div class="container">
        
        <!-- HOME TAB: Coins List -->
        <div id="home-tab" class="tab-content active">
            <h2>All Coins</h2>
            <div id="coins-container">
                <!-- Aapki coins list yahan generate hogi -->
                <div class="coin-card">
                    <span><strong>Bitcoin (BTC)</strong></span>
                    <span>$64,500</span>
                </div>
                <div class="coin-card">
                    <span><strong>Ethereum (ETH)</strong></span>
                    <span>$3,450</span>
                </div>
                <div class="coin-card">
                    <span><strong>Solana (SOL)</strong></span>
                    <span>$140</span>
                </div>
            </div>
        </div>

        <!-- SETTINGS TAB -->
        <div id="settings-tab" class="tab-content">
            <h2>Settings</h2>
            
            <!-- Rerun Option -->
            <div class="setting-option">
                <h3>Application</h3>
                <p>Restart or refresh the coin data fetching process.</p>
                <button class="btn" onclick="rerunApp()">🔄 Rerun Process</button>
            </div>

            <!-- Theme Options (Dark, Light, System) -->
            <div class="setting-option">
                <h3>Theme Settings</h3>
                <label for="theme-select">Choose Theme: </label>
                <select id="theme-select" onchange="changeTheme(this.value)">
                    <option value="system">System Default</option>
                    <option value="light">Light Mode</option>
                    <option value="dark">Dark Mode</option>
                </select>
            </div>
        </div>

    </div>

    <script>
        // 1. Tab Switching Logic (Home / Settings)
        function switchTab(tabId) {
            // Sabhi contents ko hide karein
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
import streamlit as st

# Pura HTML, CSS aur JS code ek bade string variable me daalein
dashboard_html = """
<!DOCTYPE html>
<html lang="en" data-theme="system">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Dashboard</title>
    <style>
        /* Yahan saara CSS code aayega... */
        :root[data-theme="light"] { --bg-color: #f4f6f9; --text-color: #333333; }
        :root[data-theme="dark"] { --bg-color: #121212; --text-color: #ffffff; }
        body { background-color: var(--bg-color); color: var(--text-color); }
        .navbar { display: flex; justify-content: space-around; background: #007bff; padding: 10px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="navbar">
        <div onclick="switchTab('home-tab')">🏠 Home</div>
        <div onclick="switchTab('settings-tab')">⚙️ Settings</div>
    </div>

    <div id="home-tab" class="tab-content active">
        <h2>All Coins</h2>
        <p>Bitcoin (BTC) - $64,500</p>
    </div>

    <div id="settings-tab" class="tab-content">
        <h2>Settings</h2>
        <button onclick="location.reload()">🔄 Rerun</button>
        <select onchange="document.documentElement.setAttribute('data-theme', this.value)">
            <option value="system">System</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
        </select>
    </div>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        }
    </script>
</body>
</html>
"""

# Streamlit me is HTML ko render karne ke liye yeh line use karein:
st.components.v1.html(dashboard_html, height=600, scrolling=True)
