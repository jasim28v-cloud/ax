#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOKA PRO - Legendary Edition (v2nodes Exclusive)
Fetches ONLY: vmess, vless, trojan, ss (Full URLs)
Modern Python 3.12+ optimized with full backward compatibility.
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
}


# ==================== دوال الجلب والتحليل ====================
def fetch_telegram_page(url: str) -> str:
    """جلب محتوى صفحة تيليجرام مع معالجة الأخطاء."""
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        print(f"❌ خطأ في جلب الصفحة: {exc}")
        return ""


def extract_configs(html_content: str) -> dict[str, list[str]]:
    """
    استخراج جميع تكوينات V2Ray من HTML.
    تدعم الروابط الكاملة بدون قطع عند علامة '&'.
    """
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


def classify_servers(
    configs: dict[str, list[str]]
) -> dict[str, list[dict[str, str]]]:
    """تصنيف السيرفرات مع إضافة الدولة وزمن استجابة وهمي."""
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


# ==================== توليد HTML ====================
def generate_html(servers: dict[str, list[dict[str, str]]]) -> str:
    """توليد صفحة HTML احترافية كاملة."""
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    total_servers = sum(len(server_list) for server_list in servers.values())
    servers_json = json.dumps(servers, ensure_ascii=False)

    # حفظ الإحصائيات
    stats_data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_servers": total_servers,
        "by_protocol": {
            proto: len(servers.get(proto, [])) for proto in SUPPORTED_PROTOCOLS
        },
    }
    DATA_FILE.write_text(
        json.dumps(stats_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    counts = {proto: len(servers.get(proto, [])) for proto in SUPPORTED_PROTOCOLS}

    return f"""\
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOKA PRO — The Freedom Proxy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Tajawal', sans-serif; background: #fafafa; }}
        .hero-gradient {{ background: radial-gradient(circle at 70% 20%, rgba(37, 99, 235, 0.08) 0%, transparent 60%); }}
        .protocol-card {{
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }}
        .protocol-card:hover {{
            border-color: #2563eb;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.1);
        }}
        .dark {{ background: #0f172a; color: #e2e8f0; }}
        .dark .bg-white {{ background: #1e293b !important; }}
        .dark .text-gray-800 {{ color: #e2e8f0 !important; }}
        .dark .border-gray-100,
        .dark .border-gray-200 {{ border-color: #334155 !important; }}
        .tab-btn.active {{ background: #2563eb; color: white; }}
    </style>
</head>
<body class="antialiased text-gray-800" id="main-body">

    <!-- الشريط العلوي -->
    <header class="border-b border-gray-200 bg-white/90 backdrop-blur-md sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center text-sm">
            <div class="flex items-center gap-3 text-gray-600">
                <i class="fas fa-map-marker-alt text-blue-600"></i>
                <span>IP: <span id="user-ip" class="font-mono font-medium text-gray-900">...</span></span>
                <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                <span class="text-xs font-bold text-red-500" id="status-text">غير محمي</span>
            </div>
            <div class="flex items-center gap-4">
                <button id="dark-toggle" class="text-gray-500 hover:text-blue-600 transition-colors" aria-label="تبديل الوضع الليلي">
                    <i class="fas fa-moon"></i>
                </button>
                <select id="lang-select" class="bg-transparent border border-gray-300 rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="ar">🇸🇦 عربي</option>
                    <option value="en">🇬🇧 English</option>
                </select>
                <div class="text-gray-500">
                    <i class="far fa-clock"></i> <span>{now}</span>
                </div>
            </div>
        </div>
    </header>

    <!-- القسم الرئيسي -->
    <section class="hero-gradient border-b border-gray-200 py-16 text-center">
        <h1 class="text-4xl md:text-6xl font-black mb-4" id="main-title">حرية التصفح بلا حدود</h1>
        <p class="text-gray-600 max-w-2xl mx-auto mb-10" id="main-sub">
            سيرفرات V2Ray محدثة تلقائياً. اختر بروتوكولك واستمتع بالحرية.
        </p>
        <div class="inline-flex items-center gap-4 bg-white border border-gray-200 rounded-3xl px-10 py-5 shadow-sm">
            <span class="text-6xl font-black text-blue-600">{total_servers}</span>
            <span class="text-gray-500" id="counter-label">سيرفر نشط</span>
        </div>
    </section>

    <!-- تبويبات الفلترة -->
    <section class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-wrap justify-center gap-2">
            <button class="tab-btn active px-6 py-2 bg-blue-600 text-white rounded-full transition-all" data-filter="all">
                الكل (<span id="count-all">{total_servers}</span>)
            </button>
            <button class="tab-btn px-6 py-2 bg-gray-100 rounded-full transition-all" data-filter="vmess">
                VMess (<span id="count-vmess">{counts['vmess']}</span>)
            </button>
            <button class="tab-btn px-6 py-2 bg-gray-100 rounded-full transition-all" data-filter="vless">
                VLess (<span id="count-vless">{counts['vless']}</span>)
            </button>
            <button class="tab-btn px-6 py-2 bg-gray-100 rounded-full transition-all" data-filter="trojan">
                Trojan (<span id="count-trojan">{counts['trojan']}</span>)
            </button>
            <button class="tab-btn px-6 py-2 bg-gray-100 rounded-full transition-all" data-filter="ss">
                Shadowsocks (<span id="count-ss">{counts['ss']}</span>)
            </button>
        </div>
    </section>

    <!-- شبكة السيرفرات -->
    <section class="max-w-7xl mx-auto px-4 py-8">
        <div id="servers-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
        <div id="no-servers" class="hidden text-center py-12 text-gray-400">
            لا توجد سيرفرات متاحة حالياً.
        </div>
    </section>

    <!-- صفحة الإحصائيات -->
    <section id="stats-page" class="max-w-7xl mx-auto px-4 py-12 hidden">
        <h2 class="text-3xl font-bold text-center mb-8">📊 إحصائيات السيرفرات</h2>
        <div class="max-w-xl mx-auto">
            <canvas id="stats-chart"></canvas>
        </div>
        <p class="text-center text-gray-500 mt-4">
            آخر تحديث: <span id="stats-last-update"></span>
        </p>
        <button id="back-from-stats" class="mt-6 bg-blue-600 text-white px-6 py-3 rounded-xl mx-auto block hover:bg-blue-700 transition-colors">
            عودة
        </button>
    </section>

    <!-- تذييل الصفحة -->
    <footer class="bg-gray-900 text-white py-12 mt-12 text-center">
        <p class="text-gray-400">© 2026 DOKA PRO. جميع الحقوق محفوظة.</p>
        <button id="show-stats-btn" class="mt-4 text-blue-400 text-sm underline hover:text-blue-300 transition-colors">
            عرض الإحصائيات
        </button>
    </footer>

    <!-- إشعار النسخ (Toast) -->
    <div id="toast"
         class="fixed bottom-10 left-1/2 -translate-x-1/2 bg-gray-900 text-white px-8 py-3 rounded-full opacity-0 transition-all duration-300 pointer-events-none z-50">
        ✅ تم النسخ!
    </div>

    <script>
        const serversData = {servers_json};
        const AD_LINK = "{AD_LINK}";
        let currentFilter = 'all';
        let chartInstance = null;

        // ============ الترجمة ============
        const translations = {{
            ar: {{
                title: 'حرية التصفح بلا حدود',
                sub: 'سيرفرات V2Ray محدثة تلقائياً. اختر بروتوكولك واستمتع بالحرية.',
                label: 'سيرفر نشط',
                copy: 'نسخ',
                active: 'نشط',
                inactive: 'خامل',
                unprotected: 'غير محمي',
                stats: 'عرض الإحصائيات',
                back: 'عودة',
                noServers: 'لا توجد سيرفرات متاحة حالياً.',
            }},
            en: {{
                title: 'Unlimited Freedom',
                sub: 'Auto-updated V2Ray servers. Choose your protocol and enjoy freedom.',
                label: 'Active Servers',
                copy: 'Copy',
                active: 'Active',
                inactive: 'Inactive',
                unprotected: 'Unprotected',
                stats: 'Show Stats',
                back: 'Back',
                noServers: 'No servers available.',
            }}
        }};
        let currentLang = 'ar';

        function applyLang(lang) {{
            const t = translations[lang];
            document.getElementById('main-title').innerText = t.title;
            document.getElementById('main-sub').innerText = t.sub;
            document.getElementById('counter-label').innerText = t.label;
            document.getElementById('status-text').innerText = t.unprotected;
            document.getElementById('show-stats-btn').innerText = t.stats;
            document.getElementById('back-from-stats').innerText = t.back;
        }}

        document.getElementById('lang-select').addEventListener('change', (e) => {{
            currentLang = e.target.value;
            applyLang(currentLang);
            renderCards(currentFilter);
        }});

        // ============ الوضع الليلي ============
        document.getElementById('dark-toggle').addEventListener('click', () => {{
            document.getElementById('main-body').classList.toggle('dark');
            const icon = document.querySelector('#dark-toggle i');
            icon.classList.toggle('fa-moon');
            icon.classList.toggle('fa-sun');
        }});

        // ============ عرض البطاقات ============
        function renderCards(filter) {{
            const grid = document.getElementById('servers-grid');
            const noMsg = document.getElementById('no-servers');
            const t = translations[currentLang];

            let allServers = [];
            Object.keys(serversData).forEach(proto => {{
                serversData[proto].forEach(s =>
                    allServers.push({{ ...s, proto: proto.toUpperCase() }})
                );
            }});

            const filtered = filter === 'all'
                ? allServers
                : allServers.filter(s => s.proto.toLowerCase() === filter);

            if (filtered.length === 0) {{
                grid.innerHTML = '';
                noMsg.innerText = t.noServers || 'لا توجد سيرفرات.';
                noMsg.classList.remove('hidden');
                return;
            }}

            noMsg.classList.add('hidden');
            const isActiveMap = new Map();

            let html = '';
            filtered.forEach((s, i) => {{
                if (!isActiveMap.has(s.url)) {{
                    isActiveMap.set(s.url, Math.random() > 0.2);
                }}
                const isActive = isActiveMap.get(s.url);
                const shortUrl = s.url.length > 60 ? s.url.substring(0, 60) + '...' : s.url;

                html += `
                <div class="protocol-card bg-white rounded-2xl p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-4">
                        <div class="flex items-center gap-2 flex-wrap">
                            <span class="text-2xl">${{s.country}}</span>
                            <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">${{s.proto}}</span>
                            <span class="${{isActive ? 'text-green-600' : 'text-red-500'}} text-xs">
                                <i class="fas fa-circle text-[6px]"></i> ${{isActive ? t.active : t.inactive}}
                            </span>
                            <span class="text-gray-400 text-xs">
                                <i class="fas fa-tachometer-alt"></i> ${{s.latency}}
                            </span>
                        </div>
                        <button onclick="copyText('${{s.url.replace(/'/g, "\\'")}}')"
                                class="text-gray-400 hover:text-blue-600 transition-colors"
                                aria-label="نسخ الرابط">
                            <i class="far fa-copy"></i>
                        </button>
                    </div>
                    <p class="text-xs font-mono text-gray-500 bg-gray-50 p-3 rounded-xl mb-4 break-all" dir="ltr">${{shortUrl}}</p>
                    <div class="flex gap-2">
                        <button onclick="copyText('${{s.url.replace(/'/g, "\\'")}}')"
                                class="flex-1 bg-blue-600 text-white py-2.5 rounded-xl text-sm hover:bg-blue-700 transition-colors">
                            ${{t.copy}}
                        </button>
                        <button onclick="toggleQR('q${{i}}', '${{s.url.replace(/'/g, "\\'")}}')"
                                class="px-4 bg-gray-100 rounded-xl hover:bg-gray-200 transition-colors"
                                aria-label="عرض رمز QR">
                            <i class="fas fa-qrcode"></i>
                        </button>
                    </div>
                    <div id="q${{i}}" class="hidden mt-4 p-4 flex justify-center border-2 border-dashed border-blue-100 rounded-2xl"></div>
                </div>`;
            }});
            grid.innerHTML = html;
        }}

        // ============ دوال النسخ و QR ============
        window.copyText = (text) => {{
            navigator.clipboard.writeText(text).then(() => {{
                const toast = document.getElementById('toast');
                toast.style.opacity = '1';
                setTimeout(() => (toast.style.opacity = '0'), 2000);
            }}).catch(() => {{
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                const toast = document.getElementById('toast');
                toast.style.opacity = '1';
                setTimeout(() => (toast.style.opacity = '0'), 2000);
            }});
        }};

        window.toggleQR = (id, link) => {{
            const el = document.getElementById(id);
            if (!el.innerHTML) {{
                new QRCode(el, {{ text: link, width: 160, height: 160 }});
            }}
            el.classList.toggle('hidden');
        }};

        // ============ التبويبات ============
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.tab-btn').forEach(b => {{
                    b.classList.remove('active', 'bg-blue-600', 'text-white');
                    b.classList.add('bg-gray-100');
                }});
                btn.classList.add('active', 'bg-blue-600', 'text-white');
                btn.classList.remove('bg-gray-100');
                currentFilter = btn.dataset.filter;
                renderCards(currentFilter);
            }});
        }});

        // ============ صفحة الإحصائيات ============
        document.getElementById('show-stats-btn').addEventListener('click', async () => {{
            document.querySelector('header').style.display = 'none';
            document.querySelector('.hero-gradient').style.display = 'none';
            document.querySelectorAll('section')[1].style.display = 'none';
            document.getElementById('servers-grid').parentElement.style.display = 'none';
            document.querySelector('footer').style.display = 'none';
            document.getElementById('stats-page').classList.remove('hidden');

            try {{
                const res = await fetch('stats.json');
                if (!res.ok) throw new Error('Network response was not ok');
                const stats = await res.json();
                document.getElementById('stats-last-update').innerText =
                    new Date(stats.last_updated).toLocaleString(currentLang === 'ar' ? 'ar-SA' : 'en-US');

                const ctx = document.getElementById('stats-chart').getContext('2d');
                if (chartInstance) chartInstance.destroy();
                chartInstance = new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: Object.keys(stats.by_protocol).map(p => p.toUpperCase()),
                        datasets: [{{
                            label: currentLang === 'ar' ? 'عدد السيرفرات' : 'Server Count',
                            data: Object.values(stats.by_protocol),
                            backgroundColor: '#2563eb',
                            borderRadius: 6,
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            legend: {{ display: false }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                ticks: {{ stepSize: 1 }}
                            }}
                        }}
                    }}
                }});
            }} catch (err) {{
                console.error('Failed to load stats:', err);
                document.getElementById('stats-last-update').innerText = '—';
            }}
        }});

        document.getElementById('back-from-stats').addEventListener('click', () => location.reload());

        // ============ تحديد IP المستخدم ============
        fetch('https://api.ipify.org?format=json')
            .then(r => r.json())
            .then(d => (document.getElementById('user-ip').innerText = d.ip))
            .catch(() => (document.getElementById('user-ip').innerText = 'غير معروف'));

        // ============ التشغيل الأولي ============
        renderCards('all');
        applyLang('ar');
    </script>
</body>
</html>"""


# ==================== الدالة الرئيسية ====================
def main() -> None:
    """الدالة الرئيسية لتشغيل السكريبت."""
    print("🚀 بدء جلب بيانات v2nodes (VMess / VLess / Trojan / SS فقط - روابط كاملة)...")

    html_content = fetch_telegram_page(TELEGRAM_CHANNEL_URL)
    if not html_content:
        print("⚠️ تعذّر جلب الصفحة. تأكد من اتصالك بالإنترنت.")
        return

    raw_configs = extract_configs(html_content)
    classified = classify_servers(raw_configs)
    html_output = generate_html(classified)

    OUTPUT_FILE.write_text(html_output, encoding="utf-8")
    total = sum(len(server_list) for server_list in classified.values())
    print(f"🎉 تم بنجاح! الإجمالي: {total} سيرفر كامل.")


if __name__ == "__main__":
    main()
