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

