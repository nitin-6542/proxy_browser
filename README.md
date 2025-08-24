```markdown
# Advanced Python Proxy Automation Engine

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

An advanced Python script for web automation that uses Playwright and a rotating proxy system to bypass IP blocks and scale tasks. Ideal for ethical web scraping, data collection, and application testing.

---

## The Problem This Solves

Web automation and data scraping at scale often fail when a single IP address is overused, leading to blocks, CAPTCHAs, and rate limits. This project provides a robust solution by creating a "proxy army" that intelligently distributes requests across multiple IP addresses, making your automation scripts more resilient and virtually undetectable.

## Key Features

-   **Automated Proxy Rotation:** Seamlessly loads and rotates through a list of proxies from a text file.
-   **Advanced Browser Automation:** Uses `Playwright` to create isolated browser contexts for each proxy, complete with unique, realistic user agents.
-   **Asynchronous for High Performance:** Built with `asyncio` to handle multiple browser instances concurrently without performance degradation.
-   **Intelligent Batch Processing:** Runs tasks in randomized, sequential batches with built-in delays to mimic human behavior and avoid triggering anti-bot systems.
-   **Headless & Headful Modes:** Run the script with visible browsers for debugging or in a fully headless mode for production servers.
-   **Highly Configurable:** Easily adjust all major parameters—from batch sizes to browser behavior—in a centralized configuration section.

## Installation and Setup

Follow these steps to get the project up and running on your local machine.

#### 1. Clone the Repository
```

git clone https://github.com/nitin-6542/proxy_browser.git
cd proxy_browser

```

#### 2. Create a Virtual Environment (Recommended)
Using a virtual environment prevents conflicts with other Python projects.
```


# Create the environment

python -m venv venv

# Activate the environment

# On Windows:

venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

```

#### 3. Install Dependencies
This project requires `Playwright`. Create a `requirements.txt` file with the following content:
```

playwright

```
Then, install it using `pip`:
```

pip install -r requirements.txt

```

#### 4. Install Browser Drivers
Playwright needs its own browser binaries to work correctly. Install them with this command:
```

playwright install

```
*For Linux systems, you may need to install system dependencies:* `playwright install --with-deps`

## Configuration

Before running the script, configure the settings at the top of the Python file (`your_script_name.py`).

| Variable                  | Description                                                               |
| ------------------------- | ------------------------------------------------------------------------- |
| `PROXY_FILE`              | The path to your proxy list file (e.g., `"proxies.txt"`).                  |
| `proxy_ip_url`            | The URL used to verify the current IP address of a browser instance.      |
| `close_browser`           | Set to `True` to close each browser automatically after its task is done. |
| `run_in_background`       | Set to `True` for headless mode (no visible browser windows).             |
| `MIN_THREADS_PER_BATCH`   | The minimum number of concurrent browser tasks to run in a single batch.  |
| `MAX_THREADS_PER_BATCH`   | The maximum number of concurrent browser tasks to run in a single batch.  |
| `DELAY_BETWEEN_BATCHES`   | The number of seconds to wait before starting the next batch.             |

#### Create Your Proxy File
Create a file named `proxies.txt` in the root directory. Add your proxies, one per line, in the following format:
```

username:password@host:port
username2:password2@host2:port2

```

## How to Run the Script

Once everything is configured, run the script from your terminal:
```

python your_script_name.py

```
The script will log its progress, including the batch number, the IP addresses being used, and any errors encountered.

## How It Works

The script's architecture is designed for scalability and stealth:
1.  **Load Proxies:** It reads the `proxies.txt` file and parses the credentials for each proxy.
2.  **Batch Creation:** It divides the list of proxies into smaller, randomized batches.
3.  **Asynchronous Execution:** For each proxy in a batch, it launches a new browser instance using `asyncio` and `Playwright`.
4.  **Browser Isolation:** Each browser is configured with its assigned proxy and a unique, randomly generated user agent to appear as a distinct user.
5.  **Task Execution:** The script navigates to an IP-checking URL to confirm the proxy is working and logs the result.
6.  **Delay and Repeat:** After a batch completes, the script waits for a configured delay before processing the next one, until all proxies have been used.

## Contributing

Contributions are welcome! Whether you want to fix a bug, add a new feature, or improve the documentation, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourAmazingFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/YourAmazingFeature`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Disclaimer

This script is intended for educational purposes and for performing ethical web automation on websites where you have explicit permission. The user assumes all responsibility for complying with the terms of service of any website they target. The creators of this script are not responsible for any misuse. Please use this tool responsibly.
```

<div style="text-align: center">⁂</div>

[^1]: https://github.com/nitin-6542/proxy_browser

