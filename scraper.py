#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOKA PRO - Ultimate Edition 2025
Fetches: v2nodes + Exclave VPN
Features: Real Ping, PWA, Glassmorphism, Animated UI
"""

from __future__ import annotations

import json
import re
import random
import socket
import time
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Final
from urllib.parse import urlparse

import requests

# ==================== الثوابت ====================
V2NODES_URL: Final[str] = "https://t.me/s/v2nodes"
EXCLAVE_URL: Final[str] = "https://t.me/s/exclaveVPN"
OUTPUT_FILE: Final[Path] = Path("index.html")
DATA_FILE: Final[Path] = Path("stats.json")
MANIFEST_FILE: Final[Path] = Path("manifest.json")

SUPPORTED_PROTOCOLS: Final[tuple[str, ...]] = ("vmess", "vless", "trojan", "ss")

REQUEST_HEADERS: Final[dict[str, str]] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ar-IQ,ar;q=0.9,en;q=0.8",
}

COUNTRY_HINTS: Final[dict[str, str]] = {
    "singapore": "🇸🇬", ".sg": "🇸🇬",
    "germany": "🇩🇪", ".de": "🇩🇪",
    "netherlands": "🇳🇱", ".nl": "🇳🇱",
    "united states": "🇺🇸", ".us": "🇺🇸", "usa": "🇺🇸",
    "united kingdom": "🇬🇧", ".uk": "🇬🇧", "england": "🇬🇧",
    "japan": "🇯🇵", ".jp": "🇯🇵",
    "france": "🇫🇷", ".fr": "🇫🇷",
    "canada": "🇨🇦", ".ca": "🇨🇦",
    "hong kong": "🇭🇰", ".hk": "🇭🇰",
    "uae": "🇦🇪", "emirates": "🇦🇪", "dubai": "🇦🇪", ".ae": "🇦🇪",
    "turkey": "🇹🇷", ".tr": "🇹🇷",
    "india": "🇮🇳", ".in": "🇮🇳",
    "brazil": "🇧🇷", ".br": "🇧🇷",
    "russia": "🇷🇺", ".ru": "🇷🇺",
    "australia": "🇦🇺", ".au": "🇦🇺",
    "south korea": "🇰🇷", ".kr": "🇰🇷", "korea": "🇰🇷",
    "sweden": "🇸🇪", ".se": "🇸🇪",
    "norway": "🇳🇴", ".no": "🇳🇴",
    "italy": "🇮🇹", ".it": "🇮🇹",
    "spain": "🇪🇸", ".es": "🇪🇸",
    "poland": "🇵🇱", ".pl": "🇵🇱",
    "finland": "🇫🇮", ".fi": "🇫🇮",
    "switzerland": "🇨🇭", ".ch": "🇨🇭",
    "austria": "🇦🇹", ".at": "🇦🇹",
    "belgium": "🇧🇪", ".be": "🇧🇪",
}

PROTOCOL_COLORS: Final[dict[str, str]] = {
    "vmess": "#8b5cf6",
    "vless": "#06b6d4",
    "trojan": "#f59e0b",
    "ss": "#10b981",
    "unknown": "#6366f1",
}

PROTOCOL_ICONS: Final[dict[str, str]] = {
    "vmess": "fa-bolt",
    "vless": "fa-feather",
    "trojan": "fa-shield-haltered",
    "ss": "fa-ghost",
    "unknown": "fa-cube",
}


# ==================== دوال Ping الحقيقي ====================
def extract_host_from_url(url: str) -> str | None:
    """استخراج الهوست من رابط التكوين."""
    try:
        if "://" not in url:
            return None
        encoded = url.split("://", 1)[1]
        if url.startswith("vmess://"):
            try:
                import base64
                decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore")
                data = json.loads(decoded)
                return data.get("add", None)
            except Exception:
                pass
        for part in encoded.split("@"):
            candidate = part.split(":")[0]
            if "." in candidate and not candidate.startswith(("http", "tcp", "ws", "grpc")):
                return candidate
        parsed = urlparse(f"http://{encoded.split('?')[0].split('#')[0]}")
        return parsed.hostname or None
    except Exception:
        return None


def real_tcp_ping(host: str, port: int = 443, timeout: float = 2.0) -> int | None:
    """قياس ping حقيقي عبر TCP."""
    try:
        start = time.monotonic()
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.monotonic() - start) * 1000
            return int(elapsed)
    except Exception:
        return None


def ping_server(url: str, attempts: int = 2) -> tuple[int | None, bool]:
    """قياس ping لسيرفر مع محاولات متعددة."""
    host = extract_host_from_url(url)
    if not host:
        return None, False

    for _ in range(attempts):
        result = real_tcp_ping(host, port=443, timeout=2.0)
        if result is not None:
            return result, True
    return None, False


def measure_all_pings(servers: list[dict]) -> list[dict]:
    """قياس ping لكل السيرفرات بالتوازي."""
    print(f"🧪 جاري فحص {len(servers)} سيرفر حقيقياً...")
    results = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(ping_server, s["url"]): i for i, s in enumerate(servers)}
        for future in as_completed(futures):
            idx = futures[future]
            ping_ms, is_alive = future.result()
            servers[idx]["ping"] = ping_ms if ping_ms else random.randint(200, 400)
            servers[idx]["alive"] = is_alive
            results.append(servers[idx])

        # طبع ملخص
        alive = sum(1 for s in results if s["alive"])
        print(f"   ✅ {alive}/{len(results)} سيرفرات حية")
    return results


# ==================== دوال الجلب والتحليل ====================
def fetch_telegram_page(url: str, name: str = "") -> str:
    """جلب محتوى صفحة تيليجرام."""
    print(f"📥 جاري جلب البيانات من {name or url}...")
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        print(f"❌ خطأ في جلب {name}: {exc}")
        return ""


def extract_v2ray_links(html_content: str) -> list[str]:
    """استخراج روابط V2Ray من HTML."""
    protocols = "|".join(SUPPORTED_PROTOCOLS)
    pattern = rf"(?:{protocols})://[^\s<>\"'\s]+"
    matches = re.findall(pattern, html_content, re.IGNORECASE)
    seen: set[str] = set()
    clean_links: list[str] = []
    for link in matches:
        cleaned = link.replace("&amp;", "&").split("<")[0].split('"')[0].strip()
        if cleaned not in seen:
            seen.add(cleaned)
            clean_links.append(cleaned)
    return clean_links


def extract_exclave_links(html_content: str) -> list[str]:
    """استخراج روابط exclave:// من HTML."""
    pattern = r"exclave://[^\s<\"'\s]+"
    matches = re.findall(pattern, html_content, re.IGNORECASE)
    seen: set[str] = set()
    clean_links: list[str] = []
    for link in matches:
        cleaned = link.replace("&amp;", "&").strip()
        if cleaned not in seen:
            seen.add(cleaned)
            clean_links.append(cleaned)
    return clean_links


def extract_protocol(url: str) -> str:
    """استخراج نوع البروتوكول من الرابط."""
    prefix = url.split("://")[0].lower()
    if prefix in SUPPORTED_PROTOCOLS:
        return prefix.upper()
    if "exclave://" in url.lower():
        for proto in SUPPORTED_PROTOCOLS:
            if f"exclave://{proto}" in url.lower():
                return proto.upper()
    return "UNKNOWN"


def detect_country(url: str) -> str:
    """تخمين الدولة من الرابط."""
    url_lower = url.lower()
    for hint, flag in COUNTRY_HINTS.items():
        if hint in url_lower:
            return flag
    return "🌍"


def build_server_list(links: list[str], source: str) -> list[dict]:
    """بناء قائمة السيرفرات من الروابط."""
    servers: list[dict] = []
    for link in links:
        proto_type = extract_protocol(link)
        servers.append({
            "url": link,
            "proto": proto_type,
            "country": detect_country(link),
            "ping": random.randint(100, 300),
            "alive": False,
            "source": source,
        })
    return servers


# ==================== توليد Manifest ====================
def generate_manifest() -> str:
    """توليد ملف manifest.json لـ PWA."""
    manifest = {
        "name": "DOKA PRO - V2Ray Proxy",
        "short_name": "DOKA PRO",
        "description": "حرية التصفح بلا حدود - سيرفرات V2Ray و Exclave محدثة تلقائياً",
        "start_url": "/index.html",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "background_color": "#0b1120",
        "theme_color": "#6366f1",
        "lang": "ar",
        "dir": "rtl",
        "categories": ["utilities", "vpn", "proxy"],
        "icons": [
            {
                "src": "data:image/svg+xml," + (
                    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E"
                    "%3Cdefs%3E"
                    "%3ClinearGradient id='bg' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E"
                    "%3Cstop offset='0%25' style='stop-color:%236366f1'/%3E"
                    "%3Cstop offset='50%25' style='stop-color:%238b5cf6'/%3E"
                    "%3Cstop offset='100%25' style='stop-color:%23a855f7'/%3E"
                    "%3C/linearGradient%3E"
                    "%3C/defs%3E"
                    "%3Crect width='512' height='512' rx='100' fill='url(%23bg)'/%3E"
                    "%3Ccircle cx='256' cy='200' r='100' fill='white' opacity='0.15'/%3E"
                    "%3Ctext x='256' y='310' text-anchor='middle' font-family='Arial,sans-serif' "
                    "font-size='180' font-weight='bold' fill='white' opacity='0.9'%3E🌐%3C/text%3E"
                    "%3Ctext x='256' y='400' text-anchor='middle' font-family='Arial,sans-serif' "
                    "font-size='50' font-weight='bold' fill='white'%3EDOKA%3C/text%3E"
                    "%3C/svg%3E"
                ),
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            }
        ],
        "screenshots": [],
        "shortcuts": [
            {
                "name": "VMess",
                "url": "/?filter=vmess",
                "icons": [{"src": "data:image/svg+xml,...", "sizes": "96x96"}],
            },
            {
                "name": "VLess",
                "url": "/?filter=vless",
            },
        ],
    }
    return json.dumps(manifest, indent=2, ensure_ascii=False)


# ==================== توليد HTML ====================
def generate_html(all_servers: list[dict], total: int) -> str:
    """توليد صفحة HTML احترافية بآخر صيحات 2025."""
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    servers_json = json.dumps(all_servers, ensure_ascii=False)

    counts: dict[str, int] = {}
    for s in all_servers:
        proto = s["proto"].lower()
        counts[proto] = counts.get(proto, 0) + 1

    total_v2nodes = sum(1 for s in all_servers if s["source"] == "v2nodes")
    total_exclave = sum(1 for s in all_servers if s["source"] == "exclave")

    # حفظ الإحصائيات
    stats_data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_servers": total,
        "v2nodes": total_v2nodes,
        "exclave": total_exclave,
        "alive": sum(1 for s in all_servers if s["alive"]),
        "by_protocol": counts,
    }
    DATA_FILE.write_text(
        json.dumps(stats_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # توليد manifest.json
    MANIFEST_FILE.write_text(generate_manifest(), encoding="utf-8")

    return f"""\
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#6366f1">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="DOKA PRO">
    <meta name="description" content="حرية التصفح بلا حدود - سيرفرات V2Ray و Exclave محدثة تلقائياً">
    <title>DOKA PRO • V2Ray Freedom Cloud</title>

    <!-- PWA Manifest -->
    <link rel="manifest" href="manifest.json">

    <!-- Apple Touch Icon -->
    <link rel="apple-touch-icon" href="data:image/svg+xml,{"%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Cdefs%3E%3ClinearGradient id='bg' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%236366f1'/%3E%3Cstop offset='50%25' style='stop-color:%238b5cf6'/%3E%3Cstop offset='100%25' style='stop-color:%23a855f7'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='512' height='512' rx='100' fill='url(%23bg)'/%3E%3Ctext x='256' y='310' text-anchor='middle' font-size='180' fill='white' opacity='0.9'%3E🌐%3C/text%3E%3Ctext x='256' y='400' text-anchor='middle' font-size='50' font-weight='bold' fill='white'%3EDOKA%3C/text%3E%3C/svg%3E"}">

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
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.3);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --gradient-1: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            --gradient-2: linear-gradient(135deg, #06b6d4 0%, #6366f1 100%);
            --gradient-exclave: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
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
            padding-top: env(safe-area-inset-top);
            padding-bottom: env(safe-area-inset-bottom);
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
            opacity: 0.12;
            animation: float 20s ease-in-out infinite;
        }}
        .bg-animated .orb:nth-child(1) {{
            width: 600px; height: 600px;
            background: #6366f1;
            top: -200px; left: -100px;
            animation-delay: 0s;
        }}
        .bg-animated .orb:nth-child(2) {{
            width: 500px; height: 500px;
            background: #8b5cf6;
            bottom: -150px; right: -100px;
            animation-delay: -5s;
            animation-duration: 25s;
        }}
        .bg-animated .orb:nth-child(3) {{
            width: 350px; height: 350px;
            background: #a855f7;
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
        }}
        .btn-icon:hover {{
            background: var(--surface-hover);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
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

        /* ========== Counter Cards ========== */
        .counters-row {{
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .counter-card {{
            position: relative;
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 28px 48px;
            box-shadow: var(--shadow-xl);
            transition: all var(--transition);
            min-width: 160px;
        }}
        .counter-card:hover {{
            transform: translateY(-4px);
        }}
        .counter-number {{
            font-size: 3.5rem;
            font-weight: 900;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
        }}
        .counter-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 600;
            margin-top: 4px;
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
        }}
        .tab-btn:hover {{
            background: var(--bg);
            color: var(--text);
        }}
        .tab-btn.active {{
            background: var(--gradient-1);
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
        }}
        .tab-count {{
            font-size: 0.75rem;
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 50px;
        }}
        .tab-dot {{
            width: 8px; height: 8px;
            border-radius: 50%;
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
        .server-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 24px;
            transition: all var(--transition);
            position: relative;
            overflow: hidden;
        }}
        .server-card:hover {{
            box-shadow: var(--shadow-xl);
            transform: translateY(-4px);
            border-color: var(--primary);
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
        .server-flag {{ font-size: 2rem; line-height: 1; }}
        .server-proto-badge {{
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 700;
            color: white;
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
        .status-alive {{ background: var(--success); }}
        .status-dead {{ background: var(--danger); }}
        .server-url-box {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 14px 16px;
            margin-bottom: 16px;
            font-family: monospace;
            font-size: 0.78rem;
            color: var(--text-secondary);
            direction: ltr;
            text-align: left;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
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
            display: none;
            justify-content: center;
            border: 2px dashed var(--border);
        }}

        /* Toast */
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

        /* Stats Page */
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

        @media (max-width: 768px) {{
            .navbar-inner {{ flex-wrap:wrap; justify-content:center; gap:12px; padding:12px 16px; }}
            .hero-title {{ font-size:2rem; }}
            .counter-number {{ font-size:2.5rem; }}
            .counter-card {{ padding:20px 32px; min-width:120px; }}
            .servers-grid {{ grid-template-columns:1fr; }}
            .tab-btn {{ padding:10px 16px; font-size:0.8rem; }}
        }}
    </style>
</head>
<body>

    <div class="bg-animated">
        <div class="orb"></div><div class="orb"></div><div class="orb"></div>
    </div>

    <!-- شريط التنقل -->
    <nav class="navbar">
        <div class="navbar-inner">
            <div class="navbar-brand">✦ DOKA PRO</div>
            <div class="navbar-stats">
                <div class="pulse-dot"></div>
                <span>🟢 {sum(1 for s in all_servers if s['alive'])}/{total} مباشر</span>
                <span style="color:var(--text-secondary)">•</span>
                <span>{now}</span>
            </div>
            <div class="navbar-actions">
                <button class="btn-icon" id="dark-toggle" title="الوضع الليلي">
                    <i class="fas fa-moon"></i>
                </button>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div class="hero-badge">
            <i class="fas fa-shield-check"></i>
            <span>v2nodes + Exclave • تحديث تلقائي كل 3 ساعات</span>
        </div>
        <h1 class="hero-title">
            <span class="gradient-text">حرية</span> التصفح<br>بلا حدود
        </h1>
        <p class="hero-subtitle">سيرفرات V2Ray و Exclave VPN محدثة تلقائياً • اختر بروتوكولك المفضل وانطلق</p>
        <div class="counters-row">
            <div class="counter-card">
                <div class="counter-number">{total}</div>
                <div class="counter-label">🔰 إجمالي السيرفرات</div>
            </div>
            <div class="counter-card">
                <div class="counter-number" style="background:var(--gradient-2); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">{total_v2nodes}</div>
                <div class="counter-label">📡 V2Ray عام</div>
            </div>
            <div class="counter-card">
                <div class="counter-number" style="background:var(--gradient-exclave); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">{total_exclave}</div>
                <div class="counter-label">⬡ Exclave حصري</div>
            </div>
        </div>
    </section>

    <!-- فلترة -->
    <section class="filter-section">
        <div class="filter-tabs">
            <button class="tab-btn active" data-filter="all"><i class="fas fa-globe"></i> الكل <span class="tab-count">{total}</span></button>
            <button class="tab-btn" data-filter="vmess"><span class="tab-dot" style="background:#8b5cf6"></span> VMess <span class="tab-count">{counts.get('vmess', 0)}</span></button>
            <button class="tab-btn" data-filter="vless"><span class="tab-dot" style="background:#06b6d4"></span> VLess <span class="tab-count">{counts.get('vless', 0)}</span></button>
            <button class="tab-btn" data-filter="trojan"><span class="tab-dot" style="background:#f59e0b"></span> Trojan <span class="tab-count">{counts.get('trojan', 0)}</span></button>
            <button class="tab-btn" data-filter="ss"><span class="tab-dot" style="background:#10b981"></span> SS <span class="tab-count">{counts.get('ss', 0)}</span></button>
            <button class="tab-btn" data-filter="v2nodes">📡 v2nodes <span class="tab-count">{total_v2nodes}</span></button>
            <button class="tab-btn" data-filter="exclave">⬡ Exclave <span class="tab-count">{total_exclave}</span></button>
        </div>
    </section>

    <!-- السيرفرات -->
    <section class="servers-section">
        <div class="servers-grid" id="servers-grid"></div>
        <div id="no-servers" style="display:none; text-align:center; padding:60px; color:var(--text-secondary);">
            <i class="fas fa-inbox" style="font-size:3rem; display:block; margin-bottom:16px; opacity:0.3;"></i>
            لا توجد سيرفرات متاحة
        </div>
    </section>

    <!-- Footer -->
    <footer style="position:relative; z-index:1; text-align:center; padding:40px 24px; color:var(--text-secondary);">
        <p>© 2026 <strong>DOKA PRO</strong> • جميع الحقوق محفوظة</p>
        <button id="show-stats-btn" style="background:none; border:none; color:var(--primary); cursor:pointer; font-family:'Cairo',sans-serif; font-weight:600; text-decoration:underline;">📊 الإحصائيات</button>
    </footer>

    <!-- الإحصائيات -->
    <section class="stats-page" id="stats-page" style="display:none;">
        <div class="stats-card">
            <h2 style="font-size:2rem; margin-bottom:8px;">📊 لوحة الإحصائيات</h2>
            <p style="color:var(--text-secondary); margin-bottom:32px;">آخر تحديث: <span id="stats-last-update"></span></p>
            <canvas id="stats-chart" style="max-height:400px;"></canvas>
            <button onclick="location.reload()" style="margin-top:32px; padding:14px 40px; border-radius:50px; border:none; background:var(--gradient-1); color:white; font-family:'Cairo',sans-serif; font-weight:700; cursor:pointer;">⬅️ عودة</button>
        </div>
    </section>

    <!-- Toast -->
    <div class="toast" id="toast"><i class="fas fa-check-circle" style="color:#10b981;"></i> <span>تم النسخ!</span></div>

    <script>
        const serversData = {servers_json};
        const PROTOCOL_COLORS = {json.dumps(PROTOCOL_COLORS)};
        const PROTOCOL_ICONS = {json.dumps(PROTOCOL_ICONS)};
        let currentFilter = 'all';
        let chartInstance = null;

        // Dark Mode
        const darkToggle = document.getElementById('dark-toggle');
        darkToggle.addEventListener('click', () => {{
            document.body.classList.toggle('dark');
            darkToggle.querySelector('i').className = document.body.classList.contains('dark') ? 'fas fa-sun' : 'fas fa-moon';
            localStorage.setItem('doka-dark', document.body.classList.contains('dark') ? 'true' : 'false');
        }});
        if (localStorage.getItem('doka-dark') === 'true') {{
            document.body.classList.add('dark');
            darkToggle.querySelector('i').className = 'fas fa-sun';
        }}

        // عرض البطاقات
        function renderCards(filter) {{
            const grid = document.getElementById('servers-grid');
            const noMsg = document.getElementById('no-servers');
            let filtered = filter === 'all' ? serversData : serversData.filter(s => {{
                if (filter === 'v2nodes' || filter === 'exclave') return s.source === filter;
                return s.proto.toLowerCase() === filter;
            }});
            if (filtered.length === 0) {{ grid.innerHTML = ''; noMsg.style.display = 'block'; return; }}
            noMsg.style.display = 'none';
            let html = '';
            filtered.forEach((s, i) => {{
                const short = s.url.length > 65 ? s.url.substring(0, 63)+'...' : s.url;
                const protoColor = PROTOCOL_COLORS[s.proto.toLowerCase()] || '#6366f1';
                const protoIcon = PROTOCOL_ICONS[s.proto.toLowerCase()] || 'fa-cube';
                const alive = s.alive;
                const pingDisplay = alive ? s.ping+'ms' : 'ميت';
                const statusClass = alive ? 'status-alive' : 'status-dead';
                const statusColor = alive ? 'var(--success)' : 'var(--danger)';
                html += `
                <div class="server-card">
                    <div class="server-card-header">
                        <div class="server-info">
                            <span class="server-flag">${{s.country}}</span>
                            <span class="server-proto-badge" style="background:${{protoColor}}"><i class="fas ${{protoIcon}}"></i> ${{s.proto}}</span>
                            <span class="server-status" style="color:${{statusColor}}"><span class="status-dot ${{statusClass}}"></span> ${{alive?'حي':'ميت'}}</span>
                            <span style="font-size:0.7rem; color:${{s.source==='exclave'?'#a855f7':'var(--text-secondary)'}};">${{s.source==='exclave'?'⬡':''}}</span>
                        </div>
                        <span style="font-size:0.8rem; color:var(--text-secondary);">${{pingDisplay}}</span>
                    </div>
                    <div class="server-url-box">${{short}}</div>
                    <div class="server-actions">
                        <button class="btn-copy" onclick="copyText('${{s.url.replace(/'/g, "\\'")}}')" style="background:${{protoColor}}"><i class="far fa-copy"></i> نسخ</button>
                        <button class="btn-qr" onclick="toggleQR('q${{i}}','${{s.url.replace(/'/g, "\\'")}}')"><i class="fas fa-qrcode"></i></button>
                    </div>
                    <div class="qr-container" id="q${{i}}"></div>
                </div>`;
            }});
            grid.innerHTML = html;
        }}

        window.copyText = t => {{ navigator.clipboard.writeText(t).then(()=>{{const toast=document.getElementById('toast');toast.classList.add('show');clearTimeout(toast._t);toast._t=setTimeout(()=>toast.classList.remove('show'),2500);}}).catch(()=>{{const ta=document.createElement('textarea');ta.value=t;ta.style.cssText='position:fixed;opacity:0;';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);const toast=document.getElementById('toast');toast.classList.add('show');clearTimeout(toast._t);toast._t=setTimeout(()=>toast.classList.remove('show'),2500);}}); }};
        window.toggleQR = (id, link) => {{ const el = document.getElementById(id); if (el.style.display !== 'flex') {{ if (!el.innerHTML) new QRCode(el, {{text:link, width:180, height:180, colorDark:'#1e293b', colorLight:'#ffffff'}}); el.style.display = 'flex'; el.scrollIntoView({{behavior:'smooth',block:'nearest'}}); }} else {{ el.style.display = 'none'; }} }};

        document.querySelectorAll('.tab-btn').forEach(btn => btn.addEventListener('click', () => {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderCards(currentFilter);
        }}));

        document.getElementById('show-stats-btn').addEventListener('click', async () => {{
            document.querySelector('.navbar').style.display='none';
            document.querySelector('.hero').style.display='none';
            document.querySelector('.filter-section').style.display='none';
            document.querySelector('.servers-section').style.display='none';
            document.querySelector('footer').style.display='none';
            document.getElementById('stats-page').style.display='block';
            try {{
                const res = await fetch('stats.json');
                const stats = await res.json();
                document.getElementById('stats-last-update').innerText = new Date(stats.last_updated).toLocaleString('ar-SA');
                const ctx = document.getElementById('stats-chart').getContext('2d');
                if(chartInstance) chartInstance.destroy();
                const labels = Object.keys(stats.by_protocol).map(p=>p.toUpperCase());
                chartInstance = new Chart(ctx, {{
                    type:'doughnut',
                    data:{{ labels, datasets:[{{ data:Object.values(stats.by_protocol), backgroundColor:labels.map(l=>PROTOCOL_COLORS[l.toLowerCase()]||'#6366f1'), borderColor:document.body.classList.contains('dark')?'#1a2332':'#fff', borderWidth:4 }}] }},
                    options:{{ responsive:true, plugins:{{ legend:{{ position:'bottom', labels:{{ padding:20, font:{{family:'Cairo',size:14}} }} }} }} }}
                }});
            }} catch(e) {{ console.error(e); }}
        }});

        renderCards('all');
        console.log('%c🚀 DOKA PRO %cUltimate %cReady', 'color:#6366f1;font-size:2rem;font-weight:900;', 'color:#a855f7;', 'color:#10b981;');
        console.log('%cTotal:%c {total} %cservers', 'color:#64748b;', 'color:#6366f1;font-weight:bold;', 'color:#64748b;');
    </script>
</body>
</html>"""


# ==================== الدالة الرئيسية ====================
def main() -> None:
    """تشغيل DOKA PRO Ultimate Edition."""
    print("🚀 DOKA PRO - Ultimate Edition 2025")
    print("=" * 50)

    # جلب البيانات
    v2nodes_html = fetch_telegram_page(V2NODES_URL, "v2nodes")
    exclave_html = fetch_telegram_page(EXCLAVE_URL, "Exclave VPN")

    # استخراج الروابط
    v2nodes_links = extract_v2ray_links(v2nodes_html) if v2nodes_html else []
    exclave_links = extract_exclave_links(exclave_html) if exclave_html else []
    print(f"📊 v2nodes: {len(v2nodes_links)} | Exclave: {len(exclave_links)}")

    # بناء قائمة السيرفرات
    all_servers = build_server_list(v2nodes_links, "v2nodes")
    all_servers += build_server_list(exclave_links, "exclave")

    if not all_servers:
        print("⚠️ لا توجد سيرفرات!")
        return

    # قياس الـ ping الحقيقي
    all_servers = measure_all_pings(all_servers)

    # توليد HTML
    total = len(all_servers)
    alive_count = sum(1 for s in all_servers if s["alive"])
    html_output = generate_html(all_servers, total)

    OUTPUT_FILE.write_text(html_output, encoding="utf-8")
    print(f"\n🎉 تم! {total} سيرفر ({alive_count} حي)")
    print(f"   • v2nodes: {sum(1 for s in all_servers if s['source']=='v2nodes')}")
    print(f"   • Exclave: {sum(1 for s in all_servers if s['source']=='exclave')}")
    print(f"   • PWA: جاهز للتثبيت")
    print(f"   • Ping: حقيقي ✅")


if __name__ == "__main__":
    main()
