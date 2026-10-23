# F0undry

F0undry is a defensive security reconnaissance tool designed to detect freshly created domains and short links that are rapidly spreading through Telegram channels and communities. The core idea is simple: when a domain is launched quickly and exposed publicly, it often goes live with misconfigurations, redirect chains, leaked credentials, or hidden secrets before it is properly reviewed. F0undry helps identify those risks early.

It connects to Telegram through the Telethon API, scans historical messages from a target channel or chat, extracts links and URL payloads, resolves them through a browser-based flow, and follows redirect chains to uncover the real destination domain. Once the final domain is identified, the tool runs secret discovery checks against it using browser automation and tools such as TruffleHog and other secret-finding workflows.

The result is a structured list of findings shown in a GUI, making it easier to spot exposed API keys, tokens, or other sensitive material that may have been left behind on newly launched domains.

![F0undry Screenshot](f0undry-screenshot.png)

## What F0undry does

F0undry is built to solve a very specific problem:

- Telegram channels frequently share fresh domains and shortened links.
- Many of these domains are created quickly and may not be properly monitored.
- If a redirect or landing page exposes sensitive information, it can be missed until much later.
- F0undry helps catch these issues earlier by automating the discovery and verification process.

In practice, the tool does the following:

1. Connects to Telegram using the Telethon API.
2. Fetches historical messages from a configured channel or chat.
3. Extracts URLs, shortened links, and redirect chains.
4. Opens them in a browser using Playwright or Selenium.
5. Resolves final domains and landing pages.
6. Scans the exposed pages and related JS assets for secrets.
7. Runs tools such as TruffleHog and secret finder checks.
8. Lists the discovered results in a GUI for triage.

## Why it matters

The project targets a critical gap in early-warning security monitoring: newly created domains appear fast, spread fast, and may be abused or misconfigured before they are reviewed. F0undry gives defenders a way to automatically detect and investigate these domains before they become a bigger security problem.

This is particularly useful for:

- Security researchers
- Bug bounty workflows
- Threat intelligence teams
- Defensive monitoring of public Telegram communities
- Early detection of exposed credentials and infrastructure risks

## Features

### Telegram-based reconnaissance
- Pulls historical messages and links from target Telegram chats or channels
- Extracts URLs, redirect payloads, and shared short links
- Filters and normalizes suspicious target domains

### Browser-based resolution
- Opens links in a headless browser using Playwright / Selenium
- Resolves short URLs and redirect chains to real domains
- Captures final destination pages and associated content

### Secret detection
- Scans domains and linked assets for leaked credentials
- Uses secret discovery patterns and automated validation techniques
- Integrates with tools such as TruffleHog and other secret finder workflows

### GUI output
- Displays results in a user-friendly interface
- Helps analysts quickly prioritize suspicious findings
- Makes repetitive monitoring more manageable

## Project structure

```text
F0undry/
├── core/
│   ├── f0undry_gui.py
│   └── frank_headless_v2_ultimate.py
├── tools/
│   ├── SecretFinder-master/
│   ├── keyhacks-master/
│   ├── HEDnsExtractor-main/
│   ├── t-hoog-ex/
│   └── keyhacks_validator.py
├── config/
│   └── config.py
├── chrome-win/
│   └── chrome.exe
├── results/
├── run_f0undry.py
├── README.md
└── requirements.txt
```

## Installation

### Prerequisites

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Optional browser setup

```bash
playwright install chromium
```

## Configuration

Before running the tool, configure Telegram access and any required environment variables:

```bash
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
```

You may also need to update configuration values inside `config/config.py` depending on your environment and target workflow.

## Quick start

```bash
git clone https://github.com/ksbicorp/F0undry.git
cd F0undry
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python run_f0undry.py
```

## Legal and ethical use

F0undry is intended for authorized security testing and defensive research only.

- Use only on systems or domains you own or are explicitly authorized to test.
- Do not scan or analyze unauthorized infrastructure.
- Do not use it for malicious purposes or to violate the terms of service of any platform or product.
- Comply with the laws and regulations in your jurisdiction.

## Disclaimer

This project is a research and monitoring tool focused on proactive security detection. It is not intended to facilitate unauthorized access, abuse, or malicious activity.

## Credits and ecosystem

This project draws inspiration from and integrates techniques and tools used across the security research ecosystem, including:

- SecretFinder
- TruffleHog
- KeyHacks
- HEDnsExtractor
- Playwright
- Telethon

## Contributing

Contributions are welcome. If you want to improve the scanner, add new detection logic, enhance browser resolution, or improve the GUI workflow, feel free to open an issue or submit a pull request.

## License

This project is distributed under the repository's existing license terms. Please refer to the repository for the specific licensing details.
