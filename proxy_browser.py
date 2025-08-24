import asyncio
import random
import time
from typing import Dict, List, Tuple
from playwright.async_api import async_playwright, Page, BrowserContext
import logging
import json

# ========= CONFIG =========
PROXY_FILE = "proxies.txt"  # Your proxy file
proxy_ip_url = "https://httpbin.org/ip"
MAX_WATCH = 100  # max seconds to watch video
close_browser = True  # Set to False if you want to keep the browser open after running
run_in_background = False  # Set to False if you want to run in sequential batches

# NEW: Configuration for running in sequential batches
MIN_THREADS_PER_BATCH = 20
MAX_THREADS_PER_BATCH = 20
DELAY_BETWEEN_BATCHES = 5 # Seconds to wait between finishing one batch and starting the next
# =========================

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_proxy_line(proxy_line: str) -> Tuple[str, int, str, str, str]:
    """
    Parse proxy line format: username:password@host:port
    Returns: (host, port, username, password, original_line)
    """
    try:
        proxy_line = proxy_line.strip()
        if '@' in proxy_line:
            credentials, host_port = proxy_line.split('@', 1)
            username, password = credentials.split(':', 1)
            host, port = host_port.split(':', 1)
            return host, int(port), username, password, proxy_line
        else:
            logger.error(f"Invalid proxy format: {proxy_line}")
            return None, None, None, None, proxy_line
    except Exception as e:
        logger.error(f"Error parsing proxy line '{proxy_line}': {e}")
        return None, None, None, None, proxy_line

def generate_desktop_ua() -> Dict[str, str]:
    major = random.randint(122, 128)
    build = random.randint(6200, 6800)
    patch = random.randint(80, 200)
    ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major}.0.{build}.{patch} Safari/537.36"
    accept_language = random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.9"])
    return {"user_agent": ua, "accept_language": accept_language}

def load_proxies(file_path: str) -> List[Dict]:
    """Load proxy list from file and parse each proxy"""
    try:
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        proxies = []
        for i, line in enumerate(lines):
            host, port, username, password, original = parse_proxy_line(line)
            if all([host, port, username, password]):
                proxies.append({
                    'host': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'original': original
                })
        logger.info(f"Loaded {len(proxies)} valid proxies from {file_path}")
        return proxies
    except FileNotFoundError:
        logger.error(f"FATAL: Proxy file '{file_path}' not found. Please create it.")
        return []



async def create_browser(proxy_details: Dict):
    ua_bundle = generate_desktop_ua()
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=run_in_background, args=['--mute-audio'])
    context = await browser.new_context(
        user_agent=ua_bundle["user_agent"],
        viewport={"width": 1280, "height": 720},
        locale=ua_bundle["accept_language"].split(",")[0],
        proxy={
            "server": f"http://{proxy_details['host']}:{proxy_details['port']}",
            "username": proxy_details['username'],
            "password": proxy_details['password']
        },
        java_script_enabled=True
    )
    page = await context.new_page()
    return playwright, browser, context, page
    
async def run_browser(proxy_details: Dict):
    playwright, browser, context, page = await create_browser(proxy_details)
    try:
        await page.goto(proxy_ip_url, timeout=10000)   # go to https://api.ipify.org/
        ip = await page.inner_text("body")             # extract IP text from body
        print(f"✅ Current IP: {ip}")                  # print IP
    except Exception as e:
        print(f"⚠️ Error with proxy {proxy_details['original']}: {e}")
    finally:
        if close_browser ==True:
            await context.close()                       # close context
            await browser.close()                       # close browser
            await playwright.stop()                     # stop playwright
        print(f"[{proxy_details['original']}] Browser closed")


# --- MODIFIED MAIN FUNCTION FOR SEQUENTIAL BATCHING ---
async def main():
    """
    Main execution function that runs proxies in sequential batches.
    """
    proxy_list = load_proxies(PROXY_FILE)
    if not proxy_list:
        return

    total_proxies = len(proxy_list)
    processed_proxies = 0
    batch_number = 0

    logger.info(f"🚀 Starting proxy automation for {total_proxies} proxies in sequential batches.")

    while processed_proxies < total_proxies:
        batch_number += 1
        
        # Determine the size of the current batch (2-10 threads)
        batch_size = random.randint(MIN_THREADS_PER_BATCH, MAX_THREADS_PER_BATCH)
        
        # Get the slice of proxies for the current batch
        start_index = processed_proxies
        end_index = min(start_index + batch_size, total_proxies)
        current_batch = proxy_list[start_index:end_index]

        if not current_batch:
            break # No more proxies to process

        logger.info("="*60)
        logger.info(f"--- Starting Batch {batch_number} | Running {len(current_batch)} threads ---")
        logger.info(f"--- Proxies in this batch: {start_index + 1} to {end_index} ---")
        logger.info("="*60)

        # Create and run tasks for the current batch
        tasks = [run_browser(proxy) for proxy in current_batch]
        await asyncio.gather(*tasks)

        # Update the number of processed proxies
        processed_proxies = end_index

        if processed_proxies < total_proxies:
            logger.info(f"--- Batch {batch_number} finished. Waiting {DELAY_BETWEEN_BATCHES} seconds before next batch. ---")
            await asyncio.sleep(DELAY_BETWEEN_BATCHES)

    logger.info("="*60)
    logger.info("🏁 All proxies have been processed. Automation finished. 🏁")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(main())
