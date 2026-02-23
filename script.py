#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Account to Proxies Converter - Fixed Rules
Author: github.com/ahlawisnu
Version: 3.2.1
Description: Convert all protocols to Clash/Mihomo
"""

import os
import sys
import json
import base64
import urllib.parse
import urllib.request
import ssl
import random
import re
from datetime import datetime
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

# AdBlock Domain Lists
ADBLOCK_DOMAINS = [
    'googleadservices.com', 'googlesyndication.com', 'google-analytics.com',
    'googletagmanager.com', 'googletagservices.com', 'doubleclick.net',
    'adsense.com', 'adsystem.com', 'advertising.com', 'adserver.com',
    'adtechus.com', 'googleads.g.doubleclick.net', 'pagead2.googlesyndication.com',
    'facebook.com/tr', 'fbcdn.net/tr', 'connect.facebook.net',
    'graph.facebook.com', 'analytics.facebook.com',
    'amazon-adsystem.com', 'amazonadsi.com', 'assoc-amazon.com',
    'analytics.yahoo.com', 'ads.yahoo.com', 'gemini.yahoo.com',
    'scorecardresearch.com', 'quantserve.com', 'mixpanel.com',
    'segment.io', 'segment.com', 'amplitude.com', 'hotjar.com',
    'crazyegg.com', 'optimizely.com', 'kissmetrics.com',
    'clicky.com', 'statcounter.com', 'google-analytics.com',
    'ssl.google-analytics.com', 'analytics.google.com',
    'crashlytics.com', 'firebase-settings.crashlytics.com',
    'app-measurement.com', 'firebaseinstallations.googleapis.com',
    'firebaseremoteconfig.googleapis.com',
    'admarvel.com', 'admaster.com.cn', 'adsage.com', 'adsmogo.com',
    'adsrvmedia.net', 'adwords.com', 'domob.cn', 'duomeng.cn',
    'dwtrack.com', 'guanggao.com', 'lianmeng.com', 'omgmta.com',
    'omniture.com', 'openx.net', 'partnerad.l.google.com',
    'pingfore.com', 'supersonicads.com', 'uedas.com', 'umeng.com',
    'umengcloud.com', 'usage.net', 'wlmonitor.com', 'zjtoolbar.com',
    'popads.net', 'popcash.net', 'propellerads.com', 'adsterra.com',
    'ad-maven.com', 'onclickads.net', 'popmyads.com', 'popunder.net',
    'coinhive.com', 'jsecoin.com', 'cryptaloot.pro', 'webmine.pro',
    'exoclick.com', 'adnium.com', 'juicyads.com', 'ero-advertising.com',
]

ADBLOCK_PLUS_DOMAINS = [
    'pixel.facebook.com', 'an.facebook.com', 'analytics.twitter.com',
    'ads-twitter.com', 'static.ads-twitter.com', 'ads.linkedin.com',
    'analytics.pointdrive.linkedin.com', 'ads.pinterest.com',
    'log.pinterest.com', 'analytics.pinterest.com',
    'ads.reddit.com', 'd.reddit.com', 'events.redditmedia.com',
    'googlevideo.com/videoplayback*adformat=', 'youtube.com/api/stats/ads',
    'youtube.com/get_video_info*adformat=', 'youtube.com/pagead',
    'youtube.com/ptracking', 'youtube.com/api/stats/qoe?*adformat',
    'audio-fa.scdn.co/audio/ad', 'spclient.wg.spotify.com/ads',
    'googletagservices.com/tag/js/gpt.js', 'googleads.g.doubleclick.net',
    'outbrain.com', 'taboola.com', 'revcontent.com', 'mgid.com',
    'adroll.com', 'criteo.com', 'criteo.net', 'rubiconproject.com',
    'ip2location.com', 'maxmind.com', 'ipinfo.io', 'ip-api.com',
    'telemetry.microsoft.com', 'watson.telemetry.microsoft.com',
    'vortex.data.microsoft.com', 'settings-win.data.microsoft.com',
    'telemetry.mozilla.org', 'incoming.telemetry.mozilla.org',
    'data.mozilla.com', 'metrics.mozilla.com',
]

def print_banner():
    banner = f"""
{Colors.OKCYAN}
╔══════════════════════════════════════════════════════════════════╗
║   🔗 MULTI-ACCOUNT TO PROXIES CONVERTER v3.2.1 - FIXED 🔗         ║
║         AdBlock | Load Balance | Fallback | URL Test              ║
║          ＡＨＬＡ｜Ai Ilustrator HTTPS:AHLAWISNU.GITHUB.IO                    ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """
    print(banner)

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

def create_ssl_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def fetch_url(url, max_retries=3):
    ssl_context = create_ssl_context()
    
    for attempt in range(max_retries):
        try:
            headers = get_random_headers()
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                content = response.read()
                
                try:
                    decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                    links = [line.strip() for line in decoded.split('\n') if line.strip()]
                except:
                    links = [line.strip() for line in content.decode('utf-8', errors='ignore').split('\n') if line.strip()]
                
                return links
                
        except Exception as e:
            if attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)
            else:
                print(f"{Colors.FAIL}[!] Failed to fetch: {e}{Colors.ENDC}")
                return []
    
    return []

def parse_vmess(link):
    try:
        if not link.startswith('vmess://'):
            return None
        
        b64_data = link[8:]
        padding = 4 - len(b64_data) % 4
        if padding != 4:
            b64_data += '=' * padding
        
        json_str = base64.b64decode(b64_data).decode('utf-8')
        data = json.loads(json_str)
        
        proxy = {
            'name': data.get('ps', 'Vmess Node'),
            'type': 'vmess',
            'server': data.get('add', ''),
            'port': int(data.get('port', 443)),
            'uuid': data.get('id', ''),
            'alterId': int(data.get('aid', 0)),
            'cipher': data.get('scy', 'auto'),
            'tls': data.get('tls', '') == 'tls',
            'skip-cert-verify': True,
            'network': data.get('net', 'tcp'),
            'udp': True
        }
        
        if data.get('net') == 'ws':
            proxy['ws-opts'] = {
                'path': data.get('path', '/'),
                'headers': {'Host': data.get('host', '')} if data.get('host') else {}
            }
        
        if data.get('net') == 'grpc':
            proxy['grpc-opts'] = {'grpc-service-name': data.get('path', '')}
        
        if data.get('net') == 'h2':
            proxy['h2-opts'] = {
                'host': [data.get('host', '')],
                'path': data.get('path', '/')
            }
        
        return proxy
        
    except Exception as e:
        return None

def parse_vless(link):
    try:
        if not link.startswith('vless://'):
            return None
        
        parsed = urllib.parse.urlparse(link)
        params = urllib.parse.parse_qs(parsed.query)
        
        uuid = parsed.username
        server = parsed.hostname
        port = parsed.port or 443
        
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'Vless Node'
        
        proxy = {
            'name': remark,
            'type': 'vless',
            'server': server,
            'port': port,
            'uuid': uuid,
            'tls': False,
            'skip-cert-verify': True,
            'network': 'tcp',
            'udp': True
        }
        
        security = params.get('security', ['none'])[0]
        if security in ['tls', 'xtls', 'reality']:
            proxy['tls'] = True
            proxy['servername'] = params.get('sni', [''])[0]
        
        net_type = params.get('type', ['tcp'])[0]
        proxy['network'] = net_type
        
        if net_type == 'ws':
            proxy['ws-opts'] = {
                'path': params.get('path', ['/'])[0],
                'headers': {'Host': params.get('host', [''])[0]}
            }
        
        if net_type == 'grpc':
            proxy['grpc-opts'] = {'grpc-service-name': params.get('serviceName', [''])[0]}
        
        if security == 'reality':
            proxy['reality-opts'] = {
                'public-key': params.get('pbk', [''])[0],
                'short-id': params.get('sid', [''])[0]
            }
        
        if 'flow' in params:
            proxy['flow'] = params['flow'][0]
        
        return proxy
        
    except Exception as e:
        return None

def parse_trojan(link):
    try:
        if not link.startswith('trojan://'):
            return None
        
        parsed = urllib.parse.urlparse(link)
        params = urllib.parse.parse_qs(parsed.query)
        
        password = parsed.username
        server = parsed.hostname
        port = parsed.port or 443
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'Trojan Node'
        
        proxy = {
            'name': remark,
            'type': 'trojan',
            'server': server,
            'port': port,
            'password': password,
            'skip-cert-verify': True,
            'udp': True
        }
        
        if 'sni' in params:
            proxy['sni'] = params['sni'][0]
        
        net_type = params.get('type', ['tcp'])[0]
        
        if net_type == 'ws':
            proxy['network'] = 'ws'
            proxy['ws-opts'] = {
                'path': params.get('path', ['/'])[0],
                'headers': {'Host': params.get('host', [''])[0]}
            }
        
        if net_type == 'grpc':
            proxy['network'] = 'grpc'
            proxy['grpc-opts'] = {'grpc-service-name': params.get('serviceName', [''])[0]}
        
        return proxy
        
    except Exception as e:
        return None

def parse_ss(link):
    try:
        if not link.startswith('ss://'):
            return None
        
        parsed = urllib.parse.urlparse(link)
        
        if parsed.username:
            userinfo = parsed.username
            if '%' not in userinfo:
                try:
                    userinfo = base64.b64decode(userinfo + '==').decode('utf-8')
                except:
                    pass
            
            if ':' in userinfo:
                method, password = userinfo.split(':', 1)
            else:
                method = 'aes-256-gcm'
                password = userinfo
        else:
            method = 'aes-256-gcm'
            password = ''
        
        params = urllib.parse.parse_qs(parsed.query)
        plugin = params.get('plugin', [''])[0]
        
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'SS Node'
        
        proxy = {
            'name': remark,
            'type': 'ss',
            'server': parsed.hostname,
            'port': parsed.port or 8388,
            'password': password,
            'cipher': method,
            'udp': True
        }
        
        if plugin:
            if 'obfs' in plugin:
                parts = plugin.split(';')
                plugin_opts = {}
                for part in parts[1:]:
                    if '=' in part:
                        k, v = part.split('=', 1)
                        plugin_opts[k] = v
                
                proxy['plugin'] = 'obfs'
                proxy['plugin-opts'] = {
                    'mode': plugin_opts.get('obfs', 'http'),
                    'host': plugin_opts.get('obfs-host', '')
                }
            elif 'v2ray' in plugin:
                proxy['plugin'] = 'v2ray-plugin'
                proxy['plugin-opts'] = {
                    'mode': 'websocket',
                    'tls': 'tls' in plugin,
                    'skip-cert-verify': True
                }
        
        return proxy
        
    except Exception as e:
        return None

def parse_ssr(link):
    try:
        if not link.startswith('ssr://'):
            return None
        
        b64_data = link[6:]
        padding = 4 - len(b64_data) % 4
        if padding != 4:
            b64_data += '=' * padding
        
        decoded = base64.b64decode(b64_data).decode('utf-8')
        
        if '/?' in decoded:
            main_part, params_part = decoded.split('/?', 1)
        else:
            main_part = decoded
            params_part = ''
        
        parts = main_part.split(':')
        if len(parts) < 6:
            return None
        
        server = parts[0]
        port = int(parts[1])
        protocol = parts[2]
        method = parts[3]
        obfs = parts[4]
        password_b64 = parts[5]
        
        password = base64.b64decode(password_b64 + '==').decode('utf-8')
        
        params = {}
        if params_part:
            params_str = base64.b64decode(params_part + '==').decode('utf-8')
            for param in params_str.split('&'):
                if '=' in param:
                    k, v = param.split('=', 1)
                    params[k] = v
        
        remark = base64.b64decode(params.get('remarks', '') + '==').decode('utf-8') if 'remarks' in params else 'SSR Node'
        
        proxy = {
            'name': remark + ' (SSR)',
            'type': 'ss',
            'server': server,
            'port': port,
            'password': password,
            'cipher': method,
            'udp': True
        }
        
        return proxy
        
    except Exception as e:
        return None

def parse_socks5(link):
    try:
        if not link.startswith('socks5://'):
            return None
        
        parsed = urllib.parse.urlparse(link)
        
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'Socks5 Node'
        
        proxy = {
            'name': remark,
            'type': 'socks5',
            'server': parsed.hostname,
            'port': parsed.port or 1080,
            'udp': True
        }
        
        if parsed.username:
            proxy['username'] = parsed.username
        if parsed.password:
            proxy['password'] = parsed.password
        
        return proxy
        
    except Exception as e:
        return None

def parse_http(link):
    try:
        if not link.startswith('http://') and not link.startswith('https://'):
            return None
        
        if not re.match(r'^https?://[^/]+:\d+', link):
            return None
        
        parsed = urllib.parse.urlparse(link)
        
        is_https = link.startswith('https://')
        
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'HTTP Node'
        
        proxy = {
            'name': remark,
            'type': 'http',
            'server': parsed.hostname,
            'port': parsed.port or (443 if is_https else 80)
        }
        
        if parsed.username:
            proxy['username'] = parsed.username
        if parsed.password:
            proxy['password'] = parsed.password
        if is_https:
            proxy['tls'] = True
            proxy['skip-cert-verify'] = True
        
        return proxy
        
    except Exception as e:
        return None

def parse_hysteria(link):
    try:
        if not link.startswith('hysteria://'):
            return None
        
        parsed = urllib.parse.urlparse(link)
        params = urllib.parse.parse_qs(parsed.query)
        
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'Hysteria Node'
        
        proxy = {
            'name': remark,
            'type': 'hysteria',
            'server': parsed.hostname,
            'port': parsed.port or 443,
            'auth': params.get('auth', [''])[0],
            'protocol': params.get('protocol', ['udp'])[0],
            'up': params.get('upmbps', ['10'])[0],
            'down': params.get('downmbps', ['50'])[0],
            'skip-cert-verify': True
        }
        
        if 'peer' in params or 'sni' in params:
            proxy['sni'] = params.get('peer', params.get('sni', ['']))[0]
        
        return proxy
        
    except Exception as e:
        return None

def parse_tuic(link):
    try:
        if not link.startswith('tuic://'):
            return None
        
        parsed = urllib.parse.urlparse(link)
        params = urllib.parse.parse_qs(parsed.query)
        
        uuid = parsed.username
        password = parsed.password
        remark = urllib.parse.unquote(parsed.fragment) if parsed.fragment else 'TUIC Node'
        
        proxy = {
            'name': remark,
            'type': 'tuic',
            'server': parsed.hostname,
            'port': parsed.port or 443,
            'uuid': uuid,
            'password': password,
            'congestion-controller': params.get('congestion_control', ['bbr'])[0],
            'udp-relay-mode': params.get('udp_relay_mode', ['native'])[0],
            'skip-cert-verify': True
        }
        
        if 'alpn' in params:
            proxy['alpn'] = params['alpn'][0].split(',')
        
        return proxy
        
    except Exception as e:
        return None

def convert_link_to_proxy(link):
    link = link.strip()
    if not link:
        return None
    
    parsers = [
        parse_vmess,
        parse_vless,
        parse_trojan,
        parse_ss,
        parse_ssr,
        parse_socks5,
        parse_http,
        parse_hysteria,
        parse_tuic,
    ]
    
    for parser in parsers:
        try:
            result = parser(link)
            if result:
                return result
        except:
            continue
    
    return None

def generate_advanced_config(proxies, enable_adblock=True, enable_adblock_plus=False):
    """
    PERBAIKAN UTAMA:
    - Nama proxy group konsisten antara definisi dan rules
    - Tidak ada spasi di nama group
    - Semua rule mereferensi group yang sudah didefinisikan
    """
    
    proxy_names = [p['name'] for p in proxies]
    
    if not proxy_names:
        proxy_names = ['DIRECT']
    
    # ============================================
    # PROXY GROUPS - DEFINISI
    # ============================================
    proxy_groups = [
        # 1. Load Balance (hanya proxy names)
        {
            'name': 'Load-Balance',
            'type': 'load-balance',
            'strategy': 'consistent-hashing',
            'proxies': proxy_names,
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300
        },
        
        # 2. URL Test
        {
            'name': 'URL-Test',
            'type': 'url-test',
            'proxies': proxy_names,
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'tolerance': 50,
            'lazy': True
        },
        
        # 3. Fallback
        {
            'name': 'Fallback',
            'type': 'fallback',
            'proxies': proxy_names,
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'lazy': True
        },
        
        # 4. Manual Select (bisa pilih semua group di atas)
        {
            'name': 'Manual-Select',
            'type': 'select',
            'proxies': ['URL-Test', 'Fallback', 'Load-Balance', 'DIRECT'] + proxy_names
        },
        
        # 5. AdBlock (REJECT atau DIRECT)
        {
            'name': 'AdBlock',
            'type': 'select',
            'proxies': ['REJECT', 'DIRECT']
        },
        
        # 6. AdBlock Plus
        {
            'name': 'AdBlock-Plus',
            'type': 'select',
            'proxies': ['REJECT', 'DIRECT']
        },
        
        # 7. Proxy (untuk RULE-SET proxy, gfw, tld-not-cn)
        {
            'name': 'Proxy',
            'type': 'select',
            'proxies': ['Manual-Select', 'URL-Test', 'Fallback', 'DIRECT'] + proxy_names
        },
        
        # 8. Domestic (untuk China/direct)
        {
            'name': 'Domestic',
            'type': 'select',
            'proxies': ['DIRECT', 'Manual-Select']
        },
        
        # 9. Final (catch-all)
        {
            'name': 'Final',
            'type': 'select',
            'proxies': ['Manual-Select', 'DIRECT']
        }
    ]
    
    # ============================================
    # RULES - YANG MEREFERENSI PROXY GROUPS DI ATAS
    # ============================================
    rules = []
    
    # 1. LAN/Direct rules
    rules.extend([
        'DOMAIN-SUFFIX,local,DIRECT',
        'DOMAIN-SUFFIX,localhost,DIRECT',
        'IP-CIDR,127.0.0.0/8,DIRECT',
        'IP-CIDR,172.16.0.0/12,DIRECT',
        'IP-CIDR,192.168.0.0/16,DIRECT',
        'IP-CIDR,10.0.0.0/8,DIRECT',
        'IP-CIDR,100.64.0.0/10,DIRECT',
        'IP-CIDR,224.0.0.0/4,DIRECT',
        'IP-CIDR,fe80::/10,DIRECT',
        'IP-CIDR,fc00::/7,DIRECT',
    ])
    
    # 2. AdBlock rules
    if enable_adblock:
        for domain in ADBLOCK_DOMAINS[:50]:  # Limit to 50 for performance
            if domain.startswith('*.'):
                rules.append(f'DOMAIN-SUFFIX,{domain[2:]},AdBlock')
            else:
                rules.append(f'DOMAIN-SUFFIX,{domain},AdBlock')
        
        rules.extend([
            'DOMAIN-KEYWORD,googleads,AdBlock',
            'DOMAIN-KEYWORD,googlesyndication,AdBlock',
            'DOMAIN-KEYWORD,google-analytics,AdBlock',
        ])
    
    # 3. AdBlock Plus rules
    if enable_adblock_plus:
        for domain in ADBLOCK_PLUS_DOMAINS[:30]:
            if domain.startswith('*.'):
                rules.append(f'DOMAIN-SUFFIX,{domain[2:]},AdBlock-Plus')
            else:
                rules.append(f'DOMAIN-SUFFIX,{domain},AdBlock-Plus')
    
    # 4. Rule Providers - PERBAIKAN NAMA GROUP
    rule_providers = {
        'reject': {
            'type': 'http',
            'behavior': 'domain',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt',
            'path': './ruleset/reject.yaml',
            'interval': 86400
        },
        'proxy': {
            'type': 'http',
            'behavior': 'domain',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt',
            'path': './ruleset/proxy.yaml',
            'interval': 86400
        },
        'direct': {
            'type': 'http',
            'behavior': 'domain',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt',
            'path': './ruleset/direct.yaml',
            'interval': 86400
        },
        'private': {
            'type': 'http',
            'behavior': 'domain',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt',
            'path': './ruleset/private.yaml',
            'interval': 86400
        },
        'gfw': {
            'type': 'http',
            'behavior': 'domain',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/gfw.txt',
            'path': './ruleset/gfw.yaml',
            'interval': 86400
        },
        'tld-not-cn': {
            'type': 'http',
            'behavior': 'domain',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt',
            'path': './ruleset/tld-not-cn.yaml',
            'interval': 86400
        },
        'cncidr': {
            'type': 'http',
            'behavior': 'ipcidr',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt',
            'path': './ruleset/cncidr.yaml',
            'interval': 86400
        },
        'lancidr': {
            'type': 'http',
            'behavior': 'ipcidr',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt',
            'path': './ruleset/lancidr.yaml',
            'interval': 86400
        }
    }
    
    # 5. Rule Provider Rules - PERBAIKAN: gunakan nama yang benar
    rules.extend([
        'RULE-SET,reject,AdBlock',           # AdBlock sudah didefinisikan
        'RULE-SET,private,DIRECT',           # DIRECT adalah built-in
        'RULE-SET,direct,Domestic',          # Domestic sudah didefinisikan
        'RULE-SET,proxy,Proxy',              # Proxy sudah didefinisikan
        'RULE-SET,gfw,Proxy',                # Proxy sudah didefinisikan
        'RULE-SET,tld-not-cn,Proxy',         # Proxy sudah didefinisikan
        'RULE-SET,cncidr,Domestic,no-resolve',
        'RULE-SET,lancidr,DIRECT,no-resolve',
    ])
    
    # 6. GeoIP
    rules.extend([
        'GEOIP,CN,Domestic',
        'GEOIP,PRIVATE,DIRECT,no-resolve',
    ])
    
    # 7. Final Match
    rules.append('MATCH,Final')
    
    # Build config
    config = {
        'port': 7890,
        'socks-port': 7891,
        'redir-port': 7892,
        'allow-lan': True,
        'bind-address': '*',
        'mode': 'rule',
        'log-level': 'info',
        'ipv6': True,
        'external-controller': '127.0.0.1:9090',
        'external-ui': './dashboard',
        
        'dns': {
            'enable': True,
            'listen': '0.0.0.0:53',
            'ipv6': True,
            'default-nameserver': ['223.5.5.5', '119.29.29.29'],
            'nameserver': [
                'https://doh.pub/dns-query',
                'https://dns.alidns.com/dns-query'
            ],
            'fallback': [
                'https://1.1.1.1/dns-query',
                'https://dns.google/dns-query'
            ],
            'fallback-filter': {
                'geoip': True,
                'geoip-code': 'CN',
                'ipcidr': ['240.0.0.0/4']
            }
        },
        
        'proxies': proxies,
        'proxy-groups': proxy_groups,
        'rule-providers': rule_providers,
        'rules': rules
    }
    
    return config

def save_config(proxies, filename=None, enable_adblock=True, enable_adblock_plus=False):
    try:
        import yaml
    except ImportError:
        print(f"{Colors.WARNING}[*] Installing PyYAML...{Colors.ENDC}")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyyaml'], 
                      capture_output=True)
        import yaml
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proxies_fixed_{timestamp}.yaml"
    
    if not filename.endswith('.yaml'):
        filename += '.yaml'
    
    output_path = Path(filename)
    
    config = generate_advanced_config(proxies, enable_adblock, enable_adblock_plus)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False, 
                 default_flow_style=False, indent=2)
    
    print(f"\n{Colors.OKGREEN}[+] Config saved: {output_path.absolute()}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Proxies: {len(proxies)}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    AdBlock: {'ON' if enable_adblock else 'OFF'}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    AdBlock Plus: {'ON' if enable_adblock_plus else 'OFF'}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Proxy Groups: 9 groups{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Status: FIXED - No name errors{Colors.ENDC}")
    
    return output_path

def process_links(links):
    proxies = []
    stats = {
        'vmess': 0, 'vless': 0, 'trojan': 0, 'ss': 0, 
        'ssr': 0, 'socks5': 0, 'http': 0, 'hysteria': 0,
        'tuic': 0, 'failed': 0
    }
    
    print(f"\n{Colors.OKBLUE}[*] Processing {len(links)} links...{Colors.ENDC}\n")
    
    for i, link in enumerate(links, 1):
        link = link.strip()
        if not link:
            continue
        
        proxy = convert_link_to_proxy(link)
        
        if proxy:
            original_name = proxy['name']
            counter = 1
            existing_names = [p['name'] for p in proxies]
            while proxy['name'] in existing_names:
                proxy['name'] = f"{original_name}_{counter}"
                counter += 1
            
            proxies.append(proxy)
            ptype = proxy['type']
            if ptype in stats:
                stats[ptype] += 1
            print(f"{Colors.OKGREEN}[{i}] ✓ {proxy['type'].upper()}: {proxy['name'][:50]}{Colors.ENDC}")
        else:
            stats['failed'] += 1
            print(f"{Colors.FAIL}[{i}] ✗ Failed: {link[:60]}...{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Conversion Stats:{Colors.ENDC}")
    for ptype, count in stats.items():
        if count > 0:
            print(f"  {Colors.OKCYAN}{ptype.upper()}: {count}{Colors.ENDC}")
    
    return proxies

def main_menu():
    while True:
        print_banner()
        print(f"""
{Colors.BOLD}MENU:{Colors.ENDC}
{Colors.OKCYAN}[1]{Colors.ENDC} Convert from Subscription URL
{Colors.OKCYAN}[2]{Colors.ENDC} Convert from File (txt)
{Colors.OKCYAN}[3]{Colors.ENDC} Paste Links Directly
{Colors.OKCYAN}[4]{Colors.ENDC} Convert Single Link (Test)
{Colors.OKCYAN}[0]{Colors.ENDC} Exit
        """)
        
        choice = input(f"{Colors.BOLD}Select: {Colors.ENDC}").strip()
        
        if choice == '1':
            menu_subscription_url()
        elif choice == '2':
            menu_file_input()
        elif choice == '3':
            menu_paste_links()
        elif choice == '4':
            menu_single_link()
        elif choice == '0':
            print(f"{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid choice{Colors.ENDC}")
        
        input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")

def menu_subscription_url():
    url = input(f"{Colors.OKBLUE}Subscription URL: {Colors.ENDC}").strip()
    if not url:
        return
    
    print(f"\n{Colors.OKBLUE}[*] Fetching subscription...{Colors.ENDC}")
    links = fetch_url(url)
    
    if not links:
        print(f"{Colors.FAIL}[!] No links found{Colors.ENDC}")
        return
    
    print(f"{Colors.OKGREEN}[+] Found {len(links)} links{Colors.ENDC}")
    
    proxies = process_links(links)
    
    if proxies:
        configure_and_save(proxies)

def menu_file_input():
    file_path = input(f"{Colors.OKBLUE}File path: {Colors.ENDC}").strip()
    
    if not Path(file_path).exists():
        print(f"{Colors.FAIL}[!] File not found{Colors.ENDC}")
        return
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    try:
        decoded = base64.b64decode(content).decode('utf-8')
        links = [line.strip() for line in decoded.split('\n') if line.strip()]
    except:
        links = [line.strip() for line in content.split('\n') if line.strip()]
    
    print(f"{Colors.OKGREEN}[+] Found {len(links)} lines{Colors.ENDC}")
    
    proxies = process_links(links)
    
    if proxies:
        configure_and_save(proxies)

def menu_paste_links():
    print(f"{Colors.OKBLUE}Paste links (one per line, empty line to finish):{Colors.ENDC}")
    
    links = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            links.append(line)
        except EOFError:
            break
    
    if not links:
        print(f"{Colors.FAIL}[!] No links provided{Colors.ENDC}")
        return
    
    proxies = process_links(links)
    
    if proxies:
        configure_and_save(proxies)

def configure_and_save(proxies):
    print(f"\n{Colors.BOLD}Configuration Options:{Colors.ENDC}")
    
    adblock = input(f"{Colors.OKBLUE}Enable AdBlock? (y/n) [y]: {Colors.ENDC}").strip().lower()
    enable_adblock = adblock != 'n'
    
    if enable_adblock:
        adblock_plus = input(f"{Colors.OKBLUE}Enable AdBlock Plus (strict)? (y/n) [n]: {Colors.ENDC}").strip().lower()
        enable_adblock_plus = adblock_plus == 'y'
    else:
        enable_adblock_plus = False
    
    filename = input(f"{Colors.OKBLUE}Output filename [auto]: {Colors.ENDC}").strip()
    if not filename:
        filename = None
    
    save_config(proxies, filename, enable_adblock, enable_adblock_plus)

def menu_single_link():
    link = input(f"{Colors.OKBLUE}Paste proxy link: {Colors.ENDC}").strip()
    
    proxy = convert_link_to_proxy(link)
    
    if proxy:
        print(f"\n{Colors.OKGREEN}[+] Converted:{Colors.ENDC}")
        print(f"{Colors.BOLD}Type:{Colors.ENDC} {proxy['type']}")
        print(f"{Colors.BOLD}Name:{Colors.ENDC} {proxy['name']}")
        print(f"\n{Colors.OKCYAN}YAML:{Colors.ENDC}")
        
        try:
            import yaml
            print(yaml.dump([proxy], allow_unicode=True, default_flow_style=False))
        except:
            print(str(proxy))
    else:
        print(f"{Colors.FAIL}[!] Failed to convert link{Colors.ENDC}")

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Interrupted{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
