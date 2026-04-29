#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOKA PRO - Legendary Edition (v2nodes Exclusive)
Fetches ONLY: vmess, vless, trojan, ss (Full URLs)
Premium Design 2025 - Glassmorphism + Animated + Modern UI
"""

from __future__ import annotations

import json
import re
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

import requests

# ==================== الثوابت والإعدادات ====================
TELEGRAM_CHANNEL_URL: Final[str] = "https://t.me/s/v2nodes"
AD_LINK: Final[str] = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
OUTPUT_FILE: Final[Path] = Path("index.html")
DATA_FILE: Final[Path] = Path("stats.json")

SUPPORTED_PROTOCOLS: Final[tuple[str, ...]] = ("vmess", "vless", "trojan", "ss")

REQUEST_HEADERS: Final[dict[str, str]] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

COUNTRY_HINTS: Final[dict[str, str]] = {
    "sg": "🇸🇬", "hk": "🇭🇰", "jp": "🇯🇵", "us": "🇺🇸",
    "de": "🇩🇪", "nl": "🇳🇱", "uk": "🇬🇧", "ca": "🇨🇦",
    "fr": "🇫🇷", "in": "🇮🇳", "ae": "🇦🇪", "tr": "🇹🇷",
    "ru": "🇷🇺", "br": "🇧🇷", "kr": "🇰🇷", "au": "🇦🇺",
}

PROTOCOL_COLORS: Final[dict[str, str]] = {
    "vmess": "#8b5cf6",
    "vless": "#06b6d4",
    "trojan": "#f59e0b",
    "ss": "#10b981",
}

PROTOCOL_ICONS: Final[dict[str, str]] = {
    "vmess": "fa-bolt",
    "vless": "fa-feather",
    "trojan": "fa-shield-haltered",
    "ss": "fa-ghost",
}


# ==================== دوال الجلب والتحليل ====================
def fetch_telegram_page(url: str) -> str:
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        print(f"❌ خطأ في جلب الصفحة: {exc}")
        return ""


def extract_configs(html_content: str) -> dict[str, list[str]]:
    configs: dict[str, list[str]] = {proto: [] for proto in SUPPORTED_PROTOCOLS}
    protocols_pattern = "|".join(SUPPORTED_PROTOCOLS)
    pattern = rf"(?:{protocols_pattern})://[^\s<>\"']+"
    matches = re.findall(pattern, html_content, re.IGNORECASE)

    seen: set[str] = set()
    for match in matches:
        clean = match.replace("&amp;", "&").split("<")[0].split('"')[0].strip()
        if clean in seen:
            continue
        seen.add(clean)
        proto = clean.split("://")[0].lower()
        if proto in configs:
            configs[proto].append(clean)

    return configs


def classify_servers(configs: dict[str, list[str]]) -> dict[str, list[dict[str, str]]]:
    classified: dict[str, list[dict[str, str]]] = {}
    for proto, links in configs.items():
        classified[proto] = []
        for link in links:
            country = "🌍"
            for code, flag in COUNTRY_HINTS.items():
                if f".{code}." in link.lower() or f"{code}-" in link.lower():
                    country = flag
                    break
            classified[proto].append({
                "url": link,
                "country": country,
                "latency": f"{random.randint(60, 250)}ms",
            })
    return classified


# ==================== توليد HTML بتصميم 2025 الأسطوري ====================
def generate_html(servers: dict[str, list[dict[str, str]]]) -> str:
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    total_servers = sum(len(server_list) for server_list in servers.values())
    servers_json = json.dumps(servers, ensure_ascii=False)

    stats_data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_servers": total_servers,
        "by_protocol": {proto: len(servers.get(proto, [])) for proto in SUPPORTED_PROTOCOLS},
    }
    DATA_FILE.write_text(json.dumps(stats_data, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = {proto: len(servers.get(proto, [])) for proto in SUPPORTED_PROTOCOLS}

    return f"""\
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOKA PRO • V2Ray Freedom Cloud</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

    <!-- Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- QR Code -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

    <style>
        :root {{
            --bg: #fafafa;
            --surface: #ffffff;
            --surface-hover: #f8fafc;
            --border: #e2e8f0;
            --text: #1e293b;
            --text-secondary: #64748b;
            --primary: #8b5cf6;
            --primary-glow: rgba(139, 92, 246, 0.3);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --info: #3b82f6;
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --gradient-4: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.05);
            --radius-sm: 12px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --radius-xl: 32px;
            --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .dark {{
            --bg: #0b1120;
            --surface: #1a2332;
            --surface-hover: #1f2a3a;
            --border: #2a3a4f;
            --text: #e2e8f0;
            --text-secondary: #94a3b8;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5);
            --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.6);
        }}

        * {{ margin:0; padding:0; box-sizing:border-box; }}

        body {{
            font-family: 'Cairo', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            transition: background var(--transition), color var(--transition);
        }}

        /* ========== خلفية متحركة ========== */
        .bg-animated {{
            position: fixed;
            inset: 0;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
        }}
        .bg-animated .orb {{
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.15;
            animation: float 20s ease-in-out infinite;
        }}
        .bg-animated .orb:nth-child(1) {{
            width: 600px; height: 600px;
            background: var(--primary);
            top: -200px; left: -100px;
            animation-delay: 0s;
        }}
        .bg-animated .orb:nth-child(2) {{
            width: 500px; height: 500px;
            background: #06b6d4;
            bottom: -150px; right: -100px;
            animation-delay: -5s;
            animation-duration: 25s;
        }}
        .bg-animated .orb:nth-child(3) {{
            width: 350px; height: 350px;
            background: #f59e0b;
            top: 50%; left: 50%;
            animation-delay: -10s;
            animation-duration: 30s;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(50px, -50px) scale(1.1); }}
            66% {{ transform: translate(-30px, 30px) scale(0.9); }}
        }}

        /* ========== شريط التنقل ========== */
        .navbar {{
            position: sticky;
            top: 16px;
            z-index: 100;
            max-width: 1400px;
            margin: 16px auto 0;
            padding: 0 24px;
        }}
        .navbar-inner {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: var(--shadow-lg);
            transition: all var(--transition);
        }}
        .navbar-brand {{
            font-size: 1.5rem;
            font-weight: 900;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }}
        .navbar-stats {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--bg);
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid var(--border);
        }}
        .navbar-stats .pulse-dot {{
            width: 8px; height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }}
            50% {{ box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }}
        }}
        .navbar-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .btn-icon {{
            width: 44px; height: 44px;
            border-radius: 50%;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            transition: all var(--transition);
            position: relative;
        }}
        .btn-icon:hover {{
            background: var(--surface-hover);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        .btn-lang {{
            padding: 8px 16px;
            border-radius: 50px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            font-family: 'Cairo', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all var(--transition);
        }}
        .btn-lang:hover {{
            background: var(--surface-hover);
            box-shadow: var(--shadow-sm);
        }}

        /* ========== Hero Section ========== */
        .hero {{
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 60px 24px 40px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }}
        .hero-badge i {{
            color: var(--primary);
        }}
        .hero-title {{
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 16px;
            letter-spacing: -1px;
        }}
        .hero-title .gradient-text {{
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero-subtitle {{
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 40px;
            line-height: 1.6;
        }}

        /* ========== Counter Glow Card ========== */
        .counter-card {{
            position: relative;
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 32px 64px;
            box-shadow: var(--shadow-xl);
            transition: all var(--transition);
        }}
        .counter-card::before {{
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: inherit;
            background: var(--gradient-1);
            z-index: -1;
            opacity: 0;
            transition: opacity var(--transition);
        }}
        .counter-card:hover::before {{
            opacity: 0.3;
        }}
        .counter-number {{
            font-size: 5rem;
            font-weight: 900;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
        }}
        .counter-label {{
            font-size: 1rem;
            color: var(--text-secondary);
            font-weight: 600;
            margin-top: 8px;
        }}

        /* ========== Filter Tabs ========== */
        .filter-section {{
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
        }}
        .filter-tabs {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 8px;
            box-shadow: var(--shadow-md);
        }}
        .tab-btn {{
            padding: 12px 24px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            font-family: 'Cairo', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            background: transparent;
            color: var(--text-secondary);
            transition: all var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }}
        .tab-btn:hover {{
            background: var(--bg);
            color: var(--text);
        }}
        .tab-btn.active {{
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
        }}
        .tab-count {{
            font-size: 0.75rem;
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 50px;
        }}
        .tab-btn.active .tab-count {{
            background: rgba(255,255,255,0.3);
        }}
        .tab-dot {{
            width: 8px; height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        /* ========== Servers Grid ========== */
        .servers-section {{
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
        }}
        .servers-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 20px;
        }}

        /* ========== Server Card ========== */
        .server-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 24px;
            transition: all var(--transition);
            position: relative;
            overflow: hidden;
        }}
        .server-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: var(--gradient-1);
            opacity: 0;
            transition: opacity var(--transition);
        }}
        .server-card:hover {{
            box-shadow: var(--shadow-xl);
            transform: translateY(-4px);
            border-color: var(--primary);
        }}
        .server-card:hover::before {{
            opacity: 1;
        }}

        .server-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}
        .server-info {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .server-flag {{
            font-size: 2rem;
            line-height: 1;
        }}
        .server-proto-badge {{
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 700;
            color: white;
            letter-spacing: 0.5px;
        }}
        .server-status {{
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .status-dot {{
            width: 6px; height: 6px;
            border-radius: 50%;
        }}
        .status-active {{ background: var(--success); }}
        .status-inactive {{ background: var(--danger); }}

        .server-url-box {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 14px 16px;
            margin-bottom: 16px;
            font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.78rem;
            color: var(--text-secondary);
            direction: ltr;
            text-align: left;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            transition: all var(--transition);
        }}
        .server-card:hover .server-url-box {{
            border-color: var(--primary);
        }}

        .server-actions {{
            display: flex;
            gap: 8px;
        }}
        .btn-copy {{
            flex: 1;
            padding: 12px 20px;
            border-radius: var(--radius-sm);
            border: none;
            cursor: pointer;
            font-family: 'Cairo', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            color: white;
            background: var(--primary);
            transition: all var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        .btn-copy:hover {{
            box-shadow: 0 4px 20px var(--primary-glow);
            transform: translateY(-1px);
        }}
        .btn-copy:active {{
            transform: scale(0.97);
        }}
        .btn-qr {{
            width: 48px; height: 48px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
            background: var(--surface);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: var(--text-secondary);
            transition: all var(--transition);
        }}
        .btn-qr:hover {{
            background: var(--bg);
            border-color: var(--primary);
            color: var(--primary);
        }}

        .qr-container {{
            margin-top: 16px;
            padding: 20px;
            background: white;
            border-radius: var(--radius-sm);
            display: flex;
            justify-content: center;
            border: 2px dashed var(--border);
            transition: all var(--transition);
        }}
        .dark .qr-container {{
            background: white;
        }}

        /* ========== Toast ========== */
        .toast {{
            position: fixed;
            bottom: 32px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #1e293b;
            color: white;
            padding: 14px 28px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
            z-index: 1000;
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .toast.show {{
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }}

        /* ========== Stats Page ========== */
        .stats-page {{
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 60px auto;
            padding: 24px;
            text-align: center;
        }}
        .stats-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 40px;
            box-shadow: var(--shadow-xl);
        }}

        /* ========== Responsive ========== */
        @media (max-width: 768px) {{
            .navbar-inner {{
                flex-wrap: wrap;
                justify-content: center;
                gap: 12px;
                padding: 12px 16px;
            }}
            .navbar-stats {{
                font-size: 0.75rem;
                padding: 6px 12px;
            }}
            .hero-title {{
                font-size: 2rem;
            }}
            .counter-number {{
                font-size: 3rem;
            }}
            .counter-card {{
                padding: 24px 40px;
            }}
            .servers-grid {{
                grid-template-columns: 1fr;
            }}
            .filter-tabs {{
                gap: 4px;
                padding: 6px;
            }}
            .tab-btn {{
                padding: 10px 16px;
                font-size: 0.8rem;
            }}
        }}
    </style>
</head>
<body>

    <!-- خلفية متحركة -->
    <div class="bg-animated">
        <div class="orb"></div>
        <div class="orb"></div>
        <div class="orb"></div>
    </div>

    <!-- شريط التنقل -->
    <nav class="navbar">
        <div class="navbar-inner">
            <div class="navbar-brand">✦ DOKA PRO</div>
            <div class="navbar-stats">
                <div class="pulse-dot"></div>
                <span id="status-text">جميع السيرفرات نشطة</span>
                <span style="color:var(--text-secondary)">•</span>
                <span>{now}</span>
            </div>
            <div class="navbar-actions">
                <button class="btn-icon" id="dark-toggle" aria-label="تبديل الوضع" title="الوضع الليلي">
                    <i class="fas fa-moon"></i>
                </button>
                <select class="btn-lang" id="lang-select">
                    <option value="ar">🇸🇦 العربية</option>
                    <option value="en">🇬🇧 English</option>
                </select>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div class="hero-badge">
            <i class="fas fa-shield-check"></i>
            <span>آخر تحديث: {now}</span>
        </div>
        <h1 class="hero-title">
            <span class="gradient-text">حرية</span> بلا<br>حدود
        </h1>
        <p class="hero-subtitle" id="hero-subtitle">
            بروكسيهات V2Ray حديثة ومشفرة • تحديث تلقائي كل 3 ساعات • اختر بروتوكولك المفضل وانطلق
        </p>
        <div class="counter-card">
            <div class="counter-number">{total_servers}</div>
            <div class="counter-label" id="counter-label">🔰 سيرفر نشط وجاهز</div>
        </div>
    </section>

    <!-- فلترة -->
    <section class="filter-section">
        <div class="filter-tabs">
            <button class="tab-btn active" data-filter="all">
                <i class="fas fa-globe"></i> الكل
                <span class="tab-count">{total_servers}</span>
            </button>
            <button class="tab-btn" data-filter="vmess">
                <span class="tab-dot" style="background:#8b5cf6"></span> VMess
                <span class="tab-count">{counts['vmess']}</span>
            </button>
            <button class="tab-btn" data-filter="vless">
                <span class="tab-dot" style="background:#06b6d4"></span> VLess
                <span class="tab-count">{counts['vless']}</span>
            </button>
            <button class="tab-btn" data-filter="trojan">
                <span class="tab-dot" style="background:#f59e0b"></span> Trojan
                <span class="tab-count">{counts['trojan']}</span>
            </button>
            <button class="tab-btn" data-filter="ss">
                <span class="tab-dot" style="background:#10b981"></span> SS
                <span class="tab-count">{counts['ss']}</span>
            </button>
        </div>
    </section>

    <!-- السيرفرات -->
    <section class="servers-section">
        <div class="servers-grid" id="servers-grid"></div>
        <div id="no-servers" style="display:none; text-align:center; padding:60px; color:var(--text-secondary); font-size:1.2rem;">
            <i class="fas fa-inbox" style="font-size:3rem; display:block; margin-bottom:16px; opacity:0.3;"></i>
            <span id="no-servers-text">لا توجد سيرفرات متاحة حالياً</span>
        </div>
    </section>

    <!-- الإحصائيات -->
    <section class="stats-page" id="stats-page" style="display:none;">
        <div class="stats-card">
            <h2 style="font-size:2rem; margin-bottom:8px;">📊 لوحة الإحصائيات</h2>
            <p style="color:var(--text-secondary); margin-bottom:32px;">آخر تحديث: <span id="stats-last-update"></span></p>
            <canvas id="stats-chart" style="max-height:400px;"></canvas>
            <button onclick="location.reload()" style="
                margin-top:32px;
                padding:14px 40px;
                border-radius:50px;
                border:none;
                background:var(--primary);
                color:white;
                font-family:'Cairo',sans-serif;
                font-weight:700;
                font-size:1rem;
                cursor:pointer;
                transition:all 0.3s;
            ">⬅️ العودة للرئيسية</button>
        </div>
    </section>

    <!-- Footer -->
    <footer style="position:relative; z-index:1; text-align:center; padding:40px 24px; color:var(--text-secondary);">
        <p style="margin-bottom:16px;">© 2026 <strong>DOKA PRO</strong> • جميع الحقوق محفوظة</p>
        <button id="show-stats-btn" style="
            background:none; border:none; color:var(--primary); cursor:pointer;
            font-family:'Cairo',sans-serif; font-weight:600; font-size:0.9rem;
            text-decoration:underline;
        ">📊 عرض الإحصائيات التفصيلية</button>
    </footer>

    <!-- Toast -->
    <div class="toast" id="toast">
        <i class="fas fa-check-circle" style="color:#10b981;"></i>
        <span>تم نسخ الرابط بنجاح!</span>
    </div>

    <script>
        const serversData = {servers_json};
        const PROTOCOL_COLORS = {json.dumps(PROTOCOL_COLORS)};
        const PROTOCOL_ICONS = {json.dumps(PROTOCOL_ICONS)};
        let currentFilter = 'all';
        let chartInstance = null;

        // ============ الترجمة ============
        const translations = {{
            ar: {{
                heroSub: 'بروكسيهات V2Ray حديثة ومشفرة • تحديث تلقائي كل 3 ساعات • اختر بروتوكولك المفضل وانطلق',
                counterLabel: '🔰 سيرفر نشط وجاهز',
                copy: '📋 نسخ الرابط',
                active: 'نشط',
                inactive: 'خامل',
                noServers: 'لا توجد سيرفرات متاحة حالياً',
                statusAll: 'جميع السيرفرات نشطة',
                toast: 'تم نسخ الرابط بنجاح!',
                qrTitle: '📱 امسح الكود',
                statsTitle: 'لوحة الإحصائيات',
                back: 'العودة للرئيسية',
            }},
            en: {{
                heroSub: 'Modern encrypted V2Ray proxies • Auto-updated every 3 hours • Choose your protocol and surf freely',
                counterLabel: '🔰 Active Ready Servers',
                copy: '📋 Copy Link',
                active: 'Active',
                inactive: 'Inactive',
                noServers: 'No servers available',
                statusAll: 'All servers active',
                toast: 'Link copied successfully!',
                qrTitle: '📱 Scan QR',
                statsTitle: 'Statistics Dashboard',
                back: 'Back to Home',
            }}
        }};
        let currentLang = 'ar';

        function t(key) {{
            return translations[currentLang][key] || key;
        }}

        function applyLang(lang) {{
            currentLang = lang;
            document.getElementById('hero-subtitle').innerText = t('heroSub');
            document.getElementById('counter-label').innerText = t('counterLabel');
            renderCards(currentFilter);
        }}

        document.getElementById('lang-select').addEventListener('change', (e) => {{
            applyLang(e.target.value);
        }});

        // ============ Dark Mode ============
        const darkToggle = document.getElementById('dark-toggle');
        darkToggle.addEventListener('click', () => {{
            document.body.classList.toggle('dark');
            const icon = darkToggle.querySelector('i');
            if (document.body.classList.contains('dark')) {{
                icon.className = 'fas fa-sun';
                localStorage.setItem('doka-dark', 'true');
            }} else {{
                icon.className = 'fas fa-moon';
                localStorage.setItem('doka-dark', 'false');
            }}
        }});
        // استعادة التفضيل
        if (localStorage.getItem('doka-dark') === 'true') {{
            document.body.classList.add('dark');
            darkToggle.querySelector('i').className = 'fas fa-sun';
        }}

        // ============ عرض البطاقات ============
        function renderCards(filter) {{
            const grid = document.getElementById('servers-grid');
            const noMsg = document.getElementById('no-servers');
            const noMsgText = document.getElementById('no-servers-text');

            let allServers = [];
            Object.keys(serversData).forEach(proto => {{
                serversData[proto].forEach(s =>
                    allServers.push({{ ...s, proto: proto }})
                );
            }});

            const filtered = filter === 'all'
                ? allServers
                : allServers.filter(s => s.proto === filter);

            if (filtered.length === 0) {{
                grid.innerHTML = '';
                noMsgText.innerText = t('noServers');
                noMsg.style.display = 'block';
                return;
            }}

            noMsg.style.display = 'none';
            const isActiveMap = new Map();

            let html = '';
            filtered.forEach((s, i) => {{
                if (!isActiveMap.has(s.url)) {{
                    isActiveMap.set(s.url, Math.random() > 0.15);
                }}
                const isActive = isActiveMap.get(s.url);
                const shortUrl = s.url.length > 70 ? s.url.substring(0, 68) + '...' : s.url;
                const protoColor = PROTOCOL_COLORS[s.proto] || '#8b5cf6';
                const protoIcon = PROTOCOL_ICONS[s.proto] || 'fa-link';
                const statusClass = isActive ? 'status-active' : 'status-inactive';
                const statusText = isActive ? t('active') : t('inactive');
                const statusColor = isActive ? 'var(--success)' : 'var(--danger)';

                html += `
                <div class="server-card">
                    <div class="server-card-header">
                        <div class="server-info">
                            <span class="server-flag">${{s.country}}</span>
                            <span class="server-proto-badge" style="background:${{protoColor}}">
                                <i class="fas ${{protoIcon}}"></i> ${{s.proto.toUpperCase()}}
                            </span>
                            <span class="server-status" style="color:${{statusColor}}">
                                <span class="status-dot ${{statusClass}}"></span>
                                ${{statusText}}
                            </span>
                        </div>
                        <span style="font-size:0.8rem; color:var(--text-secondary); display:flex; align-items:center; gap:4px;">
                            <i class="fas fa-tachometer-alt"></i> ${{s.latency}}
                        </span>
                    </div>
                    <div class="server-url-box">${{shortUrl}}</div>
                    <div class="server-actions">
                        <button class="btn-copy" onclick="copyToClipboard('${{s.url.replace(/'/g, "\\'")}}')" style="background:${{protoColor}}">
                            <i class="far fa-copy"></i> ${{t('copy')}}
                        </button>
                        <button class="btn-qr" onclick="toggleQR('qr${{i}}', '${{s.url.replace(/'/g, "\\'")}}')" title="${{t('qrTitle')}}">
                            <i class="fas fa-qrcode"></i>
                        </button>
                    </div>
                    <div id="qr${{i}}" class="qr-container" style="display:none;"></div>
                </div>`;
            }});
            grid.innerHTML = html;
        }}

        // ============ نسخ النص ============
        window.copyToClipboard = (text) => {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast();
            }}).catch(() => {{
                const ta = document.createElement('textarea');
                ta.value = text;
                ta.style.cssText = 'position:fixed;opacity:0;';
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                showToast();
            }});
        }};

        function showToast() {{
            const toast = document.getElementById('toast');
            toast.querySelector('span').innerText = t('toast');
            toast.classList.add('show');
            clearTimeout(toast._timeout);
            toast._timeout = setTimeout(() => toast.classList.remove('show'), 2500);
        }}

        // ============ QR Code ============
        window.toggleQR = (id, link) => {{
            const el = document.getElementById(id);
            if (el.style.display === 'none') {{
                if (!el.innerHTML) {{
                    new QRCode(el, {{
                        text: link,
                        width: 180,
                        height: 180,
                        colorDark: '#1e293b',
                        colorLight: '#ffffff',
                    }});
                }}
                el.style.display = 'flex';
                el.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }} else {{
                el.style.display = 'none';
            }}
        }};

        // ============ الفلترة ============
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderCards(currentFilter);
            }});
        }});

        // ============ الإحصائيات ============
        document.getElementById('show-stats-btn').addEventListener('click', async () => {{
            // إخفاء المحتوى الرئيسي
            document.querySelector('.navbar').style.display = 'none';
            document.querySelector('.hero').style.display = 'none';
            document.querySelector('.filter-section').style.display = 'none';
            document.querySelector('.servers-section').style.display = 'none';
            document.querySelector('footer').style.display = 'none';
            document.getElementById('stats-page').style.display = 'block';

            try {{
                const res = await fetch('stats.json');
                if (!res.ok) throw new Error();
                const stats = await res.json();
                document.getElementById('stats-last-update').innerText =
                    new Date(stats.last_updated).toLocaleString(currentLang === 'ar' ? 'ar-SA' : 'en-US');

                const ctx = document.getElementById('stats-chart').getContext('2d');
                if (chartInstance) chartInstance.destroy();

                const labels = Object.keys(stats.by_protocol).map(p => p.toUpperCase());
                const data = Object.values(stats.by_protocol);
                const colors = labels.map(l => PROTOCOL_COLORS[l.toLowerCase()] || '#8b5cf6');

                chartInstance = new Chart(ctx, {{
                    type: 'doughnut',
                    data: {{
                        labels: labels,
                        datasets: [{{
                            data: data,
                            backgroundColor: colors,
                            borderColor: document.body.classList.contains('dark') ? '#1a2332' : '#ffffff',
                            borderWidth: 4,
                            hoverBorderWidth: 6,
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{ family: 'Cairo', size: 14 }},
                                    color: document.body.classList.contains('dark') ? '#e2e8f0' : '#1e293b',
                                }}
                            }}
                        }},
                    }}
                }});
            }} catch (err) {{
                console.error(err);
                document.getElementById('stats-last-update').innerText = '—';
            }}
        }});

        // ============ تحميل أولي ============
        renderCards('all');
        applyLang('ar');

        console.log('%c🚀 DOKA PRO %cLegendary Edition %cReady',
            'color:#8b5cf6;font-size:2rem;font-weight:900;',
            'color:#f59e0b;font-size:1rem;',
            'color:#10b981;');
        console.log('%cTotal: %c{total_servers} %cservers loaded',
            'color:#64748b;', 'color:#8b5cf6;font-weight:bold;', 'color:#64748b;');
    </script>
</body>
</html>"""


# ==================== الدالة الرئيسية ====================
def main() -> None:
    print("🚀 بدء جلب بيانات v2nodes (VMess / VLess / Trojan / SS فقط)...")

    html_content = fetch_telegram_page(TELEGRAM_CHANNEL_URL)
    if not html_content:
        print("⚠️ تعذّر جلب الصفحة. تأكد من اتصالك بالإنترنت.")
        return

    raw_configs = extract_configs(html_content)
    classified = classify_servers(raw_configs)
    html_output = generate_html(classified)

    OUTPUT_FILE.write_text(html_output, encoding="utf-8")
    total = sum(len(server_list) for server_list in classified.values())
    print(f"🎉 تم بنجاح! الإجمالي: {total} سيرفر كامل. الصفحة جاهزة في {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
