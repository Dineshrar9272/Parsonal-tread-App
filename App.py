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
    {"symbol": "PARTIUSD", "desc": "Particle Network Perpetual", "price": "$0.06232", "vol": "$283.91K", "change": "+3.57%", "status": "up"}
]

top_cards_json = json.dumps(top_cards_data)
coins_list_json = json.dumps(coins_list_data)


# --- 2. MAIN DASHBOARD HTML, CSS & JS ---
dashboard_html = f"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Advanced Dashboard</title>
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
            --modal-overlay: rgba(0,0,0,0.8);
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
            --modal-overlay: rgba(0,0,0,0.5);
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
            position: fixed; bottom: 0; left: 0; right: 0;
            background-color: var(--nav-bg); border-top: 1px solid var(--border-color);
            display: flex; justify-content: space-around; padding: 12px 0; z-index: 100;
        }}
        .nav-item {{ text-align: center; font-size: 12px; color: var(--text-secondary); cursor: pointer; flex: 1; }}
        .nav-item.active {{ color: var(--nav-active); font-weight: bold; }}
        .nav-icon {{ font-size: 18px; margin-bottom: 2px; }}

        /* Main Container */
        .container {{ padding: 16px; padding-bottom: 80px; max-width: 500px; margin: 0 auto; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* Home UI Elements */
        .top-cards-grid {{ display: flex; gap: 12px; margin-bottom: 20px; }}
        .crypto-card {{ background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; flex: 1; }}
        .card-header {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; }}
        .card-price {{ font-size: 18px; font-weight: bold; margin-top: 6px; }}
        .list-header {{ display: flex; justify-content: space-between; color: var(--text-secondary); font-size: 11px; padding: 8px 4px; border-bottom: 1px solid var(--border-color); }}
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

        /* ================= ADVANCED NEWS UI WITH 3-DOT MENU ================= */
        .news-heading-box {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; position: relative;
        }}
        
        /* 3-Dot Dropdown Container */
        .menu-container {{ position: relative; display: inline-block; }}
        .three-dot-btn {{
            font-size: 22px; cursor: pointer; color: var(--text-color); padding: 5px 10px; border-radius: 50%;
        }}
        .three-dot-btn:hover {{ background: rgba(255,255,255,0.1); }}
        
        .dropdown-menu {{
            display: none; position: absolute; right: 0; top: 35px;
            background-color: var(--card-bg); min-width: 130px;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.3); border: 1px solid var(--border-color);
            border-radius: 8px; z-index: 200;
        }}
        .dropdown-menu div {{
            color: var(--text-color); padding: 10px 14px; font-size: 13px;
            text-align: left; cursor: pointer; transition: 0.2s;
        }}
        .dropdown-menu div:hover {{ background-color: rgba(255,255,255,0.08); color: var(--nav-active); }}
        .dropdown-menu div.selected {{ color: var(--nav-active); font-weight: bold; }}
        .dropdown-menu.show {{ display: block; }}

        /* News Cards Layout */
        .news-card {{
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 16px; margin-bottom: 14px; cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .news-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }}
        .news-meta {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; margin-bottom: 8px; }}
        .news-time {{ color: var(--text-secondary); }}
        .impact-badge {{ padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 10px; color: white; }}
        .impact-high {{ background-color: var(--orange); }}
        .impact-bullish {{ background-color: var(--green); }}
        .impact-bearish {{ background-color: var(--red); }}
        .news-title {{ font-size: 14px; font-weight: bold; line-height: 1.4; margin-bottom: 6px; color: var(--text-color); }}
        .news-summary {{ font-size: 12px; color: var(--text-secondary); line-height: 1.5; }}
        .click-hint {{ font-size: 10px; color: var(--nav-active); text-align: right; margin-top: 8px; font-style: italic; }}

        /* ================= FULL INFO MODAL WINDOW (POPUP) ================= */
        .modal {{
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: var(--modal-overlay); z-index: 1000; justify-content: center; align-items: center;
        }}
        .modal-content {{
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            width: 90%; max-width: 440px; border-radius: 16px; padding: 20px;
            position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            animation: fadeIn 0.3s ease;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: scale(0.9); }} to {{ opacity: 1; transform: scale(1); }} }}
        .close-modal {{
            position: absolute; top: 12px; right: 16px; font-size: 24px;
            cursor: pointer; color: var(--text-secondary);
        }}
        .close-modal:hover {{ color: var(--text-color); }}
        .modal-title {{ font-size: 16px; font-weight: bold; margin-bottom: 12px; line-height: 1.4; color: var(--text-color); }}
        .modal-full-text {{ font-size: 13px; color: var(--text-color); line-height: 1.6; text-align: justify; }}

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
                </select>
            </div>
        </div>

    </div>

    <div id="newsModal" class="modal" onclick="closeNewsModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="close-modal" onclick="closeNewsModal()">&times;</span>
            <div id="modal-meta" style="margin-bottom: 8px;"></div>
            <div id="modal-title" class="modal-title"></div>
            <hr style="border: 0; border-top: 1px solid var(--border-color); margin-bottom: 12px;">
            <div id="modal-body" class="modal-full-text"></div>
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

        // Multi-Language AI News Database
        const newsDatabase = {{
            "en": [
                {{
                    "title": "US Federal Reserve Cuts Interest Rates by 0.25%",
                    "summary": "This unexpected decision has injected massive liquidity into crypto assets.",
                    "full": "The US Federal Reserve unexpectedly cut interest rates by 25 basis points today. This expansionary monetary policy has driven institutional investors to move capital out of bonds and inject massive liquidity into digital high-risk assets, causing Bitcoin to break key resistance levels immediately.",
                    "impact": "HIGH IMPACT", "type": "bullish", "time": "Just now"
                }},
                {{
                    "title": "SEC Approves Options Trading for Ethereum ETFs",
                    "summary": "Institutional investors can now leverage derivative products for Ethereum easily.",
                    "full": "The Securities and Exchange Commission (SEC) has officially greenlit options trading for spot Ethereum ETFs. Experts suggest this move unlocks massive retail and institutional hedging capabilities, which spiked Ethereum's immediate 24-hour volume by over 45%.",
                    "impact": "BULLISH", "type": "bullish", "time": "20m ago"
                }}
            ],
            "hi": [
                {{
                    "title": "अमेरिकी फेडरल रिजर्व ने ब्याज दरों में 0.25% की कटौती की",
                    "summary": "इस अप्रत्याशित फैसले ने क्रिप्टो संपत्तियों में भारी तरलता (Liquidity) ला दी है।",
                    "full": "अमेरिकी फेडरल रिजर्व ने आज अचानक ब्याज दरों में 25 बेसिस पॉइंट की कटौती की घोषणा की है। इस फैसले के बाद संस्थागत निवेशकों ने बॉन्ड से पैसा निकालकर सीधे क्रिप्टो मार्केट में डालना शुरू कर दिया है, जिससे बिटकॉइन ने तुरंत अपने सभी मुख्य रेजिस्टेंस लेवल तोड़ दिए हैं।",
                    "impact": "हाई इम्पैक्ट", "type": "bullish", "time": "अभी-अभी"
                }},
                {{
                    "title": "SEC ने एथेरियम ETF के लिए ऑप्शंस ट्रेडिंग को मंजूरी दी",
                    "summary": "बड़े निवेशक अब एथेरियम डेरिवेटिव प्रोडक्ट्स का आसानी से फायदा उठा सकते हैं।",
                    "full": "सिक्योरिटीज एंड एक्सचेंज कमीशन (SEC) ने आधिकारिक तौर पर स्पॉट एथेरियम ETF के लिए ऑप्शंस ट्रेडिंग को हरी झंडी दे दी है। विशेषज्ञों का कहना है कि इस फैसले से मार्केट में वॉल्यूम 45% तक बढ़ गया है और लॉन्ग-टर्म ग्रोथ की संभावनाएं बढ़ गई हैं।",
                    "impact": "तेजी (BULLISH)", "type": "bullish", "time": "20 मिनट पहले"
                }}
            ],
            "pa": [
                {{
                    "title": "ਅਮਰੀਕੀ ਫੈਡਰਲ ਰਿਜ਼ਰਵ ਨੇ ਵਿਆਜ ਦਰਾਂ ਵਿੱਚ 0.25% ਦੀ ਕਟੌਤੀ ਕੀਤੀ",
                    "summary": "ਇਸ ਅਚਾਨਕ ਫੈਸਲੇ ਨੇ ਕ੍ਰਿਪਟੋ ਮਾਰਕੀਟ ਵਿੱਚ ਭਾਰੀ ਪੈਸਾ (Liquidity) ਪਹੁੰਚਾਇਆ ਹੈ।",
                    "full": "ਅਮਰੀਕੀ ਫੈਡਰਲ ਰਿਜ਼ਰਵ ਨੇ ਅੱਜ ਅਚਾਨਕ ਵਿਆਜ ਦਰਾਂ ਵਿੱਚ 25 ਬੇਸਿਸ ਪੁਆਇੰਟ ਦੀ ਕਟੌਤੀ ਕਰ ਦਿੱਤੀ ਹੈ। ਇਸ ਫੈਸਲੇ ਕਾਰਨ ਵੱਡੇ ਨਿਵੇਸ਼ਕਾਂ ਨੇ ਬਾਂਡਾਂ ਵਿੱਚੋਂ ਪੈਸਾ ਕੱਢ ਕੇ ਸਿੱਧਾ ਡਿਜੀਟਲ ਸੰਪਤੀਆਂ ਵਿੱਚ ਲਗਾਉਣਾ ਸ਼ੁਰੂ ਕਰ ਦਿੱਤਾ ਹੈ, ਜਿਸ ਨਾਲ ਬਿਟਕੋਇਨ ਦੀ ਕੀਮਤ ਤੇਜ਼ੀ ਨਾਲ ਵਧੀ ਹੈ।",
                    "impact": "ਵੱਡਾ ਅਸਰ", "type": "bullish", "time": "ਹੁਣੇ-ਹੁਣੇ"
                }},
                {{
                    "title": "SEC ਨੇ ਐਥੇਰੀਅਮ ETF ਲਈ ਆਪਸ਼ਨ ਟ੍ਰੇਡਿੰਗ ਨੂੰ ਮਨਜ਼ੂਰੀ ਦਿੱਤੀ",
                    "summary": "ਵੱਡੇ ਨਿਵੇਸ਼ਕ ਹੁਣ ਐਥੇਰੀਅਮ ਡੈਰੀਵੇਟਿਵਜ਼ ਦਾ ਆਸਾਨੀ ਨਾਲ ਫਾਇਦਾ ਉਠਾ ਸਕਦੇ ਹਨ।",
                    "full": "ਸਿਕਿਉਰਿਟੀਜ਼ ਐਂਡ ਐਕਸਚੇਂਜ ਕਮਿਸ਼ਨ (SEC) ਨੇ ਅਧਿਕਾਰਤ ਤੌਰ 'ਤੇ ਸਪਾਟ ਐਥੇਰੀਅਮ ETF ਲਈ ਆਪਸ਼ਨ ਟ੍ਰੇਡਿੰਗ ਨੂੰ ਹਰੀ ਝੰਡੀ ਦੇ ਦਿੱਤੀ ਹੈ। ਮਾਹਰਾਂ ਦਾ ਮੰਨਣਾ ਹੈ ਕਿ ਇਸ ਨਾਲ ਐਥੇਰੀਅਮ ਦੀ ਟ੍ਰੇਡਿੰਗ ਵਾਲੀਅਮ ਵਿੱਚ 45% ਦਾ ਉਛਾਲ ਆਇਆ ਹੈ।",
                    "impact": "ਤੇਜ਼ੀ (BULLISH)", "type": "bullish", "time": "20 ਮਿੰਟ ਪਹਿਲਾਂ"
                }}
            ]
        }};

        let currentLang = 'en';

        // Toggle 3-Dot Dropdown Menu
        function toggleLangMenu(e) {{
            e.stopPropagation();
            document.getElementById('lang-dropdown').classList.toggle('show');
        }}

        // Close dropdown when clicking anywhere else
        window.addEventListener('click', function() {{
            document.getElementById('lang-dropdown').classList.remove('show');
        }});

        // Change Language and Re-render News
        function changeLanguage(lang) {{
            currentLang = lang;
            
            // UI updates for selected language indicator
            document.querySelectorAll('.dropdown-menu div').forEach(div => div.classList.remove('selected'));
            document.getElementById(`lang-${{lang}}`).classList.add('selected');
            
            renderAINews();
        }}

        // Render AI News Setup
        function renderAINews() {{
            const container = document.getElementById('ai-news-container');
            container.innerHTML = '';
            
            const selectedNews = newsDatabase[currentLang];
            
            selectedNews.forEach((news, index) => {{
                let impactClass = news.type === 'bullish' ? 'impact-bullish' : 'impact-bearish';
                
                container.innerHTML += `
                    <div class="news-card" onclick="openNewsModal(${{index}})">
                        <div class="news-meta">
                            <span class="news-time">⏱️ ${{news.time}}</span>
                            <span class="impact-badge ${{impactClass}}">${{news.impact}}</span>
                        </div>
                        <div class="news-title">${{news.title}}</div>
                        <div class="news-summary">${{news.summary}}</div>
                        <div class="click-hint">Click for full info ➔</div>
                    </div>
                `;
            }});
        }}

        // Open Modal Box (Full Information Window)
        function openNewsModal(index) {{
            const news = newsDatabase[currentLang][index];
            let impactClass = news.type === 'bullish' ? 'impact-bullish' : 'impact-bearish';

            document.getElementById('modal-meta').innerHTML = `
                <span style="font-size:11px; color: var(--text-secondary);">⏱️ ${{news.time}}</span>
                <span class="impact-badge ${{impactClass}}" style="float:right;">${{news.impact}}</span>
            `;
            document.getElementById('modal-title').innerText = news.title;
            document.getElementById('modal-body').innerText = news.full;
            
            document.getElementById('newsModal').style.display = 'flex';
        }}

        function closeNewsModal() {{
            document.getElementById('newsModal').style.display = 'none';
        }}

        // Tab Switcher
        function switchTab(tabId, navId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            document.getElementById(navId).classList.add('active');
        }}

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

        function rerunApp() {{ window.location.reload(); }}
        function rebootApp() {{ if(confirm("Reboot system?")) window.location.reload(); }}
        function changeTheme(val) {{ document.documentElement.setAttribute('data-theme', val); }}

        window.onload = function() {{
            renderTopCards();
            renderCoinsList();
            renderAINews();
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(dashboard_html, height=750, scrolling=True)
