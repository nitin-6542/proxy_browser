
# 🚀 Advanced Python Proxy Automation Engine

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

An advanced Python engine for **web automation with Playwright and rotating proxies**.  
Designed for bypassing IP blocks, CAPTCHAs, and rate limits — perfect for **ethical web scraping, data collection, and testing**.

---

## 📌 Why This Project?

Web automation often breaks when using a single IP:  
❌ Frequent blocks  
❌ CAPTCHAs  
❌ Rate limits  

✅ This project solves it by creating a **rotating proxy army** — distributing requests across multiple IPs, making automation more resilient and stealthy.

---

## ✨ Features

- 🔄 **Automated Proxy Rotation** – Load & rotate proxies from a file.
- 🕹 **Playwright Integration** – Isolated browser contexts with unique user agents.
- ⚡ **Asynchronous Execution** – `asyncio` for handling multiple browsers concurrently.
- 🧩 **Batch Processing** – Randomized batches with configurable delays.
- 👀 **Headless & Headful Modes** – Debug visually or run silently in production.
- ⚙️ **Highly Configurable** – Centralized configuration for quick tweaks.

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nitin-6542/proxy_browser.git
cd proxy_browser
```

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3️⃣ Install Dependencies
Create a `requirements.txt` with:
```
playwright
```
Then install:
```bash
pip install -r requirements.txt
```

### 4️⃣ Install Playwright Browsers
```bash
playwright install
# For Linux
playwright install --with-deps
```

---

## 🔧 Configuration

Edit the variables in your Python script:

| Variable                | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
| `PROXY_FILE`            | Path to proxy list file (e.g. `proxies.txt`).                      |
| `proxy_ip_url`          | URL to verify IP of each browser instance.                         |
| `close_browser`         | Auto-close browser after task (`True/False`).                      |
| `run_in_background`     | Run in headless mode (`True`) or visible mode (`False`).           |
| `MIN_THREADS_PER_BATCH` | Min concurrent browser tasks per batch.                            |
| `MAX_THREADS_PER_BATCH` | Max concurrent browser tasks per batch.                            |
| `DELAY_BETWEEN_BATCHES` | Delay (in seconds) before starting next batch.                     |

### Proxy File Format
Create `proxies.txt`:
```
username:password@host:port
username2:password2@host2:port2
```

---

## ▶️ Usage

Run the script:
```bash
python proxy_browser.py
```

✅ Logs include batch numbers, IPs used, and errors encountered.

---

## 🔍 How It Works

1. **Load Proxies** → Reads and parses `proxies.txt`.  
2. **Batch Creation** → Splits proxies into randomized batches.  
3. **Async Execution** → Launches concurrent Playwright browsers.  
4. **Isolation** → Each browser gets a proxy + unique user agent.  
5. **Verification** → Visits IP-check URL and logs result.  
6. **Repeat** → Runs until all proxies are used (with delays).  

---

## 📝 Example Python Usage
```python
import asyncio
from playwright.async_api import async_playwright

async def check_ip(proxy: str):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(proxy={"server": proxy})
        page = await browser.new_page()
        await page.goto("https://httpbin.org/ip")
        content = await page.content()
        print(f"Proxy {proxy} returned: {content}")
        await browser.close()

asyncio.run(check_ip("username:password@host:port"))
```

---

## 🤝 Contributing

Contributions are welcome! 🚀  

1. Fork the repo  
2. Create a branch (`git checkout -b feature/YourAmazingFeature`)  
3. Commit (`git commit -m 'Add some AmazingFeature'`)  
4. Push (`git push origin feature/YourAmazingFeature`)  
5. Open a PR 🎉  

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE).

---

## ⚠️ Disclaimer

This tool is for **educational and ethical use only**.  
Do not use it on websites without explicit permission.  
The authors are **not responsible for misuse**.

---

<div align="center">

⭐ If you find this project useful, give it a star on [GitHub](https://github.com/nitin-6542/proxy_browser)! ⭐  

</div>
