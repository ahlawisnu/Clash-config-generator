#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Account to Proxies Converter - Global Secure Edition (Fixed)
Author: GITHUB.COM/AHLAWISNU 
Version: 3.4.2
Description: Convert all protocols to Clash/Mihomo with Fixed GeoSite & Syntax
Fix: Fixed unterminated string literal error
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

# Global AdBlock Domains (No Region Specific)
ADBLOCK_DOMAINS = [
    'googleadservices.com', 'googlesyndication.com', 'google-analytics.com',
    'googletagmanager.com', 'googletagservices.com', 'doubleclick.net',
    'adsense.com', 'adsystem.com', 'advertising.com', 'adserver.com',
    'googleads.g.doubleclick.net', 'pagead2.googlesyndication.com',
    'ssl.google-analytics.com', 'analytics.google.com',
    'facebook.com/tr', 'connect.facebook.net', 'graph.facebook.com',
    'analytics.facebook.com', 'pixel.facebook.com', 'an.facebook.com',
    'analytics.twitter.com', 'ads-twitter.com', 'static.ads-twitter.com',
    'ads.linkedin.com', 'analytics.pointdrive.linkedin.com',
    'ads.pinterest.com', 'log.pinterest.com', 'analytics.pinterest.com',
    'ads.reddit.com', 'd.reddit.com', 'events.redditmedia.com',
    'amazon-adsystem.com', 'amazonadsi.com', 'assoc-amazon.com',
    'telemetry.microsoft.com', 'watson.telemetry.microsoft.com',
    'vortex.data.microsoft.com', 'settings-win.data.microsoft.com',
    'telemetry.mozilla.org', 'incoming.telemetry.mozilla.org',
    'data.mozilla.com', 'metrics.mozilla.com',
    'mixpanel.com', 'segment.io', 'segment.com', 'amplitude.com',
    'hotjar.com', 'crazyegg.com', 'optimizely.com', 'kissmetrics.com',
    'clicky.com', 'statcounter.com', 'scorecardresearch.com',
    'quantserve.com', 'outbrain.com', 'taboola.com', 'revcontent.com',
    'mgid.com', 'adroll.com', 'criteo.com', 'criteo.net',
    'rubiconproject.com',
    'crashlytics.com', 'firebase-settings.crashlytics.com',
    'app-measurement.com', 'firebaseinstallations.googleapis.com',
    'firebaseremoteconfig.googleapis.com', 'umeng.com', 'umengcloud.com',
    'popads.net', 'popcash.net', 'propellerads.com', 'adsterra.com',
    'ad-maven.com', 'onclickads.net', 'popmyads.com', 'popunder.net',
    'exoclick.com', 'adnium.com', 'juicyads.com',
    'coinhive.com', 'jsecoin.com', 'cryptaloot.pro', 'webmine.pro',
]

def print_banner():
    banner = f"""
{Colors.OKCYAN}
╔══════════════════════════════════════════════════════════════════╗
║   🔗 PROXIES CONVERTER v3.4.2 - GLOBAL SECURE (FIXED) 🔗         ║
║         Fake-IP | Anti-DNS Leak | Fixed GeoSite & Syntax         ║
║              Load Balance | Fallback | URL Test                  ║
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

def generate_global_config(proxies, enable_adblock=True, enable_fake_ip=True):
    """
    Konfigurasi global dengan GeoSite yang valid
    PERBAIKAN: Fixed syntax error pada DNS configuration
    """
    
    proxy_names = [p['name'] for p in proxies]
    
    if not proxy_names:
        proxy_names = ['DIRECT']
    
    # Proxy Groups
    proxy_groups = [
        {
            'name': 'Load-Balance',
            'type': 'load-balance',
            'strategy': 'consistent-hashing',
            'proxies': proxy_names,
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300
        },
        {
            'name': 'URL-Test',
            'type': 'url-test',
            'proxies': proxy_names,
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'tolerance': 50,
            'lazy': True
        },
        {
            'name': 'Fallback',
            'type': 'fallback',
            'proxies': proxy_names,
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'lazy': True
        },
        {
            'name': 'Manual-Select',
            'type': 'select',
            'proxies': ['URL-Test', 'Fallback', 'Load-Balance', 'DIRECT'] + proxy_names
        },
        {
            'name': 'AdBlock',
            'type': 'select',
            'proxies': ['REJECT', 'DIRECT']
        },
        {
            'name': 'Global',
            'type': 'select',
            'proxies': ['Manual-Select', 'URL-Test', 'Fallback', 'DIRECT'] + proxy_names
        },
        {
            'name': 'Final',
            'type': 'select',
            'proxies': ['Global', 'DIRECT']
        }
    ]
    
    # DNS Configuration dengan GeoSite yang VALID
    # PERBAIKAN: Fixed syntax error pada nameserver list
    dns_config = {
        'enable': True,
        'listen': '0.0.0.0:53',
        'ipv6': True,
        'enhanced-mode': 'fake-ip' if enable_fake_ip else 'redir-host',
        'fake-ip-range': '198.18.0.1/16',
        'fake-ip-filter': [
            '*.pool.ntp.org',
            'time.*.com',
            'time.*.google.com',
            'time.*.apple.com',
            'time.*.facebook.com',
            'time.windows.com',
            'msftconnecttest.com',
            'msftncsi.com',
            '*.msftconnecttest.com',
            'connectivitycheck.gstatic.com',
            'clients3.google.com',
            'captive.apple.com',
            'gsp1.apple.com',
            'www.msftconnecttest.com',
            'ipv6.msftconnecttest.com',
            '*.lan',
            '*.local',
            '*.localdomain',
            'localhost',
            'localhost.localdomain',
            '*.ip6-local',
            '*.ip6-loopback',
            'stun.*.*',
            'stun.*.*.*',
            '*.stun.*.*',
            '*.stun.*.*.*',
            '*.windowsupdate.com',
            '*.update.microsoft.com',
            '*.icloud.com',
            '*.icloud-content.com',
            '*.apple-cloudkit.com',
            '*.apple.com',
        ],
        
        # Global Popular DNS
        'default-nameserver': [
            '8.8.8.8',
            '8.8.4.4',
            '1.1.1.1',
            '1.0.0.1',
            '9.9.9.9',
            '149.112.112.112',
        ],
        
        # PERBAIKAN: Fixed syntax error - semua string harus ditutup dengan benar
        'nameserver': [
            'https://dns.google/dns-query',
            'https://cloudflare-dns.com/dns-query',
            'https://dns.quad9.net/dns-query',
            'tls://8.8.8.8:853',
            'tls://1.1.1.1:853',
            'tls://9.9.9.9:853',
            'https://doh.opendns.com/dns-query',
            'https://dns.adguard-dns.com/dns-query',
            'tls://dns.adguard-dns.com:853',
        ],
        
        'fallback': [
            'https://dns.google/dns-query',
            'https://cloudflare-dns.com/dns-query',
            'https://dns.quad9.net/dns-query',
            'tls://8.8.8.8:853',
            'tls://1.1.1.1:853',
        ],
        
        # PERBAIKAN: Hanya geosite yang VALID
        'fallback-filter': {
            'geoip': True,
            'geoip-code': 'ID',
            'geosite': ['gfw'],
            'ipcidr': ['240.0.0.0/4', '0.0.0.0/32', '127.0.0.0/8'],
        },
        
        # PERBAIKAN: DNS Policy dengan geosite yang valid
        'nameserver-policy': {
            'geosite:private': [
                'https://dns.google/dns-query',
                'https://cloudflare-dns.com/dns-query'
            ],
            'geosite:cn': [
                'https://dns.google/dns-query',
                'https://cloudflare-dns.com/dns-query'
            ],
        }
    }
    
    # Rules
    rules = []
    
    # 1. LAN/Direct
    rules.extend([
        'DOMAIN-SUFFIX,local,DIRECT',
        'DOMAIN-SUFFIX,localhost,DIRECT',
        'DOMAIN-SUFFIX,ip6-local,DIRECT',
        'DOMAIN-SUFFIX,ip6-loopback,DIRECT',
        'IP-CIDR,127.0.0.0/8,DIRECT',
        'IP-CIDR,172.16.0.0/12,DIRECT',
        'IP-CIDR,192.168.0.0/16,DIRECT',
        'IP-CIDR,10.0.0.0/8,DIRECT',
        'IP-CIDR,100.64.0.0/10,DIRECT',
        'IP-CIDR,224.0.0.0/4,DIRECT',
        'IP-CIDR,fe80::/10,DIRECT',
        'IP-CIDR,fc00::/7,DIRECT',
        'IP-CIDR,::1/128,DIRECT',
    ])
    
    # 2. AdBlock
    if enable_adblock:
        for domain in ADBLOCK_DOMAINS[:50]:
            if domain.startswith('*.'):
                rules.append(f'DOMAIN-SUFFIX,{domain[2:]},AdBlock')
            else:
                rules.append(f'DOMAIN-SUFFIX,{domain},AdBlock')
        
        rules.extend([
            'DOMAIN-KEYWORD,googleads,AdBlock',
            'DOMAIN-KEYWORD,googlesyndication,AdBlock',
            'DOMAIN-KEYWORD,google-analytics,AdBlock',
            'DOMAIN-KEYWORD,facebook-tr,AdBlock',
            'DOMAIN-KEYWORD,telemetry,AdBlock',
        ])
    
    # 3. Rule Providers
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
        'lancidr': {
            'type': 'http',
            'behavior': 'ipcidr',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt',
            'path': './ruleset/lancidr.yaml',
            'interval': 86400
        },
        'cncidr': {
            'type': 'http',
            'behavior': 'ipcidr',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt',
            'path': './ruleset/cncidr.yaml',
            'interval': 86400
        },
        'applications': {
            'type': 'http',
            'behavior': 'classical',
            'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt',
            'path': './ruleset/applications.yaml',
            'interval': 86400
        }
    }
    
    # 4. Rule Provider Rules
    rules.extend([
        'RULE-SET,reject,AdBlock',
        'RULE-SET,private,DIRECT',
        'RULE-SET,direct,DIRECT',
        'RULE-SET,proxy,Global',
        'RULE-SET,gfw,Global',
        'RULE-SET,tld-not-cn,Global',
        'RULE-SET,lancidr,DIRECT,no-resolve',
        'RULE-SET,cncidr,Global,no-resolve',
        'RULE-SET,applications,DIRECT',
    ])
    
    # 5. GeoIP (hanya PRIVATE)
    rules.extend([
        'GEOIP,PRIVATE,DIRECT,no-resolve',
    ])
    
    # 6. Final Match
    rules.append('MATCH,Global')
    
    # Build config
    config = {
        'port': 7899,
        'mixed-port': 7890,
        'socks-port': 7891,
        'redir-port': 7892,
        'tproxy-port': 7893,
        'allow-lan': True,
        'bind-address': '*',
        'mode': 'rule',
        'log-level': 'info',
        'ipv6': True,
        'external-controller': '127.0.0.1:9090',
        'external-ui': 'ui',
        
        'profile': {
            'store-selected': True,
            'store-fake-ip': enable_fake_ip
        },
        
        'dns': dns_config,
        
        'sniffer': {
            'enable': True,
            'force-dns-mapping': True,
            'parse-pure-ip': True,
            'override-destination': False,
            'sniff': {
                'TLS': {'ports': [443, 8443]},
                'HTTP': {'ports': [80, 8080, 8880, 2052, 2082, 2086, 2095], 'override-destination': True},
                'QUIC': {'ports': [443, 8443]}
            }
        },
        
        'proxies': proxies,
        'proxy-groups': proxy_groups,
        'rule-providers': rule_providers,
        'rules': rules
    }
    
    return config

def save_config(proxies, filename=None, enable_adblock=True, enable_fake_ip=True):
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
        mode = "fakeip" if enable_fake_ip else "redir"
        filename = f"proxies_global_fixed_{mode}_{timestamp}.yaml"
    
    if not filename.endswith('.yaml'):
        filename += '.yaml'
    
    output_path = Path(filename)
    
    config = generate_global_config(proxies, enable_adblock, enable_fake_ip)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False, 
                 default_flow_style=False, indent=2)
    
    print(f"\n{Colors.OKGREEN}[+] Config saved: {output_path.absolute()}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Proxies: {len(proxies)}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Mode: {'Fake-IP (Anti DNS Leak)' if enable_fake_ip else 'Redir-Host'}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    AdBlock: {'ON' if enable_adblock else 'OFF'}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}    DNS: Google + Cloudflare + Quad9 (DoH/DoT){Colors.ENDC}")
    print(f"{Colors.OKCYAN}    GeoSite: Fixed (removed invalid lists){Colors.ENDC}")
    print(f"{Colors.OKCYAN}    Syntax: Fixed (no unterminated strings){Colors.ENDC}")
    
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
    
    fake_ip = input(f"{Colors.OKBLUE}Enable Fake-IP mode? (y/n) [y]: {Colors.ENDC}").strip().lower()
    enable_fake_ip = fake_ip != 'n'
    
    if enable_fake_ip:
        print(f"{Colors.OKGREEN}    ✓ Fake-IP: Anti DNS leak protection enabled{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}    ! Redir-Host mode (DNS may leak){Colors.ENDC}")
    
    adblock = input(f"{Colors.OKBLUE}Enable AdBlock? (y/n) [y]: {Colors.ENDC}").strip().lower()
    enable_adblock = adblock != 'n'
    
    filename = input(f"{Colors.OKBLUE}Output filename [auto]: {Colors.ENDC}").strip()
    if not filename:
        filename = None
    
    save_config(proxies, filename, enable_adblock, enable_fake_ip)

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
