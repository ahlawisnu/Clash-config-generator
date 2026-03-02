#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script Python untuk Termux - Generator Konfigurasi Clash/Mihomo
# Fitur: Full Config & Proxy Provider dengan semua jenis protocol

import os
import re
import json
import yaml
import base64
import urllib.parse
from urllib.parse import urlparse, parse_qs

class ClashConfigGenerator:
    def __init__(self):
        self.config_template = """proxy-providers:
  SERVER:
    type: file
    path: "./akun.yaml"
    health-check:
      enable: true
      url: http://www.gstatic.com/generate_204
      interval: 300

proxy-groups:
  - name: MANUAL
    type: select
    proxies:
      - BEST-PING
      - FALLBACK
      - LB
    use:
      - SERVER
    
  - name: UMUM
    type: select
    proxies:
      - MANUAL
      - BEST-PING
      - FALLBACK
      - LB
    use:
      - SERVER
    
  - name: FINAL
    type: select
    proxies:
      - UMUM
      - DIRECT
      
  - name: ADBLOCK+
    type: select
    proxies:
      - REJECT
      - FALLBACK

  - name: FALLBACK
    type: fallback
    use:
      - SERVER
    url: http://www.gstatic.com/generate_204
    interval: 300

  - name: BEST-PING
    type: url-test
    use:
      - SERVER
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 100

  - name: LB
    type: load-balance
    strategy: round-robin
    use:
      - SERVER
    url: http://www.gstatic.com/generate_204
    interval: 300
    
port: 7893
socks-port: 7891
redir-port: 7892
mixed-port: 7890
tproxy-port: 7895
ipv6: false
mode: rule
log-level: silent
allow-lan: true
external-controller: 0.0.0.0:9090
secret: ""
bind-address: "*"
unified-delay: true

profile:
  store-selected: true
  store-fake-ip: true

dns:
  enable: true
  ipv6: false
  use-host: true
  enhanced-mode: fake-ip
  listen: 0.0.0.0:7874
  nameserver:
    - 94.140.14.140
    - 94.140.14.141
    - https://unfiltered.adguard-dns.com/dns-query
  fallback:
    - https://cloudflare-dns.com/dns-query
    - https://dns.google/dns-query
  default-nameserver:
    - 9.9.9.9
    - 8.8.8.8
    - 1.1.1.1
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter:
    - "*.lan"
    - "*.localdomain"
    - "*.example"
    - "*.invalid"
    - "*.localhost"
    - "*.test"
    - "*.local"
    - "*.home.arpa"
    - time.*.com
    - time.*.gov
    - time.*.edu.cn
    - time.*.apple.com
    - time1.*.com
    - time2.*.com
    - time3.*.com
    - time4.*.com
    - time5.*.com
    - time6.*.com
    - time7.*.com
    - ntp.*.com
    - ntp1.*.com
    - ntp2.*.com
    - ntp3.*.com
    - ntp4.*.com
    - ntp5.*.com
    - ntp6.*.com
    - ntp7.*.com
    - "*.time.edu.cn"
    - "*.ntp.org.cn"
    - +.pool.ntp.org
    - time1.cloud.tencent.com
    - music.163.com
    - "*.music.163.com"
    - "*.126.net"
    - musicapi.taihe.com
    - music.taihe.com
    - songsearch.kugou.com
    - trackercdn.kugou.com
    - "*.kuwo.cn"
    - api-jooxtt.sanook.com
    - api.joox.com
    - joox.com
    - y.qq.com
    - "*.y.qq.com"
    - streamoc.music.tc.qq.com
    - mobileoc.music.tc.qq.com
    - isure.stream.qqmusic.qq.com
    - dl.stream.qqmusic.qq.com
    - aqqmusic.tc.qq.com
    - amobile.music.tc.qq.com
    - "*.xiami.com"
    - "*.music.migu.cn"
    - music.migu.cn
    - "*.msftconnecttest.com"
    - "*.msftncsi.com"
    - msftconnecttest.com
    - msftncsi.com
    - localhost.ptlogin2.qq.com
    - localhost.sec.qq.com
    - +.srv.nintendo.net
    - +.stun.playstation.net
    - xbox.*.microsoft.com
    - xnotify.xboxlive.com
    - +.battlenet.com.cn
    - +.wotgame.cn
    - +.wggames.cn
    - +.wowsgame.cn
    - +.wargaming.net
    - proxy.golang.org
    - stun.*.*
    - stun.*.*.*
    - +.stun.*.*
    - +.stun.*.*.*
    - +.stun.*.*.*.*
    - heartbeat.belkin.com
    - "*.linksys.com"
    - "*.linksyssmartwifi.com"
    - "*.router.asus.com"
    - mesu.apple.com
    - swscan.apple.com
    - swquery.apple.com
    - swdownload.apple.com
    - swcdn.apple.com
    - swdist.apple.com
    - lens.l.google.com
    - stun.l.google.com
    - +.nflxvideo.net
    - "*.square-enix.com"
    - "*.finalfantasyxiv.com"
    - "*.ffxiv.com"
    - "*.mcdn.bilivideo.cn"
    - +.media.dssott.com

rule-providers:
  ABPindo:
    type: http
    behavior: domain
    format: text
    path: "./rule_provider/ABPindo.txt"
    url: https://raw.githubusercontent.com/zzzt27/clash-AdsBlock/main/ABPindo.txt
    interval: 86400

  oisd_nsfw🔞:
    type: http
    behavior: domain
    format: text
    path: "./rule_provider/oisd_nsfw.txt"
    url: https://raw.githubusercontent.com/zzzt27/clash-AdsBlock/main/oisd_nsfw.txt
    interval: 86400

  oisd_big:
    type: http
    behavior: domain
    format: text
    path: "./rule_provider/oisd_big.txt"
    url: https://raw.githubusercontent.com/zzzt27/clash-AdsBlock/main/oisd_big.txt
    interval: 86400

  rule_adblock:
    type: http
    url: https://raw.githubusercontent.com/ahlawisnu/CLASH/refs/heads/main/adblock.yaml
    behavior: classical
    path: ./rule_provider/adblock.yaml

  rule_haram:
    type: http
    url: https://raw.githubusercontent.com/ahlawisnu/CLASH/refs/heads/main/haram.yaml
    behavior: domain
    path: ./rule_provider/haram.yaml

  rule_18+:
    type: http
    url: https://raw.githubusercontent.com/ahlawisnu/CLASH/refs/heads/main/18+.yaml
    behavior: domain
    path: ./rule_provider/18+.yaml
    

tun:
  enable: true
  dns-hijack:
    - any:53

rules:
  - RULE-SET,ABPindo,ADBLOCK+
  - RULE-SET,oisd_nsfw🔞,ADBLOCK+
  - RULE-SET,oisd_big,ADBLOCK+
  # === FAMILY SAFE FILTER ===
  - RULE-SET,rule_18+,ADBLOCK+
  - RULE-SET,rule_haram,ADBLOCK+
  - RULE-SET,rule_adblock,ADBLOCK+
  
  # ====== to do =======
  
# - DOMAIN-KEYWORD,tiktok,ADBLOCK+
# - DOMAIN-KEYWORD,bigo,ADBLOCK+
# - DOMAIN-KEYWORD,live,ADBLOCK+

  # === FINAL ROUTING ===
  - MATCH,FINAL"""
        
        self.proxies = []
        self.proxy_counter = 0

    def decode_base64(self, data):
        """Decode base64 dengan padding handling"""
        try:
            missing_padding = len(data) % 4
            if missing_padding:
                data += '=' * (4 - missing_padding)
            return base64.b64decode(data).decode('utf-8')
        except:
            return None

    def parse_vmess(self, url):
        """Parse VMess URL"""
        try:
            if not url.startswith('vmess://'):
                return None
            
            b64_data = url[8:]
            json_str = self.decode_base64(b64_data)
            if not json_str:
                return None
            
            data = json.loads(json_str)
            
            proxy = {
                'name': data.get('ps', f'VMess-{self.proxy_counter}'),
                'type': 'vmess',
                'server': data.get('add', ''),
                'port': int(data.get('port', 443)),
                'uuid': data.get('id', ''),
                'alterId': int(data.get('aid', 0)),
                'cipher': data.get('scy', 'auto'),
                'tls': data.get('tls', '') == 'tls',
                'skip-cert-verify': True,
                'servername': data.get('sni', ''),
                'network': data.get('net', 'tcp'),
            }
            
            # Handle ws/grpc network
            if proxy['network'] == 'ws':
                proxy['ws-opts'] = {
                    'path': data.get('path', '/'),
                    'headers': {
                        'Host': data.get('host', '')
                    }
                }
            elif proxy['network'] == 'grpc':
                proxy['grpc-opts'] = {
                    'grpc-service-name': data.get('path', '')
                }
            
            self.proxy_counter += 1
            return proxy
        except Exception as e:
            print(f"Error parsing VMess: {e}")
            return None

    def parse_vless(self, url):
        """Parse VLESS URL"""
        try:
            if not url.startswith('vless://'):
                return None
            
            parsed = urlparse(url)
            uuid = parsed.username
            server = parsed.hostname
            port = parsed.port
            
            query = parse_qs(parsed.query)
            
            proxy = {
                'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'VLESS-{self.proxy_counter}',
                'type': 'vless',
                'server': server,
                'port': port,
                'uuid': uuid,
                'cipher': 'none',
                'tls': 'security' in query and query['security'][0] == 'tls',
                'skip-cert-verify': True,
                'servername': query.get('sni', [''])[0],
                'network': query.get('type', ['tcp'])[0],
            }
            
            # Handle flow
            if 'flow' in query:
                proxy['flow'] = query['flow'][0]
            
            # Handle ws/grpc
            if proxy['network'] == 'ws':
                proxy['ws-opts'] = {
                    'path': query.get('path', ['/'])[0],
                    'headers': {
                        'Host': query.get('host', [''])[0]
                    }
                }
            elif proxy['network'] == 'grpc':
                proxy['grpc-opts'] = {
                    'grpc-service-name': query.get('serviceName', [''])[0]
                }
            
            # Handle reality
            if 'security' in query and query['security'][0] == 'reality':
                proxy['reality-opts'] = {
                    'public-key': query.get('pbk', [''])[0],
                    'short-id': query.get('sid', [''])[0]
                }
                proxy['client-fingerprint'] = query.get('fp', ['chrome'])[0]
            
            self.proxy_counter += 1
            return proxy
        except Exception as e:
            print(f"Error parsing VLESS: {e}")
            return None

    def parse_trojan(self, url):
        """Parse Trojan URL"""
        try:
            if not url.startswith('trojan://'):
                return None
            
            parsed = urlparse(url)
            password = parsed.username
            server = parsed.hostname
            port = parsed.port
            
            query = parse_qs(parsed.query)
            
            proxy = {
                'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'Trojan-{self.proxy_counter}',
                'type': 'trojan',
                'server': server,
                'port': port,
                'password': password,
                'skip-cert-verify': True,
            }
            
            if 'sni' in query:
                proxy['sni'] = query['sni'][0]
            
            if 'type' in query:
                net_type = query['type'][0]
                proxy['network'] = net_type
                
                if net_type == 'ws':
                    proxy['ws-opts'] = {
                        'path': query.get('path', ['/'])[0],
                        'headers': {
                            'Host': query.get('host', [''])[0]
                        }
                    }
                elif net_type == 'grpc':
                    proxy['grpc-opts'] = {
                        'grpc-service-name': query.get('serviceName', [''])[0]
                    }
            
            self.proxy_counter += 1
            return proxy
        except Exception as e:
            print(f"Error parsing Trojan: {e}")
            return None

    def parse_ss(self, url):
        """Parse Shadowsocks URL"""
        try:
            if not url.startswith('ss://'):
                return None
            
            # Handle SIP002 format
            if url.startswith('ss://'):
                parsed = urlparse(url)
                
                # Decode base64 userinfo
                userinfo = parsed.username
                if userinfo:
                    # base64 encoded method:password
                    decoded = self.decode_base64(userinfo)
                    if decoded and ':' in decoded:
                        method, password = decoded.split(':', 1)
                    else:
                        return None
                else:
                    return None
                
                server = parsed.hostname
                port = parsed.port
                
                proxy = {
                    'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'SS-{self.proxy_counter}',
                    'type': 'ss',
                    'server': server,
                    'port': port,
                    'cipher': method,
                    'password': password,
                }
                
                # Handle plugin
                query = parse_qs(parsed.query)
                if 'plugin' in query:
                    plugin_str = query['plugin'][0]
                    if 'obfs' in plugin_str:
                        # simple-obfs
                        parts = plugin_str.split(';')
                        proxy['plugin'] = 'obfs'
                        for part in parts[1:]:
                            if '=' in part:
                                key, val = part.split('=', 1)
                                if key == 'obfs':
                                    proxy['plugin-opts'] = {'mode': val}
                                elif key == 'obfs-host':
                                    if 'plugin-opts' not in proxy:
                                        proxy['plugin-opts'] = {}
                                    proxy['plugin-opts']['host'] = val
                
                self.proxy_counter += 1
                return proxy
        except Exception as e:
            print(f"Error parsing SS: {e}")
            return None

    def parse_ssr(self, url):
        """Parse ShadowsocksR URL"""
        try:
            if not url.startswith('ssr://'):
                return None
            
            decoded = self.decode_base64(url[6:])
            if not decoded:
                return None
            
            # Format: server:port:protocol:method:obfs:password_base64/?params_base64
            match = re.match(r'([^:]+):(\d+):([^:]+):([^:]+):([^:]+):([^/]+)/?\?(.*)', decoded)
            if not match:
                return None
            
            server, port, protocol, method, obfs, password_b64, params = match.groups()
            password = self.decode_base64(password_b64) or password_b64
            
            # Parse params
            param_dict = {}
            for param in params.split('&'):
                if '=' in param:
                    k, v = param.split('=', 1)
                    param_dict[k] = self.decode_base64(v) or v
            
            proxy = {
                'name': param_dict.get('remarks', f'SSR-{self.proxy_counter}'),
                'type': 'ssr',
                'server': server,
                'port': int(port),
                'cipher': method,
                'password': password,
                'protocol': protocol,
                'obfs': obfs,
                'protocol-param': param_dict.get('protoparam', ''),
                'obfs-param': param_dict.get('obfsparam', ''),
            }
            
            self.proxy_counter += 1
            return proxy
        except Exception as e:
            print(f"Error parsing SSR: {e}")
            return None

    def parse_hysteria(self, url):
        """Parse Hysteria/Hysteria2 URL"""
        try:
            if url.startswith('hysteria2://') or url.startswith('hy2://'):
                parsed = urlparse(url)
                password = parsed.username
                server = parsed.hostname
                port = parsed.port or 443
                
                query = parse_qs(parsed.query)
                
                proxy = {
                    'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'Hysteria2-{self.proxy_counter}',
                    'type': 'hysteria2',
                    'server': server,
                    'port': port,
                    'password': password,
                    'skip-cert-verify': True,
                }
                
                if 'sni' in query:
                    proxy['sni'] = query['sni'][0]
                
                if 'obfs' in query:
                    proxy['obfs'] = query['obfs'][0]
                    if 'obfs-password' in query:
                        proxy['obfs-password'] = query['obfs-password'][0]
                
                self.proxy_counter += 1
                return proxy
                
            elif url.startswith('hysteria://'):
                parsed = urlparse(url)
                server = parsed.hostname
                port = parsed.port
                
                query = parse_qs(parsed.query)
                
                proxy = {
                    'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'Hysteria-{self.proxy_counter}',
                    'type': 'hysteria',
                    'server': server,
                    'port': port,
                    'skip-cert-verify': True,
                }
                
                if 'protocol' in query:
                    proxy['protocol'] = query['protocol'][0]
                if 'auth' in query:
                    proxy['auth-str'] = query['auth'][0]
                if 'upmbps' in query:
                    proxy['up'] = query['upmbps'][0]
                if 'downmbps' in query:
                    proxy['down'] = query['downmbps'][0]
                if 'sni' in query:
                    proxy['sni'] = query['sni'][0]
                if 'alpn' in query:
                    proxy['alpn'] = query['alpn'][0].split(',')
                
                self.proxy_counter += 1
                return proxy
                
        except Exception as e:
            print(f"Error parsing Hysteria: {e}")
            return None

    def parse_tuic(self, url):
        """Parse TUIC URL"""
        try:
            if not url.startswith('tuic://'):
                return None
            
            parsed = urlparse(url)
            uuid = parsed.username
            password = parsed.password
            server = parsed.hostname
            port = parsed.port
            
            query = parse_qs(parsed.query)
            
            proxy = {
                'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'TUIC-{self.proxy_counter}',
                'type': 'tuic',
                'server': server,
                'port': port,
                'uuid': uuid,
                'password': password,
                'skip-cert-verify': True,
            }
            
            if 'congestion_control' in query:
                proxy['congestion-controller'] = query['congestion_control'][0]
            if 'udp_relay_mode' in query:
                proxy['udp-relay-mode'] = query['udp_relay_mode'][0]
            if 'sni' in query:
                proxy['sni'] = query['sni'][0]
            if 'alpn' in query:
                proxy['alpn'] = query['alpn'][0].split(',')
            
            self.proxy_counter += 1
            return proxy
        except Exception as e:
            print(f"Error parsing TUIC: {e}")
            return None

    def parse_wireguard(self, url):
        """Parse WireGuard URL"""
        try:
            if not url.startswith('wg://') and not url.startswith('wireguard://'):
                return None
            
            parsed = urlparse(url)
            server = parsed.hostname
            port = parsed.port
            
            query = parse_qs(parsed.query)
            
            proxy = {
                'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'WG-{self.proxy_counter}',
                'type': 'wireguard',
                'server': server,
                'port': port,
            }
            
            if 'publickey' in query:
                proxy['public-key'] = query['publickey'][0]
            if 'privatekey' in query:
                proxy['private-key'] = query['privatekey'][0]
            if 'presharedkey' in query:
                proxy['pre-shared-key'] = query['presharedkey'][0]
            if 'mtu' in query:
                proxy['mtu'] = int(query['mtu'][0])
            if 'reserved' in query:
                proxy['reserved'] = query['reserved'][0].split(',')
            
            self.proxy_counter += 1
            return proxy
        except Exception as e:
            print(f"Error parsing WireGuard: {e}")
            return None

    def parse_socks_http(self, url):
        """Parse SOCKS5/HTTP proxy URL"""
        try:
            if url.startswith('socks5://') or url.startswith('socks://'):
                parsed = urlparse(url)
                proxy = {
                    'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'SOCKS5-{self.proxy_counter}',
                    'type': 'socks5',
                    'server': parsed.hostname,
                    'port': parsed.port,
                }
                if parsed.username:
                    proxy['username'] = parsed.username
                if parsed.password:
                    proxy['password'] = parsed.password
                
                self.proxy_counter += 1
                return proxy
                
            elif url.startswith('http://') or url.startswith('https://'):
                parsed = urlparse(url)
                proxy = {
                    'name': urllib.parse.unquote(parsed.fragment) if parsed.fragment else f'HTTP-{self.proxy_counter}',
                    'type': 'http',
                    'server': parsed.hostname,
                    'port': parsed.port,
                }
                if parsed.username:
                    proxy['username'] = parsed.username
                if parsed.password:
                    proxy['password'] = parsed.password
                if url.startswith('https://'):
                    proxy['tls'] = True
                    proxy['skip-cert-verify'] = True
                
                self.proxy_counter += 1
                return proxy
                
        except Exception as e:
            print(f"Error parsing SOCKS/HTTP: {e}")
            return None

    def parse_url(self, url):
        """Parse single URL dan return proxy config"""
        url = url.strip()
        if not url:
            return None
        
        parsers = [
            self.parse_vmess,
            self.parse_vless,
            self.parse_trojan,
            self.parse_ss,
            self.parse_ssr,
            self.parse_hysteria,
            self.parse_tuic,
            self.parse_wireguard,
            self.parse_socks_http,
        ]
        
        for parser in parsers:
            result = parser(url)
            if result:
                return result
        
        return None

    def parse_subscription(self, data):
        """Parse subscription data (base64 atau plain text)"""
        proxies = []
        
        # Coba decode base64 dulu
        decoded = self.decode_base64(data)
        if decoded:
            lines = decoded.strip().split('\n')
        else:
            lines = data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            proxy = self.parse_url(line)
            if proxy:
                proxies.append(proxy)
        
        return proxies

    def generate_full_config(self, proxies):
        """Generate full config dengan proxies langsung (tanpa proxy provider)"""
        config = yaml.safe_load(self.config_template)
        
        # Hapus proxy-providers
        if 'proxy-providers' in config:
            del config['proxy-providers']
        
        # Update proxy-groups untuk tidak menggunakan provider
        for group in config.get('proxy-groups', []):
            if 'use' in group:
                del group['use']
            # Tambah proxies ke grup yang perlu
            if group.get('type') in ['fallback', 'url-test', 'load-balance']:
                if 'proxies' not in group:
                    group['proxies'] = [p['name'] for p in proxies]
        
        # Tambah proxies
        config['proxies'] = proxies
        
        return config

    def generate_provider_config(self):
        """Generate config dengan proxy provider (template asli)"""
        return yaml.safe_load(self.config_template)

    def generate_proxies_provider_file(self, proxies):
        """Generate file akun.yaml untuk proxy provider"""
        return {'proxies': proxies}

    def save_config(self, config, filename):
        """Save config ke file YAML"""
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"[✓] Config saved: {filename}")

    def save_proxies_list(self, proxies, filename='akun.yaml'):
        """Save proxies list untuk provider"""
        data = self.generate_proxies_provider_file(proxies)
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"[✓] Proxies provider saved: {filename}")


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║     CLASH/MIHOMO CONFIG GENERATOR FOR TERMUX             ║
║     Support: VMess, VLESS, Trojan, SS, SSR,              ║
║              Hysteria(2), TUIC, WireGuard, SOCKS, HTTP   ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    print_banner()
    
    generator = ClashConfigGenerator()
    
    print("Pilih mode:")
    print("1. Generate dari file subscription (txt)")
    print("2. Generate dari single URL")
    print("3. Generate dari clipboard (Termux)")
    print()
    print("Format output:")
    print("a. Full Config (tanpa proxy provider)")
    print("b. Proxy Provider Config + akun.yaml")
    print()
    
    mode = input("Pilih mode (1/2/3): ").strip()
    output_format = input("Pilih format output (a/b): ").strip().lower()
    
    proxies = []
    
    if mode == '1':
        filename = input("Masukkan nama file subscription (.txt): ").strip()
        if not os.path.exists(filename):
            print(f"[!] File {filename} tidak ditemukan!")
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        proxies = generator.parse_subscription(data)
        
    elif mode == '2':
        url = input("Masukkan URL: ").strip()
        proxy = generator.parse_url(url)
        if proxy:
            proxies = [proxy]
        
    elif mode == '3':
        # Untuk Termux, gunakan termux-clipboard-get
        try:
            import subprocess
            result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
            data = result.stdout
            proxies = generator.parse_subscription(data)
        except Exception as e:
            print(f"[!] Error accessing clipboard: {e}")
            print("[!] Pastikan termux-api terinstall")
            return
    
    if not proxies:
        print("[!] Tidak ada proxy yang berhasil diparse!")
        return
    
    print(f"[+] Berhasil parse {len(proxies)} proxies")
    
    # Print daftar proxies
    print("\n[+] Daftar Proxies:")
    for i, p in enumerate(proxies, 1):
        print(f"  {i}. {p['name']} ({p['type']}) - {p['server']}:{p['port']}")
    
    if output_format == 'a':
        # Full config
        config = generator.generate_full_config(proxies)
        generator.save_config(config, 'config.yaml')
        print("\n[✓] Full config berhasil dibuat: config.yaml")
        
    elif output_format == 'b':
        # Proxy provider config
        config = generator.generate_provider_config()
        generator.save_config(config, 'config.yaml')
        generator.save_proxies_list(proxies, 'akun.yaml')
        print("\n[✓] Proxy provider config berhasil dibuat:")
        print("    - config.yaml (main config)")
        print("    - akun.yaml (proxy list)")
    
    print("\n[!] Catatan:")
    print("    - Pastikan folder rule_provider sudah dibuat")
    print("    - Jalankan: mkdir -p rule_provider")


if __name__ == '__main__':
    main()
