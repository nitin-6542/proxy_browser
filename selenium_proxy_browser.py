import time
import random
import threading
import zipfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ========= CONFIG =========
PROXY_FILE = "proxies.txt"
proxy_ip_url = "https://httpbin.org/ip"
MAX_WATCH = 30
close_browser = True
run_in_background = False
MIN_THREADS_PER_BATCH = 2
MAX_THREADS_PER_BATCH = 4
DELAY_BETWEEN_BATCHES = 5
EXT_DIR = "extensions"
# ==========================

def parse_proxy_line(proxy_line: str):
    """
    Parse proxy line format: username:password@host:port
    """
    try:
        proxy_line = proxy_line.strip()
        if '@' in proxy_line:
            credentials, host_port = proxy_line.split('@', 1)
            username, password = credentials.split(':', 1)
            host, port = host_port.split(':', 1)
            return host, int(port), username, password, proxy_line
        else:
            print(f"Invalid proxy format: {proxy_line}")
            return None, None, None, None, proxy_line
    except Exception as e:
        print(f"Error parsing proxy line '{proxy_line}': {e}")
        return None, None, None, None, proxy_line

def load_proxies(file_path: str):
    proxies = []
    try:
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        for line in lines:
            host, port, username, password, original = parse_proxy_line(line)
            if all([host, port, username, password]):
                proxies.append({
                    'host': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'original': original
                })
        print(f"Loaded {len(proxies)} valid proxies from {file_path}")
    except FileNotFoundError:
        print(f"FATAL: Proxy file '{file_path}' not found.")
    return proxies

def create_proxy_extension(proxy):
    """
    Generate a Chrome extension to handle proxy authentication.
    """
    if not os.path.exists(EXT_DIR):
        os.makedirs(EXT_DIR)

    ext_path = os.path.join(EXT_DIR, f"{proxy['host']}_{proxy['port']}.zip")

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
              singleProxy: {{
                scheme: "http",
                host: "{proxy['host']}",
                port: parseInt({proxy['port']})
              }},
              bypassList: ["localhost"]
            }}
          }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{proxy['username']}",
                password: "{proxy['password']}"
            }}
        }};
    }}
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {{urls: ["<all_urls>"]}},
                ['blocking']
    );
    """

    with zipfile.ZipFile(ext_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return ext_path

def create_driver(proxy):
    options = Options()
    if run_in_background:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--mute-audio")

    ext_file = create_proxy_extension(proxy)
    options.add_extension(ext_file)

    driver = webdriver.Chrome(options=options)
    return driver

def run_browser(proxy):
    try:
        driver = create_driver(proxy)
        driver.get(proxy_ip_url)
        time.sleep(2)
        ip = driver.find_element("tag name", "body").text
        print(f"✅ Current IP via {proxy['original']}: {ip}")
        watch_time = random.randint(5, MAX_WATCH)
        time.sleep(watch_time)
    except Exception as e:
        print(f"⚠️ Error with proxy {proxy['original']}: {e}")
    finally:
        if close_browser:
            driver.quit()
            print(f"[{proxy['original']}] Browser closed")

def batch_run(proxies, batch_number):
    print(f"\n=== Starting Batch {batch_number} with {len(proxies)} threads ===")
    threads = []
    for proxy in proxies:
        t = threading.Thread(target=run_browser, args=(proxy,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def main():
    proxy_list = load_proxies(PROXY_FILE)
    if not proxy_list:
        return

    total_proxies = len(proxy_list)
    processed = 0
    batch_number = 0

    while processed < total_proxies:
        batch_number += 1
        batch_size = random.randint(MIN_THREADS_PER_BATCH, MAX_THREADS_PER_BATCH)
        start = processed
        end = min(start + batch_size, total_proxies)
        current_batch = proxy_list[start:end]

        if not current_batch:
            break

        batch_run(current_batch, batch_number)

        processed = end
        if processed < total_proxies:
            print(f"Batch {batch_number} done. Waiting {DELAY_BETWEEN_BATCHES} seconds...\n")
            time.sleep(DELAY_BETWEEN_BATCHES)

    print("🏁 All proxies processed.")

if __name__ == "__main__":
    main()
